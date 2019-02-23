import argparse
import sys
import pandas as pd
import os


def has(qrels, qid, pid):
    if qrels.get(qid) is None:
        return False
    else:
        paraList = qrels.get(qid)
        if pid in paraList:
            return True
        else:
            return False


def createDictionary(Qrels, runFile):
    number_of_feature = len(runFiles)
    current_feature_number = 0

    for run in runFiles:
        with open(run, 'r') as f:
            for line in f:
                print(line)

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

def readFileList(path):
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
        runFiles = readFileList(args.dirpath)

    if args.verbose:
        displayQrel(Qrel)
        displayFile(runFiles)

createDictionary(Qrel, runFiles)
