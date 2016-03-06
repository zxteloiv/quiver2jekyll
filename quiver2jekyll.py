#!/usr/bin/env python2
# coding: utf-8

import sys, argparse

parser = argparse.ArgumentParser(
        description='Turn quiver notes or notebooks to jekyll markdown.')

parser.add_argument('note_path', required=True,
        help='/path/to/quiver/note.'
        'This path can also be quiver notebook(.qvnotebook)')

parser.add_argument('output_path', required=True,
        help='Directory path to save the output jekyll markdown')


