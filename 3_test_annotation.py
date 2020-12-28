import os
import os.path
import numpy as np
import xml.etree.ElementTree as xmlET
from PIL import Image, ImageDraw


classes = ('__background__', # always index 0
           'bump','trash','edge','person')

file_path_img = './VOC2012_enhance/JPEGImages'
file_path_xml = './VOC2012_enhance/Annotations'
save_file_path = './result'
pathDir = os.listdir(file_path_xml)
file_num=len(pathDir)

for idx in range(file_num): 
    filename = pathDir[idx]
    print('Completion :%d/%d'%(idx,file_num),filename)
    tree = xmlET.parse(os.path.join(file_path_xml, filename))
    objs = tree.findall('object')        
    num_objs = len(objs)
    boxes = np.zeros((num_objs, 5), dtype=np.uint16)

    for ix, obj in enumerate(objs):
        bbox = obj.find('bndbox')
        # Make pixel indexes 0-based
        x1 = float(bbox.find('xmin').text) + 1
        y1 = float(bbox.find('ymin').text) + 1
        x2 = float(bbox.find('xmax').text) + 1
        y2 = float(bbox.find('ymax').text) + 1

        cla = obj.find('name').text 
        label = classes.index(cla)
        boxes[ix, 0:4] = [x1, y1, x2, y2]
        boxes[ix, 4] = label

    image_name = os.path.splitext(filename)[0]
    img = Image.open(os.path.join(file_path_img, image_name + '.jpg')) 

    draw = ImageDraw.Draw(img)
    for ix in range(len(boxes)):
        xmin = int(boxes[ix, 0])
        ymin = int(boxes[ix, 1])
        xmax = int(boxes[ix, 2])
        ymax = int(boxes[ix, 3])
        draw.rectangle([xmin, ymin, xmax, ymax], outline=(255, 0, 0))
        draw.text([xmin, ymin], classes[boxes[ix, 4]], (255, 0, 0))

    img.save(os.path.join(save_file_path, image_name + '.png'))
