#!/usr/bin/env python2
# coding: utf-8

import os, argparse, json, re
import distutils
from distutils import dir_util

parser = argparse.ArgumentParser(
        description='Turn quiver notes or notebooks to jekyll markdown.')

parser.add_argument('in_path',
        help='/path/to/quiver/note.'
        'This path can also be quiver notebook(.qvnotebook).')

parser.add_argument('out_path',
        help='Directory path to save the output jekyll markdown.')

parser.add_argument('--title', type=lambda x: unicode(x, 'utf-8'),
        help='Overwrite the title in note or notebook, '
        'which will be used as directory name.')

def note_to_md(meta, content):
    """ To produce note representation in markdown """
    title = meta[u'title']
    tpl = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
        u'template.md'), 'r').read()

    tmpdata = u''
    for c in content[u'cells']:
        if c['type'] == 'text':
            tmpdata += (u'\n<div>' +
                    re.sub('quiver-image-url', u'resources', c['data'])
                    + u'</div>\n')
        elif c['type'] == 'markdown':
            tmpdata += u'\n' + c['data'] + u'\n'
        elif c['type'] == 'code':
            tmpdata += u'\n~~~ ' + c['language'] + u'\n' + c['data'] + u'\n~~~\n'
        elif c['type'] == 'latex':
            tmpdata += u'\n$$\n' + c['data'] + '\n$$\n'
        else:
            tmpdata += u'\n' + c['data'] + u'\n'

    jekyllmd = tpl.format(title=title.encode('utf-8'),
            content=tmpdata.encode('utf-8'))
    return jekyllmd

def export_note(in_path, out_path, title=None):
    meta = json.loads(open(os.path.join(in_path, u'meta.json'), 'r').read())
    content = json.loads(open(os.path.join(in_path, u'content.json'), 'r').read())

    jekyllmd = note_to_md(meta, content)

    # make dir for the note
    title = title if title is not None else meta[u'title']
    md_dir = os.path.join(out_path, title.replace(u'/', u':'))
    if not os.path.exists(md_dir):
        os.mkdir(md_dir)

    # write note content in markdown
    with open(os.path.join(md_dir, 'index.md'), 'w') as f:
        f.write(jekyllmd)

    # copy resources for that note
    res_dir = os.path.join(in_path, 'resources')
    if os.path.exists(res_dir):
        distutils.dir_util.copy_tree(res_dir, os.path.join(md_dir, 'resources'))

def export_notebook(in_path, out_path, title=None):
    meta = json.loads(open(os.path.join(in_path, u'meta.json'), 'r').read())
    title = meta[u'title'] if title is None else title

    in_path = os.path.expanduser(in_path)
    out_path = os.path.expanduser(out_path)

    # make output dir for the whole notebook
    notebook_path = os.path.join(out_path, title.replace(u'/', u':'))
    if not os.path.exists(notebook_path):
        os.mkdir(notebook_path)

    # find each note inside the notebook, export each one
    for note_in_path in (x for x in os.listdir(in_path) if 'qvnote' in x):
        export_note(os.path.join(in_path, note_in_path), notebook_path)

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

