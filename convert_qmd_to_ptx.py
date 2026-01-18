#!/usr/bin/env python3
"""
Convert Quarto markdown (.qmd) files to PreText XML format
"""

import re
import sys

def escape_xml(text):
    """Escape XML special characters"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text

def convert_inline_markdown(text):
    """Convert inline markdown to PreText XML"""
    # Don't escape yet - we'll do specific replacements first
    
    # Remove footnote markers and inline footnotes
    text = re.sub(r'\^\[[^\]]+\]', '', text)  # Remove ^[...] style footnotes
    text = re.sub(r'\[\^[^\]]+\]', '', text)  # Remove [^...] style references
    
    # Convert cross-references @sec-xxx to <xref ref="sec-xxx"/>
    text = re.sub(r'@(sec|ch|fig|tbl)-([a-z0-9\-]+)', r'<xref ref="\1-\2"/>', text)
    
    # Convert links [text](url) - must do before escaping
    def link_repl(m):
        return '<url href="{}">{}</url>'.format(m.group(2), escape_xml(m.group(1)))
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', link_repl, text)
    
    # Convert inline R code `r ...` to just <c>...</c> (we can't execute it)
    text = re.sub(r'`r\s+([^`]+)`', r'<c>\1</c>', text)
    
    # Now escape XML characters for remaining text
    # But we need to preserve our already-created tags
    parts = re.split(r'(<url href="[^"]+">.*?</url>|<xref ref="[^"]+"/>|<c>.*?</c>)', text)
    for i in range(len(parts)):
        if not parts[i].startswith('<'):
            parts[i] = escape_xml(parts[i])
    text = ''.join(parts)
    
    # Convert inline code `text` (remaining ones)
    text = re.sub(r'`([^`]+)`', r'<c>\1</c>', text)
    
    # Convert bold **text**
    text = re.sub(r'\*\*([^\*]+)\*\*', r'<alert>\1</alert>', text)
    
    # Convert italic *text* or _text_ (but not emphasis already in tags)
    text = re.sub(r'(?<![<\w])\*([^\*<]+)\*(?![>\w])', r'<em>\1</em>', text)
    text = re.sub(r'(?<![<\w])_([^_<]+)_(?![>\w])', r'<em>\1</em>', text)
    
    # Convert inline math $...$ but NOT escaped dollar signs \$
    # First protect escaped dollar signs
    text = text.replace(r'\$', '<<<DOLLAR>>>')
    text = re.sub(r'\$([^\$]+)\$', r'<m>\1</m>', text)
    # Restore escaped dollar signs as regular dollar signs
    text = text.replace('<<<DOLLAR>>>', '$')
    
    return text

def convert_qmd_to_ptx(qmd_content, chapter_id, chapter_title):
    """Convert Quarto markdown to PreText XML"""
    
    lines = qmd_content.split('\n')
    result = []
    
    # State tracking
    in_code_block = False
    code_block_content = []
    code_lang = "r"
    in_list = False
    list_type = None
    list_indent = 0
    in_callout = False
    section_depth = 0
    subsection_depth = 0
    para_buffer = []
    
    def flush_para():
        """Flush accumulated paragraph lines"""
        if para_buffer:
            para_text = ' '.join(para_buffer)
            para_text = convert_inline_markdown(para_text)
            indent = '          ' + '  ' * subsection_depth
            result.append(indent + '<p>{}</p>'.format(para_text))
            result.append('')
            para_buffer.clear()
    
    def close_list():
        nonlocal in_list
        if in_list:
            indent = '          ' + '  ' * subsection_depth
            result.append(indent + ('</ol>' if list_type == 'ol' else '</ul>'))
            result.append('')
            in_list = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip the main title (it's already in the chapter tag)
        if i == 0 and line.startswith('# '):
            i += 1
            continue
        
        # Handle code blocks
        if line.strip().startswith('```'):
            flush_para()
            if not in_code_block:
                # Starting code block
                in_code_block = True
                code_block_content = []
                # Extract language
                match = re.match(r'```\{(\w+)', line.strip())
                if match:
                    code_lang = match.group(1)
                else:
                    match = re.match(r'```(\w+)', line.strip())
                    code_lang = match.group(1) if match else "r"
                i += 1
                continue
            else:
                # Ending code block
                in_code_block = False
                if code_block_content:
                    indent = '          ' + '  ' * subsection_depth
                    result.append(indent + '<program language="{}">'.format(code_lang))
                    result.append(indent + '  <input>')
                    for code_line in code_block_content:
                        result.append(escape_xml(code_line))
                    result.append(indent + '  </input>')
                    result.append(indent + '</program>')
                    result.append('')
                i += 1
                continue
        
        if in_code_block:
            code_block_content.append(line)
            i += 1
            continue
        
        # Handle sections (## headings)
        if line.startswith('## ') and not line.startswith('### '):
            flush_para()
            close_list()
            
            # Close any open subsection
            if subsection_depth > 0:
                result.append('          </subsection>')
                result.append('')
                subsection_depth = 0
            
            # Close previous section if open
            if section_depth > 0:
                result.append('        </section>')
                result.append('')
            
            # Extract title and id
            title_full = line[3:].strip()
            title = re.sub(r' \{#[^\}]+\}', '', title_full)
            
            # Check for explicit id
            id_match = re.search(r'\{#([^\}]+)\}', title_full)
            if id_match:
                xml_id = id_match.group(1)
            else:
                # Generate id from title
                xml_id = 'sec-' + re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
            
            result.append('        <section xml:id="{}">'.format(xml_id))
            result.append('          <title>{}</title>'.format(title))
            result.append('')
            section_depth = 1
            i += 1
            continue
        
        # Handle subsections (### headings)
        if line.startswith('### '):
            flush_para()
            close_list()
            
            # Close previous subsection if open
            if subsection_depth > 0:
                result.append('          </subsection>')
                result.append('')
            
            # Extract title and id
            title_full = line[4:].strip()
            title = re.sub(r' \{#[^\}]+\}', '', title_full)
            
            # Check for explicit id
            id_match = re.search(r'\{#([^\}]+)\}', title_full)
            if id_match:
                xml_id = id_match.group(1)
            else:
                xml_id = 'subsec-' + re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
            
            result.append('          <subsection xml:id="{}">'.format(xml_id))
            result.append('            <title>{}</title>'.format(title))
            result.append('')
            subsection_depth = 1
            i += 1
            continue
        
        # Handle images
        if line.strip().startswith('!['):
            flush_para()
            # Match image with or without attributes
            match = re.match(r'!\[([^\]]*)\]\(([^\)]+)\)(?:\{[^\}]+\})?', line.strip())
            if match:
                img_path = match.group(2)
                # Adjust path if needed - dataviz images should be in dataviz/img/
                if img_path.startswith('img/'):
                    img_path = 'dataviz/' + img_path
                indent = '          ' + '  ' * subsection_depth
                result.append(indent + '<figure>')
                result.append(indent + '  <image source="{}"/>'.format(img_path))
                result.append(indent + '</figure>')
                result.append('')
            i += 1
            continue
        
        # Handle callout blocks and layout blocks
        if line.strip().startswith(':::'):
            if not in_callout:
                flush_para()
                close_list()
                # Check if it's a callout-note or just a layout block
                if 'callout-note' in line:
                    in_callout = True
                    indent = '          ' + '  ' * subsection_depth
                    result.append(indent + '<note>')
                    i += 1
                    # Collect callout content - process it properly
                    callout_buffer = []
                    while i < len(lines) and not lines[i].strip().startswith(':::'):
                        callout_buffer.append(lines[i])
                        i += 1
                    
                    # Process callout content
                    j = 0
                    while j < len(callout_buffer):
                        line_content = callout_buffer[j]
                        
                        # Check for display math
                        if line_content.strip().startswith('$$'):
                            if line_content.strip() == '$$':
                                # Multi-line display math
                                j += 1
                                math_lines = []
                                while j < len(callout_buffer) and not callout_buffer[j].strip().startswith('$$'):
                                    math_lines.append(callout_buffer[j])
                                    j += 1
                                if math_lines:
                                    result.append(indent + '  <me>')
                                    result.append('\n'.join(math_lines))
                                    result.append(indent + '  </me>')
                                j += 1  # Skip closing $$
                                continue
                        
                        # Regular paragraph in callout
                        if line_content.strip():
                            para_text = convert_inline_markdown(line_content.strip())
                            result.append(indent + '  <p>{}</p>'.format(para_text))
                        j += 1
                    
                    result.append(indent + '</note>')
                    result.append('')
                    in_callout = False
                else:
                    # Just skip layout blocks, process content inside normally
                    i += 1
                    continue
            else:
                in_callout = False
            i += 1
            continue
        
        # Handle lists
        list_match = re.match(r'^(\d+)\\\.\s+(.*)$', line)
        if list_match:
            flush_para()
            if not in_list or list_type != 'ol':
                close_list()
                indent = '          ' + '  ' * subsection_depth
                result.append(indent + '<ol>')
                in_list = True
                list_type = 'ol'
            
            item_text = convert_inline_markdown(list_match.group(2))
            indent = '          ' + '  ' * subsection_depth
            result.append(indent + '  <li><p>{}</p></li>'.format(item_text))
            i += 1
            continue
        
        # Handle numbered lists (simple format)
        list_match = re.match(r'^(\d+)\.\s+(.*)$', line)
        if list_match:
            flush_para()
            if not in_list or list_type != 'ol':
                close_list()
                indent = '          ' + '  ' * subsection_depth
                result.append(indent + '<ol>')
                in_list = True
                list_type = 'ol'
            
            item_text = convert_inline_markdown(list_match.group(2))
            indent = '          ' + '  ' * subsection_depth
            result.append(indent + '  <li><p>{}</p></li>'.format(item_text))
            i += 1
            continue
        
        # Handle blockquotes
        if line.strip().startswith('>'):
            flush_para()
            close_list()
            # Remove leading > characters
            quote_text = re.sub(r'^>\s*', '', line.strip())
            quote_text = re.sub(r'^>\s*', '', quote_text)  # Remove nested >
            quote_text = re.sub(r'^>\s*', '', quote_text)  # Remove more nested >
            if quote_text:
                quote_text = convert_inline_markdown(quote_text)
                indent = '          ' + '  ' * subsection_depth
                result.append(indent + '<blockquote>')
                result.append(indent + '  <p>{}</p>'.format(quote_text))
                result.append(indent + '</blockquote>')
                result.append('')
            i += 1
            continue
        
        # Skip footnote definitions
        if re.match(r'^\[\^[^\]]+\]:', line):
            flush_para()
            i += 1
            continue
        
        # Empty line
        if not line.strip():
            flush_para()
            i += 1
            continue
        
        # Handle display math blocks
        if line.strip().startswith('$$'):
            flush_para()
            close_list()
            # Check if it's single-line display math
            if line.strip() == '$$' or (len(line.strip()) > 2 and not line.strip()[2:].strip()):
                # Multi-line display math
                i += 1
                math_lines = []
                while i < len(lines) and not lines[i].strip().startswith('$$'):
                    math_lines.append(lines[i])
                    i += 1
                if math_lines:
                    indent = '          ' + '  ' * subsection_depth
                    result.append(indent + '<me>')
                    result.append('\n'.join(math_lines))
                    result.append(indent + '</me>')
                    result.append('')
                i += 1
                continue
            else:
                # Single-line display math
                math_content = line.strip()[2:-2].strip() if line.strip().endswith('$$') else line.strip()[2:].strip()
                if math_content:
                    indent = '          ' + '  ' * subsection_depth
                    result.append(indent + '<me>')
                    result.append(math_content)
                    result.append(indent + '</me>')
                    result.append('')
                i += 1
                continue
        
        # Regular paragraph line
        if line.strip() and not line.startswith('#'):
            # Check if this continues a list or starts new paragraph
            if not in_list:
                para_buffer.append(line.strip())
            else:
                # If line doesn't start list pattern, close list and start paragraph
                if not re.match(r'^[\d\*\-]', line):
                    close_list()
                    para_buffer.append(line.strip())
        
        i += 1
    
    # Flush any remaining paragraph
    flush_para()
    
    # Close any open list
    close_list()
    
    # Close any open subsection
    if subsection_depth > 0:
        result.append('          </subsection>')
        result.append('')
    
    # Close any open section
    if section_depth > 0:
        result.append('        </section>')
    
    return '\n'.join(result)


if __name__ == '__main__':
    import sys
    import os
    
    try:
        # Define chapters to convert
        chapters = [
            {
                'path': 'dataviz/dataviz-principles.qmd',
                'id': 'ch-data-visualization-principles',
                'title': 'Data visualization principles',
                'output': '/tmp/chapter9.ptx',
                'number': 9
            },
            {
                'path': 'dataviz/dataviz-in-practice.qmd',
                'id': 'ch-data-visualization-in-practice',
                'title': 'Data visualization in practice',
                'output': '/tmp/chapter10.ptx',
                'number': 10
            },
            {
                'path': 'wrangling/dates-and-times.qmd',
                'id': 'ch-parsing-dates-and-times',
                'title': 'Parsing dates and times',
                'output': '/tmp/chapter13.ptx',
                'number': 13
            },
            {
                'path': 'wrangling/locales.qmd',
                'id': 'ch-locales',
                'title': 'Locales',
                'output': '/tmp/chapter14.ptx',
                'number': 14
            },
            {
                'path': 'wrangling/web-scraping.qmd',
                'id': 'ch-extracting-data-from-the-web',
                'title': 'Extracting data from the web',
                'output': '/tmp/chapter15.ptx',
                'number': 15
            }
        ]
        
        # Convert each chapter
        for chapter in chapters:
            # Check if source file exists
            if not os.path.exists(chapter['path']):
                print(f"Error: Source file not found: {chapter['path']}", file=sys.stderr)
                sys.exit(1)
            
            # Read and convert
            try:
                with open(chapter['path'], 'r') as f:
                    content = f.read()
            except IOError as e:
                print(f"Error reading {chapter['path']}: {e}", file=sys.stderr)
                sys.exit(1)
            
            ptx_content = convert_qmd_to_ptx(content, chapter['id'], chapter['title'])
            
            try:
                with open(chapter['output'], 'w') as f:
                    f.write(ptx_content)
            except IOError as e:
                print(f"Error writing {chapter['output']}: {e}", file=sys.stderr)
                sys.exit(1)
            
            print(f"Chapter {chapter['number']} converted, length: {len(ptx_content)}")
        
        print("\nConversion complete!")
        
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
