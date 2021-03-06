#!/usr/bin/env python2
# coding: utf-8

import os, argparse, json, re, sys
import distutils
from distutils import dir_util

PY3 = sys.version_info >= (3,)

parser = argparse.ArgumentParser(
        description='Turn quiver notes or notebooks to jekyll markdown.')

parser.add_argument('in_path',
        help='/path/to/quiver/note.'
        'This path can also be quiver notebook(.qvnotebook).')

parser.add_argument('out_path',
        help='Directory path to save the output jekyll markdown.')

parser.add_argument('--title', type=lambda x: x if PY3 else unicode(x, 'utf-8'),
        help='Overwrite the title in note or notebook, '
        'which will be used as directory name.')

def load_jekyll_page_tpl(filename=None):
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),
        u'template.md') if filename is None else filename
    with open(filename, 'r') as f:
        data = f.read()
    return data if PY3 else data.decode('utf-8')

def note_to_md(meta, content):
    """ To produce note representation in markdown """
    title = make_valid_title_path(meta[u'title'], is_path=False)
    tpl = load_jekyll_page_tpl()

    tmpdata = u''
    for c in content[u'cells']:
        if c['type'] == 'text':
            tmpdata += (u'\n<div>' +
                    re.sub('quiver-image-url', u'resources', c['data'])
                    + u'</div>\n')
        elif c['type'] == 'markdown':
            tmpdata += u'\n' + re.sub('quiver-image-url', u'resources', c['data']) + u'\n'
        elif c['type'] == 'code':
            tmpdata += u'\n~~~ ' + c['language'] + u'\n' + c['data'] + u'\n~~~\n'
        elif c['type'] == 'latex':
            tmpdata += u'\n$$\n' + c['data'] + '\n$$\n'
        else:
            tmpdata += u'\n' + c['data'] + u'\n'

    jekyllmd = tpl.format(title=title, content=tmpdata)
    return jekyllmd

def make_valid_title_path(title, is_path=True):
    """
    Make valid title or path.
    Substitute with space for title, whereas underscore for path.
    """
    title = re.sub(u'[-/: &]+', u'_' if is_path else u' '
            , title).strip()
    if not title:
        title = u"Empty_Title"
    return title

def export_note(in_path, out_path, title=None):
    meta = json.loads(open(os.path.join(in_path, u'meta.json'), 'r').read())
    content = json.loads(open(os.path.join(in_path, u'content.json'), 'r').read())

    jekyllmd = note_to_md(meta, content)

    # make dir for the note
    title = title if title is not None else meta[u'title']
    md_dir = os.path.join(out_path, make_valid_title_path(title))
    if not os.path.exists(md_dir):
        os.mkdir(md_dir)

    # write note content in markdown
    with open(os.path.join(md_dir, 'index.md'), 'wb') as f:
        f.write(jekyllmd.encode('utf-8'))

    # copy resources for that note
    res_dir = os.path.join(in_path, 'resources')
    if os.path.exists(res_dir):
        distutils.dir_util.copy_tree(res_dir, os.path.join(md_dir, 'resources'))

    return title

def export_notebook(in_path, out_path, title=None):
    meta = json.loads(open(os.path.join(in_path, u'meta.json'), 'r').read())
    title = meta[u'name'] if title is None else title

    in_path = os.path.expanduser(in_path)
    out_path = os.path.expanduser(out_path)

    # make output dir for the whole notebook
    notebook_path = os.path.join(out_path, make_valid_title_path(title))
    if not os.path.exists(notebook_path):
        os.mkdir(notebook_path)

    # find each note inside the notebook, export each one
    # build the index.md for notebook dir, too
    note_titles = []
    for note_dir in (x for x in os.listdir(in_path) if 'qvnote' in x):
        note_title = export_note(os.path.join(in_path, note_dir), notebook_path)
        note_titles.append(note_title)

    # when exporting a notebook, note title are used as relative path
    nb_content = u"\n\n".join(u"[{0}]({0})".format(make_valid_title_path(title))
           for title in sorted(note_titles))

    # write notebook index.md
    tpl = load_jekyll_page_tpl()
    note_index = tpl.format(title=title, content=nb_content)

    with open(os.path.join(notebook_path, 'index.md'), 'wb') as f:
        f.write(note_index.encode('utf-8'))

    return title

def main(args):
    pathlist = os.path.normpath(args.in_path).split(os.sep)
    # since qvnote is a substring of qvnotebook, check qvnotebook first
    if 'qvnotebook' in pathlist[-1]:
        export_notebook(args.in_path, args.out_path, args.title)
    elif 'qvnote' in pathlist[-1]:
        export_note(args.in_path, args.out_path, args.title)
    else:
        pass

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)

