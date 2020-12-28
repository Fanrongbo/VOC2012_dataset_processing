import os
import random
import sys

# if len(sys.argv) < 2:
    # print("no directory specified, please input target directory")
    # exit()

# root_path = sys.argv[1]
root_path='./VOC2012_person/'
xmlfilepath = root_path + '/Annotations'

txtsavepath = root_path + '/ImageSets/Main'

if not os.path.exists(root_path):
    print("cannot find such directory: " + root_path)
    exit()

if not os.path.exists(txtsavepath):
    os.makedirs(txtsavepath)
    
trainval_percent = 0.95
train_percent = 0.8
total_xml = os.listdir(xmlfilepath)
num = len(total_xml)
list = range(num)
tv = int(num * trainval_percent)
tr = int(tv * train_percent)
trainval = random.sample(list, tv)
train = random.sample(trainval, tr)

print("train size:", tr)
print("val size:", tv-tr)
print('test size:',num-tv)
print('total size:',num)

ftest = open(txtsavepath + '/test.txt', 'w')
ftrain = open(txtsavepath + '/train.txt', 'w')
fval = open(txtsavepath + '/val.txt', 'w')

for i in list:
    name = total_xml[i][:-4] + '\n'
    if i in trainval:
        if i in train:
            ftrain.write(name)
        else:
            fval.write(name)
    else:
        ftest.write(name)

ftrain.close()
fval.close()
ftest.close()
