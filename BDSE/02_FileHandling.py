# https://code.visualstudio.com/docs/python/python-tutorial

# python -m pip install
# python -m pip uninstall ***

## what if anyating seems wrong?
# https://www.codewrecks.com/post/general/pip-and-python-in-vscode/python


import awscli

import os
import pandas as pd
import numpy as np



# dname = r''
# os.chdir(dname)

full_path = os.path.realpath('iris.csv')
print(full_path + "\n")


print("Path at terminal when executing this file")
print(os.getcwd() + "\n")

dfiris = pd.read_csv('iris.csv')
dfiris






