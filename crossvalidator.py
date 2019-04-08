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
    return [os.path.join(dirpath, name) for name in os.listdir(dirpath)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Takes unnormalized feature file and performs the normalization")
    parser.add_argument("-q", "--qrelpath", help="Path to the Qrel file", required=True)
    parser.add_argument("-d", "--dirpath", help="Path to the Feature file", required=True)
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
        print(dir)
        print("Working on directory {}".format(dir))
        runFiles = rlib.getFileList(dir)
        print(runFiles, len(runFiles))
        ranker = rlib.create_dictionary(runFiles)

        fname = ""
        if args.suffix:
            fname = args.suffix + ".txt"
        else:
            fname = os.path.basename(dir) + "-feature.txt"

        print("Filename = " + fname)

        if args.normalizer:
            rowlist = rlib.convert_dict_to_list(ranker, qrel)
            df = rlib.create_data_frame(rowlist, len(runFiles))
            rlib.normalize_data_frame(df, len(runFiles))
            if (args.verbose):
                print(df.head())
            rlib.write_feature_file_normalized(df, len(runFiles), fname)
        else:
            rlib.write_feature_file_unnormalized(qrel, ranker, fname)

        if args.ranklib:
            rlib.run_rank_lib(args.ranklib, fname)
            out = rlib.get_combined_run_dict("model.txt", fname)
            rlib.create_combined_run_file(out)
