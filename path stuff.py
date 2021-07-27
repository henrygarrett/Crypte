# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 18:23:57 2021

@author: madma
"""
# import os
# path1 = os.path.join(os.path.curdir, 'file.name')
# path2 = os.path.dirname(os.path.curdir)
# print(path2)
# print(path1)
import os
cwd = os.getcwd()
print(cwd)


from pathlib import Path
p = Path.cwd()
#with q.open() as f: f.readline()
print(p)
p = p.parents[1]
print(p)