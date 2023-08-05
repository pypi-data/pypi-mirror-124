import os

from multi_reader.demo_reader.compressed import *

extension_map={
    '.bz2':bz2_opener,
    '.gzip':gzip_opener
}



class MultiReader:
    def __init__(self,filename):
        extension=os.path.splitext(filename)[1]
        opener=extension_map.get(extension,open)
        self.f=opener(filename,'rt')

    def close(self):
        self.f.close()

    def read(self):
        return self.f.read()



