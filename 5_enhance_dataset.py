import cv2
import math
import numpy as np
import os
import glob
import json
import shutil
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element
import random
################################color###########################

def getColorImg(alpha,beta,img_path,img_write_path):
    img = cv2.imread(img_path)
    colored_img = np.uint8(np.clip((alpha * img + beta), 0, 255))
    cv2.imwrite(img_write_path,colored_img)

def getColorAnno(anno_path,anno_write_path):
    tree = ET.parse(anno_path) 
    tree.write(anno_write_path)  # save XML file

def color(alpha,beta,img_path,anno_path,img_write_dir,anno_write_dir,img_name,num):

    img_write_path=os.path.join(img_write_dir,'%d.jpg'%num)

    anno_write_path = os.path.join(anno_write_dir, '%d.xml'%num)

    getColorImg(alpha,beta,img_path,img_write_path)
    getColorAnno(anno_path,anno_write_path)
    return img_write_path,anno_write_path
################################rotate###########################
def getRotatedImg(Pi_angle,img_path,img_write_path):
    img = cv2.imread(img_path)
    rows, cols = img.shape[:2]
    a, b = cols / 2, rows / 2
    M = cv2.getRotationMatrix2D((a, b), angle, 1)
    rotated_img = cv2.warpAffine(img, M, (cols, rows))  # The rotated image remains the same size
    cv2.imwrite(img_write_path,rotated_img)
    return a,b

def getRotatedAnno(Pi_angle,a,b,anno_path,anno_write_path):
    tree = ET.parse(anno_path)
    root = tree.getroot()
    objects = root.findall("object")
    for obj in objects:
        bbox = obj.find('bndbox')
        x1 = float(bbox.find('xmin').text) - 1
        y1 = float(bbox.find('ymin').text) - 1
        x2 = float(bbox.find('xmax').text) - 1
        y2 = float(bbox.find('ymax').text) - 1

        x3=x1
        y3=y2
        x4=x2
        y4=y1

        X1 = (x1 - a) * math.cos(Pi_angle) - (y1 - b) * math.sin(Pi_angle) + a
        Y1 = (x1 - a) * math.sin(Pi_angle) + (y1 - b) * math.cos(Pi_angle) + b

        X2 = (x2 - a) * math.cos(Pi_angle) - (y2 - b) * math.sin(Pi_angle) + a
        Y2 = (x2 - a) * math.sin(Pi_angle) + (y2 - b) * math.cos(Pi_angle) + b

        X3 = (x3 - a) * math.cos(Pi_angle) - (y3 - b) * math.sin(Pi_angle) + a
        Y3 = (x3 - a) * math.sin(Pi_angle) + (y3 - b) * math.cos(Pi_angle) + b

        X4 = (x4 - a) * math.cos(Pi_angle) - (y4 - b) * math.sin(Pi_angle) + a
        Y4 = (x4 - a) * math.sin(Pi_angle) + (y4 - b) * math.cos(Pi_angle) + b

        X_MIN=min(X1,X2,X3,X4)
        X_MAX = max(X1, X2, X3, X4)
        Y_MIN = min(Y1, Y2, Y3, Y4)
        Y_MAX = max(Y1, Y2, Y3, Y4)

        bbox.find('xmin').text=str(int(X_MIN))
        bbox.find('ymin').text=str(int(Y_MIN))
        bbox.find('xmax').text=str(int(X_MAX))
        bbox.find('ymax').text=str(int(Y_MAX))

    tree.write(anno_write_path) 

def rotate(angle,img_path,anno_path,img_write_dir,anno_write_dir,img_name,num):
    Pi_angle = -angle * math.pi / 180.0  # Radian system, the rotation coordinates need to use, pay attention to the minus sign!!

    img_write_path=os.path.join(img_write_dir,'%d.jpg'%num)
    #
    anno_write_path = os.path.join(anno_write_dir, '%d.xml'%num)
    #
    a,b=getRotatedImg(Pi_angle,img_path,img_write_path)
    getRotatedAnno(Pi_angle,a,b,anno_path,anno_write_path)
    return img_write_path,anno_write_path


################################mirror###########################


def h_MirrorImg(img_path,img_write_path):
    img = cv2.imread(img_path)
    mirror_img = cv2.flip(img, 1)  #
    cv2.imwrite(img_write_path,mirror_img)
def v_MirrorImg(img_path,img_write_path):
    img = cv2.imread(img_path)
    mirror_img = cv2.flip(img, 0)  #
    cv2.imwrite(img_write_path,mirror_img)
def a_MirrorImg(img_path,img_write_path):
    img = cv2.imread(img_path)
    mirror_img = cv2.flip(img, -1)  #
    cv2.imwrite(img_write_path,mirror_img)

