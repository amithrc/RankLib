'''
@Author Amith RC
@Created March 29th 2019
@Purpose: Takes the feature file and perform the Zscale normalize
'''

import ranklib as rlib
import argparse
import sys


def read_feature_file(filepath):
    fetdict = dict()
    number_of_fet = 0
    with open(filepath, 'r') as f:
        for line in f:
            qid, pid = rlib.get_qid_pid(line)
            score = []
            match = rlib.fetextract.findall(line)
            count = 0
            if match is not None:
                count = count + 1
                for val in match:
                    count = count + 1
                    score.append(float(val.split(":")[1]))
            number_of_fet = count

            if qid in fetdict:
                pass
            else:
                pass
    return fetdict


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Takes unnormalized feature file and performs the normalization")
    parser.add_argument("-q", "--qrelpath", help="Path to the Qrel file", required=True)
    parser.add_argument("-f", "--fetpath", help="Path to the Feature file", required=True)
    parser.add_argument("-v", "--verbose", help="Display information on the stdout", action="store_true")
    parser.add_argument("-s", "--suffix", help="Pass a filename suffix")
    parser.add_argument("-r", "--ranklib", help="Path to the RankLib jar")
    parser.add_argument("-n", "--normalizer", help="Perform Z score normalize on the data", action="store_true")

    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    qrel = None
    fet = None
    if args.normalizer:
        fet = read_feature_file(args.fetpath)
        qrel = rlib.readQrel(args.qrelpath)
