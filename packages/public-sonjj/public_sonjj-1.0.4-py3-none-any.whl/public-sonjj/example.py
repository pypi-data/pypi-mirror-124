from m2r import parse_from_file
import os
output = parse_from_file(os.path.abspath(os.curdir)+'\README.md')

f = open(os.path.abspath(os.curdir)+'\index.rst', "w")
f.write(output)
f.close()