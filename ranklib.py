'''
@Author Amith RC
@Created March 24th 2019
@Purpose: Creates the Ranklib feature file using the Run file (TREC car format)
'''
import argparse
import sys
import pandas as pd
import os
import numpy as np
from scipy.stats import zscore
verbose = False


def is_relevant(qrel, qid, pid):
    if qid in qrel:
        para = qrel.get(qid)
        if pid in para:
            return 1
        else:
            return 0
    else:
        return 0


'''
Write to the feature file format, write the feature file from the ranker dict
Append the qid_pid as info
We can use this to combine the rank files
'''


def write_feature_file_unnormalized(qrel, ranker, fname_suffix):
    fname = fname_suffix + ".txt"
    print("Creating the feature file in the PWD {}".format(fname))
    with open(fname, 'w') as fw:
        qid_counter = 1
        pcount = 0
        for qid, paradict in ranker.items():
            pcount = pcount + 1
            if (pcount % 50 == 0):
                print("\n")
            else:
                print(".", end=" ")
            for pid, score in paradict.items():
                is_rel = is_relevant(qrel, qid, pid)
                qid_val = "qid:{}".format(qid_counter)
                sb = ""
                c = 1
                for score_val in score:
                    sb += str(c) + ":" + str(score_val)
                    sb += " "
                    c = c + 1
                info = "#" + qid + "_" + pid
                line = str(is_rel) + " " + qid_val + " " + sb + " " + info + "\n"
                if verbose:
                    print(line)
                fw.write(line)
            qid_counter = qid_counter + 1


'''
Reads all the files in run files directory and put it in Dict
dict<QID,dict<PID,[0.0 0.0 0.0 ...]>
'''


def create_dictionary(runFile):
    ranker = dict()
    number_of_feature = len(runFiles)
    current_feature_number = 0

    for run in runFiles:
        print("Working on file {}".format(run))
        with open(run, 'r') as f:
            for line in f:
                data = line.split(" ")
                qid = data[0]
                pid = data[2]
                score = data[4]

                if qid in ranker:
                    paraExtract = ranker.get(qid)
                    if pid in paraExtract:
                        list = paraExtract.get(pid)
                        list[current_feature_number] = score
                    else:
                        scorelist = [0.0 for x in range(0, number_of_feature)]
                        scorelist[current_feature_number] = score
                        paraExtract[pid] = scorelist
                else:
                    scorelist = [0.0 for x in range(0, number_of_feature)]
                    scorelist[current_feature_number] = score
                    inner = dict()
                    inner[pid] = scorelist
                    ranker[qid] = inner

        current_feature_number = current_feature_number + 1

    return ranker


'''
Helper functions to read the Qrel file into dict
'''


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


'''
Helper functions to display the list of file
'''


def dump_file_out(fileList):
    for file in fileList:
        print(file)


'''
Helper functions to display the qrel file
'''


def display_qrel_out(Qrel):
    for key, value in Qrel.items():
        for para in value:
            print(key, para)


'''
Helper functions to display the updated score file
'''


def display_dict_out(Qrel):
    for key, value in Qrel.items():
        for k, v in value.items():
            print(key, k, v)


'''
Creates te columns based on the number of features
This is used to create pandas DF
isrelevant,qid,pid,fet1,fet2 ...... fetn
'''


def get_columns(number_of_fet):
    col = []
    col.append("isrel")
    col.append("qid")
    col.append("pid")

    for i in range(0, number_of_fet):
        col.append("fet" + str(i + 1))
    return col

def get_fet_col(number_of_fet):
    fet = []
    for i in range(number_of_fet):
        fet.append("fet"+str(i+1))
    return fet
'''
Convert dictionary into list
'''


def convert_dict_to_list(ranker, qrel):
    rowlists = []
    for qid, pval in ranker.items():
        for pid, slist in pval.items():
            temp = []
            temp.append(is_relevant(qrel, qid, pid))
            temp.append(qid)
            temp.append(pid)
            for val in slist:
                temp.append(val)
            rowlists.append(temp)
    return rowlists


def create_data_frame(rowlist, number_of_fet):
    col = get_columns(number_of_fet)
    fet_data_frame = pd.DataFrame(rowlist, columns=col)
    return fet_data_frame


'''
Read the file names in to list
'''


def getFileList(path):
    return [os.path.join(path, file) for file in os.listdir(path)]


'''
Helper function to Display the 
row list created using the dictionary
'''

def disp_row_list(rowlist):
    for val in rowlist:
        print(val)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("RankLib File Formatter")
    parser.add_argument("-q", "--qrelpath", help="Path to the Qrel file", required=True)
    parser.add_argument("-d", "--dirpath", help="Path to the Qrel file", required=True)
    parser.add_argument("-v", "--verbose", help="Display information on the stdout", action="store_true")
    parser.add_argument("-s", "--suffix", help="Pass a filename suffix")
    parser.add_argument("-r", "--ranklib", help="Pass a filename suffix")
    parser.add_argument("-n", "--normalize", help="Perform Z score normalize on the data", action="store_true")

    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    Qrel = None
    runFiles = None

    if args.qrelpath:
        Qrel = readQrel(args.qrelpath)

    if args.dirpath:
        runFiles = getFileList(args.dirpath)

    if args.verbose:
        verbose = True
        display_qrel_out(Qrel)
        dump_file_out(runFiles)

    ranker = create_dictionary(runFiles)

    if (args.verbose):
        display_dict_out(ranker)

    fname = ""
    if args.suffix:
        fname = args.suffix + ".txt"
    else:
        fname = "featurefile.txt"

    if args.normalize:
        rowlist = convert_dict_to_list(ranker, Qrel)
        df = create_data_frame(rowlist, len(runFiles))
        if (args.verbose):
            print(df.head())
    else:
        write_feature_file_unnormalized(Qrel, ranker, fname)
