
with open('dummy/management/commands/data/fnames.txt', 'r') as f:
    fnames = list(set([line.strip() for line in f]))