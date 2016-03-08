# quiver2jekyll
Export Quiver notes and notebooks into jekyll pages.

[Quiver](http://happenapps.com/#quiver) is an excellent markdown notebook on Mac OS X and stays in active development with a kind programmer.

This tool helps you to export either a Quiver note or Quiver notebook into several Jekyll Pages, which make you publish your Quiver notes to Jekyll blogs easily.  
Quiver GUI itself has provided the functionality to export notes but only in rendered html files. This has some limitations.

To convert notes into Jekyll markdown, you will benefit from several merits:

- Better javascript plugin support from Jekyll, e.g., choose between MathJax or KaTeX as you like
- Consistent css style with your Jekyll blogs
- Better effect to render mathematic formula as it's rendered at the runtime
- Host your blog freely on GitHub Pages

Also you have some new limitations.

- Markdown in Quiver is restricted to Kramdown syntax only, although Quiver support many dialects of markdown. Otherwise GitHub Pages will note render your note correctly.
- Maybe in the future Quiver will have more cell types or richer format in cells types it already has. Exporting tools may bring the risk to delay.

### Usage

It supports to export both a Quiver notebook or simply a Quiver note, which is determined automatically by the folder extension (_.qvnote_ or _.qvnotebook_).

The exporter will map the notes and directories as below:

- Quiver Notebook -> Output notebook directory
- Quiver Note -> Output note directory
- Resources (mainly images) -> Output inside the corresponding note directory

You can specify a title argument for the very notebook (notes inside not included in this case) or the very note direcory, which will overwrite the title you use in Quiver. Otherwise, the title you use in Quiver will be used as the output directory name. While you can only specify a title for the top layer directory, the titles of notes inside will continue to serve as the directory name for every note.

If you put the output folder inside the jekyll blog, as they are all jekyll pages, the url path may contain spaces or special characters if you use them in the note title or notebook title.

You can use the following to export, though:

~~~ bash
python quiver2jekyll.py ~/Nutstore/Quiver\ Tutorial.qvnotebook/ tmp/ --title test
~~~

which export the Quiver Tutorial notebook into the _tmp_ directory using a directory name "test". Exporting a note is similar and left out.

### License

The Star And Thank Author License (SATA)
