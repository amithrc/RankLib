'''
@Author Amith RC
@Created April 7th 2019
@Purpose: Takes the feature file and perform the Zscale normalize
'''

import ranklib as rlib
import argparse
import sys
import os


def read_dir_list(dirpath):
    return [os.path.abspath(name) for name in os.listdir(dirpath)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Takes unnormalized feature file and performs the normalization")
    parser.add_argument("-q", "--qrelpath", help="Path to the Qrel file", required=True)
    parser.add_argument("-f", "--dirpath", help="Path to the Feature file", required=True)
    parser.add_argument("-v", "--verbose", help="Display information on the stdout", action="store_true")
    parser.add_argument("-s", "--suffix", help="Pass a filename suffix")
    parser.add_argument("-r", "--ranklib", help="Path to the RankLib jar")
    parser.add_argument("-n", "--normalizer", help="Perform Z score normalize on the data", action="store_true")

    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    qrel = None
    dirlist = None
    number_of_fet = 0

    if args.qrelpath:
        qrel = rlib.readQrel(args.qrelpath)

    for dir in read_dir_list(args.dirpath):
        runFiles = rlib.getFileList(dir)
        ranker = rlib.create_dictionary(runFiles)
        print(dir)
        print(os.path.basename(dir))


