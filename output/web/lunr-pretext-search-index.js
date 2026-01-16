var ptx_lunr_search_style = "textbook";
var ptx_lunr_docs = [
{
  "id": "preface",
  "level": "1",
  "url": "preface.html",
  "type": "Preface",
  "number": "",
  "title": "Preface",
  "body": " Preface  Content will be added here.  "
},
{
  "id": "introduction",
  "level": "1",
  "url": "introduction.html",
  "type": "Chapter",
  "number": "1",
  "title": "Introduction",
  "body": " Introduction  Content will be added here.  "
},
{
  "id": "ch-getting-started",
  "level": "1",
  "url": "ch-getting-started.html",
  "type": "Chapter",
  "number": "2",
  "title": "Getting started",
  "body": " Getting started  Content will be added here.  "
},
{
  "id": "ch-r-basics",
  "level": "1",
  "url": "ch-r-basics.html",
  "type": "Chapter",
  "number": "3",
  "title": "R basics",
  "body": " R basics  Content will be added here.  "
},
{
  "id": "ch-programming-basics",
  "level": "1",
  "url": "ch-programming-basics.html",
  "type": "Chapter",
  "number": "4",
  "title": "Programming basics",
  "body": " Programming basics  Content will be added here.  "
},
{
  "id": "ch-tidyverse",
  "level": "1",
  "url": "ch-tidyverse.html",
  "type": "Chapter",
  "number": "5",
  "title": "The tidyverse",
  "body": " The tidyverse  Content will be added here.  "
},
{
  "id": "ch-data-table",
  "level": "1",
  "url": "ch-data-table.html",
  "type": "Chapter",
  "number": "6",
  "title": "data.table",
  "body": " data.table  Content will be added here.  "
},
{
  "id": "ch-importing-data",
  "level": "1",
  "url": "ch-importing-data.html",
  "type": "Chapter",
  "number": "7",
  "title": "Importing data",
  "body": " Importing data  Content will be added here.  "
},
{
  "id": "ch-visualizing-data-distributions",
  "level": "1",
  "url": "ch-visualizing-data-distributions.html",
  "type": "Chapter",
  "number": "8",
  "title": "Visualizing data distributions",
  "body": " Visualizing data distributions  Content will be added here.  "
},
{
  "id": "ch-ggplot2",
  "level": "1",
  "url": "ch-ggplot2.html",
  "type": "Chapter",
  "number": "9",
  "title": "ggplot2",
  "body": " ggplot2  Content will be added here.  "
},
{
  "id": "ch-data-visualization-principles",
  "level": "1",
  "url": "ch-data-visualization-principles.html",
  "type": "Chapter",
  "number": "10",
  "title": "Data visualization principles",
  "body": " Data visualization principles  Content will be added here.  "
},
{
  "id": "ch-data-visualization-in-practice",
  "level": "1",
  "url": "ch-data-visualization-in-practice.html",
  "type": "Chapter",
  "number": "11",
  "title": "Data visualization in practice",
  "body": " Data visualization in practice  Content will be added here.  "
},
{
  "id": "ch-reshaping-data",
  "level": "1",
  "url": "ch-reshaping-data.html",
  "type": "Chapter",
  "number": "12",
  "title": "Reshaping data",
  "body": " Reshaping data  Content will be added here.  "
},
{
  "id": "ch-joining-tables",
  "level": "1",
  "url": "ch-joining-tables.html",
  "type": "Chapter",
  "number": "13",
  "title": "Joining tables",
  "body": " Joining tables  Content will be added here.  "
},
{
  "id": "ch-parsing-dates-and-times",
  "level": "1",
  "url": "ch-parsing-dates-and-times.html",
  "type": "Chapter",
  "number": "14",
  "title": "Parsing dates and times",
  "body": " Parsing dates and times  Content will be added here.  "
},
{
  "id": "ch-locales",
  "level": "1",
  "url": "ch-locales.html",
  "type": "Chapter",
  "number": "15",
  "title": "Locales",
  "body": " Locales  Content will be added here.  "
},
{
  "id": "ch-extracting-data-from-the-web",
  "level": "1",
  "url": "ch-extracting-data-from-the-web.html",
  "type": "Chapter",
  "number": "16",
  "title": "Extracting data from the web",
  "body": " Extracting data from the web  Content will be added here.  "
},
{
  "id": "ch-string-processing",
  "level": "1",
  "url": "ch-string-processing.html",
  "type": "Chapter",
  "number": "17",
  "title": "String processing",
  "body": " String processing  Content will be added here.  "
},
{
  "id": "ch-text-analysis",
  "level": "1",
  "url": "ch-text-analysis.html",
  "type": "Chapter",
  "number": "18",
  "title": "Text analysis",
  "body": " Text analysis  Content will be added here.  "
},
{
  "id": "ch-organizing-with-unix",
  "level": "1",
  "url": "ch-organizing-with-unix.html",
  "type": "Chapter",
  "number": "19",
  "title": "Organizing with Unix",
  "body": " Organizing with Unix  Content will be added here.  "
},
{
  "id": "ch-git-and-github",
  "level": "1",
  "url": "ch-git-and-github.html",
  "type": "Chapter",
  "number": "20",
  "title": "Git and GitHub",
  "body": " Git and GitHub  Content will be added here.  "
},
{
  "id": "ch-reproducible-projects",
  "level": "1",
  "url": "ch-reproducible-projects.html",
  "type": "Chapter",
  "number": "21",
  "title": "Reproducible projects",
  "body": " Reproducible projects  Content will be added here.  "
}
]

var ptx_lunr_idx = lunr(function () {
  this.ref('id')
  this.field('title')
  this.field('body')
  this.metadataWhitelist = ['position']

  ptx_lunr_docs.forEach(function (doc) {
    this.add(doc)
  }, this)
})
