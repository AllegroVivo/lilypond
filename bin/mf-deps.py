#!@PYTHON@

"""look into metafont source for dependencies.

 fixme: python path
 fixme: error reporting
 fixem: python sucks slightly: why doesn't it have closures?

"""

from regex import * ;
from regsub import * ;
import sys;
import os;

input_re = compile('^[ \t]*input *\([^;]+\);')
postfixes = ['log', 'dvi', '2602gf', 'tfm']


def print_one(x):
    print x

def line_concat(x,y):
    return x + '\n' +  y

class Targetdeps:
    """Dependencies for one toplevel sourcefile

    """
    
    def __init__(self,nm):
	split = os.path.splitext(nm)	
	self.basename=split[0];
	self.depfiles = []
	self.checkdep(nm)
	
    def checkdep(self, name):
	split = os.path.splitext(name)
	name = split[0] + '.mf';

	if name not in self.depfiles:
	    self.get_filedeps(name)

    def get_filedeps(self,filename):
#	print sys.stderr.write( 'checking ' + filename + '\n');
	try:
	    file = open(filename)
	except IOError:
#	    print sys.stderr.write( 'can\'t open ' + filename + '\n')
	    return

	self.depfiles.append(filename)
	lines = file.readlines()
	file.close()
	for line in lines:
	    if input_re.search (line) <> -1:
		self.checkdep( input_re.group(1))

    def target_string(self):
	# ugh.  Closures, anyone?
	targets =  map (lambda x,y = self.basename: 'out/' + y + '.' + x, postfixes)
	depstring = reduce(lambda x,y: x + ' ' + y, self.depfiles) 
	dependencies = map (lambda x, y=depstring: x + ': ' + y, targets)

	return reduce(line_concat, dependencies)



for file in sys.argv[1:]: # skip programname
    t = Targetdeps(file)
    print t.target_string()


