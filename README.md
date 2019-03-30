# RankLib

Create the ranklib by taking the Run files directory as input with Ground truth file

# CommandLine options

```
usage: RankLib File Formatter [-h] -q QRELPATH -d DIRPATH [-v] [-s SUFFIX]
                              [-r RANKLIB] [-n]

optional arguments:
  -h, --help            show this help message and exit
  -q QRELPATH, --qrelpath QRELPATH
                        Path to the Qrel file
  -d DIRPATH, --dirpath DIRPATH
                        Path to the Qrel file
  -v, --verbose         Display information on the stdout
  -s SUFFIX, --suffix SUFFIX
                        Pass a filename suffix
  -r RANKLIB, --ranklib RANKLIB
                        Pass a filename suffix
  -n, --normalize       Perform Z score normalize on the each feature
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

# Note

The directory should contains only the run files because program does not make any sanity check if other file exists, each file as considered as one feature
