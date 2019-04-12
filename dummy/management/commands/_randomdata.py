
def read_data(path):
    with open('dummy/management/commands/data/' + path + '.txt', 'r') as f:
        return list(set([line.strip() for line in f]))

fnames = read_data('fnames')
lnames = read_data('lnames')

