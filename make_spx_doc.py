#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import textwrap
import shutil
import subprocess
import json
from pathlib import Path as p
from distutils import dir_util as du


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
    return [x.relative_to(search_path)
            for x in search_path.iterdir()
            if x.is_dir()]


def listup_docsrc(search_path):
    return [x.relative_to(search_path)
            for x in search_path.iterdir()
            if (x.is_file() and (str(x).endswith(".md")) or (str(x).endswith(".rst")))]


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

    idx_name = p(idx_name)
    path_idx = path_tgt / idx_name

    with open(path_idx, 'w', encoding="utf-8") as f:
        f.write(index_body)

    # recursive
    for dr in list_dir:
        print(p().cwd())
        print(dr)
        generate_spx_layer(path_tgt / dr)


def update_spx_source(src=""):
    """Move a file tree to sphinx source. Old sources are deleted.
    """

    # delete old spx_prj source
    p_spxsrc = p(spx_src_dir)
    if p_spxsrc.is_dir():
        shutil.rmtree(p_spxsrc)
    p_spxsrc.mkdir()

    # prepare new spx_prj source dir
    p_spxsrc_org = p(str(p_spxsrc) + "_org")
    list_src = p_spxsrc_org.glob("**/*")
    _listprint(list_src)
    du.copy_tree(str(p_spxsrc_org), str(p_spxsrc))

    # copy doc source
    list_src = src.glob("**/*")
    _listprint(list_src)

    du.copy_tree(str(src), str(p_spxsrc))


def execute_spx():
    path_spx = p(spx_prj_dir)
    os.chdir(path_spx)
    print(p().cwd())

    path_build = path_spx / p("build")
    if path_build.exists():
        shutil.rmtree(path_build)

    cmd = "make.bat html"
    subprocess.call(cmd)


def main():

    path_doc_src = p("./spx_source")

    # make temporaly workspace
    path_tmp_ws = str(path_doc_src) + "_"
    path_tmp_ws = p(path_tmp_ws)
    print(path_tmp_ws)
    if path_tmp_ws.exists():
        shutil.rmtree(path_tmp_ws)
    shutil.copytree(path_doc_src, path_tmp_ws)

    generate_spx_layer(path_tmp_ws, if_top=True)

    update_spx_source(path_tmp_ws)

    execute_spx()


if __name__ == '__main__':

    main()
