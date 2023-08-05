import sys

from multi_reader.demo_reader.multireader import MultiReader


filename=sys.argv[1]
r=MultiReader(filename)
print(r.read())
r.close()

