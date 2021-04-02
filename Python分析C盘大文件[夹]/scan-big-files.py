import os
import codecs
from os.path import join, getsize

def getdirsize(dirDict, rootpath):
    dirsize = 0L
    for root, dirs, files in os.walk(rootpath):
        if root == rootpath:
            for dir in dirs:
                dirDict, fsize = getdirsize(dirDict, join(rootpath, dir))
                dirsize += fsize
            try:
                dirsize += sum([getsize(join(rootpath, file)) for file in files])
            except:
                pass
    if dirsize / 1024 / 1024 != 0 and rootpath not in dirDict:
        dirDict[rootpath] = dirsize / 1024 / 1024
        print len(dirDict)
    return dirDict, dirsize

if __name__ == '__main__':
    write_path = 'C:\\LOG.txt'
    write_file = codecs.open(write_path, 'w', encoding='UTF-8')
    rootpath = 'C:\\'
    dirDict = {}
    for file in os.listdir(rootpath):
        if file.startswith('$'):
            continue
        if os.path.isdir(join(rootpath,file)):
            dirDict, fsize = getdirsize(dirDict, join(rootpath, file))
            seq_dict = sorted(dirDict.items(), key=lambda t: t[1], reverse=True)
            for item in seq_dict:
                write_file.write('\t'.join([item[0], '%.1f' % item[1]]).decode('gbk')+'\n')
