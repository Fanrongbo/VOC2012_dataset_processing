import os
import random
import sys
import shutil

root_path='./VOC2012_trash_edge'
xmlfilepath = root_path + '/Annotations/'
imgfilepath=root_path + '/JPEGImages/'

root_save_path='./VOC_trash_edge'
xmlfilesavepath =  root_save_path+'/Annotations/'
imgfilesavepath= root_save_path+'/JPEGImages/'
if not os.path.exists(root_save_path):
    os.mkdir(root_save_path)
if not os.path.exists(xmlfilesavepath):
    os.mkdir(xmlfilesavepath)
if not os.path.exists(imgfilesavepath):
    os.mkdir(imgfilesavepath)
fileList = os.listdir(xmlfilepath)
i=0
for path in fileList:
    name=path.split('.')[0]
    xmlpath=xmlfilepath+path
    imgpath=imgfilepath+name+'.jpg'
    print(imgpath)
    shutil.copyfile(imgpath,imgfilesavepath+'%d.jpg'%i)
    shutil.copyfile(xmlpath,xmlfilesavepath+'%d.xml'%i)
    i=i+1
