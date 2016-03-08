import os
from os.path import join


def populate_directory(root):
    '''
     - 1
       - 1-1
         - 1-1.txt -> standard-content 1-1
     - 2
       - 2-1
         - 2-1.txt -> standard-content 2-1
     - empty
    '''

    os.mkdir(join(root, '1'))
    os.mkdir(join(root, '1', '1-1'))
    with open(join(root, '1', '1-1', '1-1.txt'), 'w') as f:
        f.write('standard-content 1-1')
    os.mkdir(join(root, '2'))
    os.mkdir(join(root, '2', '2-1'))
    with open(join(root, '2', '2-1', '2-1.txt'), 'w') as f:
        f.write('standard-content 2-1')
    os.mkdir(join(root, 'empty'))
