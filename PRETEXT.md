# PreText Textbook Structure

This repository contains a PreText version of "Introduction to Data Science".

## Structure

The PreText textbook follows the same structure as the Quarto files in the main repository:

- **Title**: Introduction to Data Science
- **Preface**: Introductory material
- **Introduction**: Overview of the book

### Part 1: R (Chapters 1-6)
1. Getting started
2. R basics
3. Programming basics
4. The tidyverse
5. data.table
6. Importing data

### Part 2: Data Visualization (Chapters 7-10)
7. Visualizing data distributions
8. ggplot2
9. Data visualization principles
10. Data visualization in practice

### Part 3: Data Wrangling (Chapters 11-17)
11. Reshaping data
12. Joining tables
13. Parsing dates and times
14. Locales
15. Extracting data from the web
16. String processing
17. Text analysis

### Part 4: Productivity Tools (Chapters 18-20)
18. Organizing with Unix
19. Git and GitHub
20. Reproducible projects

## Files

- `source/main.ptx` - Main PreText book file with complete structure
- `project.ptx` - Project configuration file
- `publication/publication.ptx` - Publication settings
- `requirements.txt` - Python dependencies (PreTeXt 2.36.0)

## Building the Book

To build this PreText book, you need to have PreText CLI installed. Install dependencies first:

```bash
pip install -r requirements.txt
```

Then build the book:

```bash
pretext build web
```

For PDF output:
```bash
pretext build print
```

The output will be generated in the `output/` directory.

## Notes

This is a skeleton structure. Content placeholders have been added to each chapter and can be filled in as needed.
