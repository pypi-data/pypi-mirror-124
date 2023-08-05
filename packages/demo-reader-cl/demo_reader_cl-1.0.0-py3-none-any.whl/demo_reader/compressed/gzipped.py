import gzip
from multi_reader.demo_reader.util import writer

opener=gzip.open

if __name__=='__main__':
    writer.main(opener)