#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess as sp
from pathlib import Path as p
from time import sleep as sl

# install tools
cmd = "pip install sphinx commonmark recommonmark sphinx-markdown-tables sphinx_rtd_theme"
ret = sp.call(cmd)
# print(ret)

p_cur = p(".").absolute()
name_dir = "spdir"

p(name_dir).mkdir()
p_prj = p_cur / p(name_dir)
os.chdir(p_prj)

cmd = 'sphinx-quickstart -q -p "tprj" -a author_name -v 1.0 -l ja prj --sep'
ret = sp.call(cmd)

