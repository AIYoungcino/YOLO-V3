import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
# 2012代表年份， 2012train.txt 就是ImageSets\Main 下对应的txt名称，其依次类推， 换成自己数据集需修改sets
sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

# classes 是所有类别名称， 换成自己数据集需要修改classes
classes = ["car", "bus"]

#@params  size  图片宽高
#@params  box  groud truth 框的x y w h
def convert(size, box):
    dw = 1./size[0]              # 用于下面框的坐标和高宽归一化
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0     # 求中心坐标
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(year, image_id):
    in_file = open('F:/YOLOv3-master/data04/VOC2007/Annotations/%s.xml'%(year, image_id))    # 读取 image_id 的xml文件
    out_file = open('F:/YOLOv3-master/data04/VOC2007/Annotations/labels/%s.txt'%(year, image_id), 'w')      # 保存txt文件地址
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')         # 读取图片 w h
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b) # w,h,x,y归一化操作
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')   # 一个框写入

wd = getcwd() # 获取当前地址

for year, image_set in sets:
    if not os.path.exists('F:/YOLOv3-master/data04/VOC%s/labels/'%(year)):
        os.makedirs('F:/YOLOv3-master/data04/VOC%s/labels/'%(year))
    image_ids = open('F:/YOLOv3-master/data04/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()  # 读取图片名称
    list_file = open('%s_%s.txt'%(year, image_set), 'w')                                                                                    # 保存所有图片的绝对路径
    for image_id in image_ids:
        list_file.write('%sF:/YOLOv3-master/data04/VOC%s/JPEGImages/%s.jpg\n'%(wd, year, image_id))
        convert_annotation(year, image_id)
    list_file.close()


