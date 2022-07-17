import ROOT
import sys
import os
sys.path.append('/afs/cern.ch/work/c/chenguan/private/pycommontool/')
from FileSystemClass import *
from PlotClass import *
dirs = DirTree()
dirs.mkrootdir('test_eemass')
path = dirs.root

os.system('cp *png ' + path + '/' )