def h_MirrorAnno(anno_path,anno_write_path):
    tree = ET.parse(anno_path)
    root = tree.getroot()
    size=root.find('size')
    w=int(size.find('width').text)
    objects = root.findall("object")
    for obj in objects:
        bbox = obj.find('bndbox')
        x1 = float(bbox.find('xmin').text)
        x2 = float(bbox.find('xmax').text)
        x1=w-x1+1
        x2=w-x2+1
        assert x1>0
        assert x2>0
        bbox.find('xmin').text=str(int(x2))
        bbox.find('xmax').text=str(int(x1))
    tree.write(anno_write_path)  
    
def v_MirrorAnno(anno_path,anno_write_path):
    tree = ET.parse(anno_path)
    root = tree.getroot()
    size = root.find('size')
    h=int(size.find('height').text)
    objects = root.findall("object")
    for obj in objects:
        bbox = obj.find('bndbox')
        y1 = float(bbox.find('ymin').text)
        y2 = float(bbox.find('ymax').text)

        y1=h-y1+1
        y2=h-y2+1

        assert y1>0
        assert y2>0

        bbox.find('ymin').text=str(int(y2))
        bbox.find('ymax').text=str(int(y1))

    tree.write(anno_write_path)  
    
def a_MirrorAnno(anno_path,anno_write_path):
    tree = ET.parse(anno_path)
    root = tree.getroot()
    size = root.find('size')
    w=int(size.find('width').text)
    h = int(size.find('height').text)
    objects = root.findall("object")
    for obj in objects:
        bbox = obj.find('bndbox')
        x1 = float(bbox.find('xmin').text)
        y1 = float(bbox.find('ymin').text)
        x2 = float(bbox.find('xmax').text)
        y2 = float(bbox.find('ymax').text)

        x1=w-x1+1
        x2=w-x2+1

        y1 = h - y1+1
        y2 = h - y2+1

        assert x1 > 0
        assert x2 > 0
        assert y1 > 0
        assert y2 > 0

        bbox.find('xmin').text=str(int(x2))
        bbox.find('xmax').text=str(int(x1))
        bbox.find('ymin').text=str(int(y2))
        bbox.find('ymax').text=str(int(y1))

    tree.write(anno_write_path)  
    
def mirror(img_path,anno_path,img_write_dir,anno_write_dir,img_name,num):
    a=random.randint(0,2)
    # print('a',a)
    img_write_path=os.path.join(img_write_dir,'%d.jpg'%num)
    anno_write_path = os.path.join(anno_write_dir, '%d.xml'%num)
    if a ==0:
        h_MirrorImg(img_path,img_write_path)
        h_MirrorAnno(anno_path,anno_write_path)
    if a ==1:
        v_MirrorImg(img_path,img_write_path)
        v_MirrorAnno(anno_path,anno_write_path)
    if a ==2:
        a_MirrorImg(img_path,img_write_path)
        a_MirrorAnno(anno_path,anno_write_path)
    return img_write_path,anno_write_path



alphas=[0.3,0.5,1.2,1.6]
beta=10
img_dir='VOC2012_4c/JPEGImages'
anno_dir='VOC2012_4c/Annotations'
img_write_dir='VOC2012_enhance/JPEGImages'
anno_write_dir='VOC2012_enhance/Annotations'
if not os.path.exists(img_write_dir):
    os.makedirs(img_write_dir)

if not os.path.exists(anno_write_dir):
    os.makedirs(anno_write_dir)
# for alpha in alphas:
img_names=os.listdir(img_dir)
print('original num',len(img_names))
goal_num=18000
num=0
angle=180
# for i in range(round(goal_num/len(img_names))):
while num <= goal_num:
    
    for img_name in img_names:
        img_path=os.path.join(img_dir,img_name)
        anno_path=os.path.join(anno_dir,img_name[:-4]+'.xml')
        alpha=random.randint(3,16)
        beta=random.randint(-10,10)
        if random.randint(0,1)==1:
            print('mirror')
        img_path,anno_path=mirror(img_path,anno_path,img_write_dir,anno_write_dir,img_name,num)
        if random.randint(0,1)==1:
            print('rotate')
        img_path,anno_path=rotate(180,img_path,anno_path,img_write_dir,anno_write_dir,img_name,num)
        img_path,anno_path=color(alpha/10,beta,img_path,anno_path,img_write_dir,anno_write_dir,img_name,num)
        num=num+1
        print(img_path,num,'/',angle,'schedule percent:%.4f'%(num/angle))
print('Complete the dataset enhance: expansion from %d to %d'%(len(img_names),goal_num))
    
    
    
    
    
    
    
    
    
    
    
    