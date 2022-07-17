import ROOT
import sys
import os
import json
import pandas as pd
sys.path.append('/afs/cern.ch/work/c/chenguan/private/pycommontool/')
from FileSystemClass import *
from HTMLClass import *

dirs = DirTree()
dirs.mkrootdir('test_'+os.getcwd().split('/')[-1])
path = dirs.root

# load json to pandas dataframe
df = pd.read_json('miniaod_Zee.json',orient='index')

# custom columns order
colstmp = []
with open('columns.txt','r') as colsf:
	for l in colsf:
		colstmp.append(l.strip())
df = df[colstmp]

# custom index order
# custom by index. sort_index returns the index order as 0,1,10,100,1000.... do not konw why. if you want 1,2,3..., as following two lines.
#indextmp = [i for i in range(0,len(df.index))]
#df.index = indextmp

# custom index by columns values, by lumiblock and eventNum here.
df.sort_values(by=['LumiBlock','eventNum'],inplace=True)

myhtml = HTMLClass('Z to ee info for electron track study')
myhtml.section('')
string = myhtml.check()

string = string + '\n' + df.to_html()
fp = open(path + '/test.html','w')
fp.write(string)
fp.close()
