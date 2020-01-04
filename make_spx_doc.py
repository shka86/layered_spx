#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import pathlib
import textwrap
import shutil
import subprocess
import json

with open("pathdefine.json", 'r', encoding='utf-8') as f:
    d = json.load(f)

spx_prj_dir = d["spx_prj_dir"]
spx_src_dir = d["spx_src_dir"]

def _listprint(lists):
    """for debug
    """
    for x in lists:
        print(x)


def listup_dir(search_path):
    return [p.relative_to(search_path)
            for p in search_path.iterdir()
            if p.is_dir()]


def listup_docsrc(search_path):
    return [p.relative_to(search_path)
            for p in search_path.iterdir()
            if (p.is_file() and (str(p).endswith(".md")) or (str(p).endswith(".rst")))]


def generate_toc(toc_title, tocs):
    body = textwrap.dedent('''
        ###toc_title###
        ====================================

        .. toctree::
           :maxdepth: 2
           :caption: Contents:

        ###list_doc###

    ''')

    body = body.replace("###toc_title###", toc_title)
    body = body.replace("###list_doc###", tocs)

    return body


def generate_spx_layer(path_tgt, if_top=False):
    """Construct sphinx-ready file tree.
    """
    # listup dirs and files
    list_dir = listup_dir(path_tgt)
    list_file = listup_docsrc(path_tgt)

    tocs = ""
    for dr in list_dir:
        line = str(dr) + "/" + str(dr) + ".rst\n"
        tocs += "   " + line
    for f in list_file:
        line = str(f) + "\n"
        tocs += "   " + line

    toc_title = path_tgt.stem
    index_body = generate_toc(toc_title, tocs)

    if if_top:
        idx_name = "index.rst"
    else:
        idx_name = str(path_tgt.stem) + ".rst"

    idx_name = pathlib.Path(idx_name)
    path_idx = path_tgt / idx_name

    with open(path_idx, 'w', encoding="utf-8") as f:
        f.write(index_body)

    # recursive
    for dr in list_dir:
        print(pathlib.Path().cwd())
        print(dr)
        generate_spx_layer(path_tgt / dr)


def update_spx_source(src=""):
    """Move a file tree to sphinx source. Old sources are deleted.
    """

    # copy source
    list_src = src.glob("**/*")
    _listprint(list_src)

    # copy destination
    dst = spx_src_dir
    dst = pathlib.Path(dst)

    if dst.exists():
        shutil.rmtree(dst)

    shutil.copytree(src, dst)


def execute_spx():
    path_spx = pathlib.Path(spx_prj_dir)
    os.chdir(path_spx)
    print(pathlib.Path().cwd())

    cmd = "make.bat html"
    subprocess.Popen(cmd)


def main():

    path_doc_src = pathlib.Path("./spx_source")

    # make temporaly workspace
    path_tmp_ws = str(path_doc_src) + "_"
    path_tmp_ws = pathlib.Path(path_tmp_ws)
    print(path_tmp_ws)
    if path_tmp_ws.exists():
        shutil.rmtree(path_tmp_ws)
    shutil.copytree(path_doc_src, path_tmp_ws)

    generate_spx_layer(path_tmp_ws, if_top=True)

    update_spx_source(path_tmp_ws)

    execute_spx()


if __name__ == '__main__':

    main()
