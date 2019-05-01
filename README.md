# RankLib

Create the ranklib by taking the Run files directory as input with Ground truth file

# CommandLine options

```
usage: RankLib File Formatter [-h] -q QRELPATH [-d DIRPATH [DIRPATH ...]] [-v]
                              [-s SUFFIX] [-r RANKLIB] [-n] [-m MODELFILE]
                              [-dir RUNDIR]

optional arguments:
  -h, --help            show this help message and exit
  -q QRELPATH, --qrelpath QRELPATH
                        Path to the Qrel file
  -d DIRPATH [DIRPATH ...], --dirpath DIRPATH [DIRPATH ...]
                        Path to the Qrel file
  -v, --verbose         Display information on the stdout
  -s SUFFIX, --suffix SUFFIX
                        Pass a filename suffix
  -r RANKLIB, --ranklib RANKLIB
                        Path to the RankLib jar
  -n, --normalize       Perform Z score normalize on the data
  -m MODELFILE, --modelfile MODELFILE
                        Pass model file, this is for the test set
  -dir RUNDIR, --rundir RUNDIR
                        pass the runfile directory, it will sort the files
```
Example command line argument, using the --rundir option reads the file from the directory and sorts it.

```
--qrelpath  D:\test200-train\train.pages.cbor-article.qrels --runir D:\test --ranklib D:\RankLib\RankLib-2.10.jar -n
```
If you want to pass the file as the list of arguments, example, --dirpath fet1 fet2 fet3 .... fetn, use the below command

```
--qrelpath  D:\test200-train\train.pages.cbor-article.qrels --dirpath fet1 fet2 fet3 --ranklib D:\RankLib\RankLib-2.10.jar -n
```

Once you have the model file trained on the Train run files,the same program can be used to use this model file on the test run files by ignoring the --ranklib option and passing in the --modelfile option.

Example command line argument
```
--qrelpath  D:\test200-train\train.pages.cbor-article.qrels --dirpath D:\test -n --modelfile model.txt
```
# Normalizer

Another application that takes the feature file and qrels as input and produces zscore normalized version output file. Additionally, you can pass the ranklib path, it will run the ranklib and converts the feature file into combined run file

```
usage: Takes unnormalized feature file and performs the normalization
       [-h] -q QRELPATH -f FETPATH [-v] [-s SUFFIX] [-r RANKLIB] [-n]

optional arguments:
  -h, --help            show this help message and exit
  -q QRELPATH, --qrelpath QRELPATH
                        Path to the Qrel file
  -f FETPATH, --fetpath FETPATH
                        Path to the Feature file
  -v, --verbose         Display information on the stdout
  -s SUFFIX, --suffix SUFFIX
                        Pass a filename suffix
  -r RANKLIB, --ranklib RANKLIB
                        Path to the RankLib jar
  -n, --normalizer      Perform Z score normalize on the data

```

Example command line argument

```
--normalizer --qrelpath  D:\test200-train\train.pages.cbor-article.qrels --fetpath featurefile.txt --ranklib D:\RankLib\RankLib-2.10.jar
```

File Format

```
1 qid:1 1:2.86898275512205 2:1.6123268762274203 3:1.830355435547622 4:1.6527173793977503 #enwiki:Political%20status%20of%20Transnistria_6019abc315e3afd5250d01a8897bee49b1646249
```
# Note

The directory should contains only the run files because program does not make any sanity check if other file exists, each file as considered as one feature
