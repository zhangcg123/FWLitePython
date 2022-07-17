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


df = pd.read_json('aod_Zee.json',orient='index')



myhtml = HTMLClass('Z to ee info for electron track study')
myhtml.section('')
string = myhtml.check()

string = string + '\n' + df.to_html()
fp = open(path + '/test.html','w')
fp.write(string)
fp.close()
