import argparse
import sys
import pandas as pd
import os
from scipy import stats
import numpy as np


def has(qrels, qid, pid):
    if qrels.get(qid) is None:
        return False
    else:
        paraList = qrels.get(qid)
        if pid in paraList:
            return True
        else:
            return False


'''
Reads all the files in run files directory and put it in Dict
dict<QID,dict<PID,[0.0 0.0 0.0 ...]>
'''


def create_dictionary(runFile):
    ranker = dict()
    number_of_feature = len(runFiles)
    current_feature_number = 0

    for run in runFiles:
        with open(run, 'r') as f:
            for line in f:
                data = line.split(" ")
                qid = data[0]
                pid = data[2]
                score = data[4]
                if qid in ranker:
                    paravalue = ranker.get(qid)
                    if pid in paravalue:
                        paravalue.get(pid).insert(current_feature_number,score)
                    else:
                        scorelist = [0.0 for x in range(0, number_of_feature)]
                        scorelist.insert(current_feature_number, score)
                        paravalue[pid]=scorelist
                else:
                    scorelist = [0.0 for x in range(0, number_of_feature)]
                    scorelist.insert(current_feature_number,score)
                    inner = dict()
                    inner[pid] = scorelist
                    ranker[qid]= inner

        current_feature_number = current_feature_number + 1


def displayQrel(Qrel):
    for key, value in Qrel.items():
        for para in value:
            print(key, para)


def readQrel(qrelpath):
    Qrel = dict()
    with open(qrelpath, 'r') as qrel:
        for line in qrel:
            data = line.split(" ")
            key = data[0]
            value = data[2]
            if Qrel.get(key) is None:
                para_list = []
                para_list.append(value)
                Qrel[key] = para_list
            else:
                Qrel.get(key).append(value)

    return Qrel


def displayFile(fileList):
    for file in fileList:
        print(file)


def createFrame():
    col = ['rel', 'qid', 'pid']

    for i in range(0, 10):
        col.append("fet" + str(i + 1))

    rankLIB = pd.DataFrame(columns=col)
    print(rankLIB)


'''
Read the file names in to list
'''


def getFileList(path):
    return [os.path.join(path, file) for file in os.listdir(path)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser("RankLib File Formatter")
    parser.add_argument("-q", "--qrelpath", help="Path to the Qrel file", required=True)
    parser.add_argument("-d", "--dirpath", help="Path to the Qrel file", required=True)
    parser.add_argument("-v", "--verbose", help="Display information on the stdout", action="store_true")
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    Qrel = None
    runFiles = None

    if args.qrelpath:
        Qrel = readQrel(args.qrelpath)

    if args.dirpath:
        runFiles = getFileList(args.dirpath)

    if args.verbose:
        displayQrel(Qrel)
        displayFile(runFiles)

    create_dictionary(runFiles)
