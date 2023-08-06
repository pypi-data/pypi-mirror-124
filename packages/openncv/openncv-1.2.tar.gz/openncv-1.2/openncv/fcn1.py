#!/usr/bin/env python
# coding: utf-8


import time
from tqdm import tqdm
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import math
import sys
import os
sys.path.append("..")

voc_dir = "/home/student24/notebooks/cv_project_2days/object_detection/data/VOCdevkit/VOC2012" # linux
# voc_dir = r"G:\deep_learning_data\VOCdevkit\VOC2012"
dirs_lst = os.listdir(voc_dir)
print(dirs_lst)



feature = tf.io.read_file('%s/JPEGImages/%s.jpg' % (voc_dir, fname))
feature = tf.image.decode_jpeg(feature)
print(feature.shape)   #(h, w, c)
plt.imshow(feature)


# In[5]:


label = tf.io.read_file('%s/SegmentationClass/%s.png' % (voc_dir, fname))
label = tf.image.decode_png(label)

print(label.shape)
plt.imshow(label)   #(h, w, c)


# In[6]:


def read_voc_images(root,  is_train=True, max_num=None):
    txt_fname = '%s/ImageSets/Segmentation/%s' % (root, 'train.txt' if is_train else 'val.txt') # 获取txt文件路径
    
    with open(txt_fname, 'r') as f:
        images = f.read().split()  # 获取图片名称
        
    if max_num is not None:
        images = images[:min(max_num, len(images))] # 截取 max_num张图片
        
    features, labels = [None] * len(images), [None] * len(images) # 创建空list
    
    for i, fname in tqdm(enumerate(images)):
        feature_tmp = tf.io.read_file('%s/JPEGImages/%s.jpg' % (root, fname))  # 读取图片
        features[i] = tf.image.decode_jpeg(feature_tmp)                        # 存入列表中
        
        label_tmp = tf.io.read_file('%s/SegmentationClass/%s.png' % (root, fname)) # 读取标签
        labels[i] = tf.image.decode_png(label_tmp)                              # 存入列表中
        
    return features, labels # shape=(h, w, c)


# In[7]:


def show_images(imgs, num_rows, num_cols, scale=2):
    figsize = (num_cols * scale, num_rows * scale)
    _, axes = plt.subplots(num_rows, num_cols, figsize=figsize)
    for i in range(num_rows):
        for j in range(num_cols):
            axes[i][j].imshow(imgs[i * num_cols + j])
            axes[i][j].axes.get_xaxis().set_visible(False)
            axes[i][j].axes.get_yaxis().set_visible(False)
    return axes


# In[8]:


train_features, train_labels = read_voc_images(voc_dir, max_num=10)


# 我们画出前5张输入图像和它们的标签。在标签图像中，白色和黑色分别代表边框和背景，而其他不同的颜色则对应不同的类别。

# In[9]:


n = 5
imgs = train_features[0:n] + train_labels[0:n]
show_images(imgs, 2, n)


# 

# ## 3. 标签转换
# 接下来，我们列出标签中每个RGB颜色的值及其标注的类别。

# In[10]:


VOC_COLORMAP = [[0, 0, 0], [128, 0, 0], [0, 128, 0], [128, 128, 0],
                [0, 0, 128], [128, 0, 128], [0, 128, 128], [128, 128, 128],
                [64, 0, 0], [192, 0, 0], [64, 128, 0], [192, 128, 0],
                [64, 0, 128], [192, 0, 128], [64, 128, 128], [192, 128, 128],
                [0, 64, 0], [128, 64, 0], [0, 192, 0], [128, 192, 0],
                [0, 64, 128]]

VOC_CLASSES = ['background', 'aeroplane', 'bicycle', 'bird', 'boat',
               'bottle', 'bus', 'car', 'cat', 'chair', 'cow',
               'diningtable', 'dog', 'horse', 'motorbike', 'person',
               'potted plant', 'sheep', 'sofa', 'train', 'tv/monitor']



colormap2label = np.zeros(256 ** 3, dtype=np.uint8)  # 256 ** 3 = 1677 7216

for i, colormap in enumerate(VOC_COLORMAP):
    colormap2label[(colormap[0] * 256 + colormap[1]) * 256 + colormap[2]] = i  #
    
colormap2label = tf.convert_to_tensor(colormap2label)
colormap2label[8388608]
colormap2label[32768]
def voc_label_indices(colormap, colormap2label):
    """
    convert colormap (tf image) to colormap2label (uint8 tensor).
    """
    colormap = tf.cast(colormap, dtype=tf.int32)
    idx = tf.add(tf.multiply(colormap[:, :, 0], 256), colormap[:, :, 1])
    idx = tf.add(tf.multiply(idx, 256), colormap[:, :, 2])
    idx = tf.add(idx, colormap[:, :, 2])
    return tf.gather_nd(colormap2label, tf.expand_dims(idx, -1))

y = voc_label_indices(train_labels[0], colormap2label)  # tf.image
y[105:115, 130:140], VOC_CLASSES[1]


def voc_rand_crop(feature, label, height, width):
    """
    Random crop feature (tf image) and label (tf image).
    先将channel合并，剪裁之后再分开
    """
    combined = tf.concat([feature, label], axis=2)
    last_label_dim = tf.shape(label)[-1]
    last_feature_dim = tf.shape(feature)[-1]
    combined_crop = tf.image.random_crop(combined,
                        size=tf.concat([(height, width), [last_label_dim + last_feature_dim]],axis=0))
    return combined_crop[:, :, :last_feature_dim], combined_crop[:, :, last_feature_dim:]

imgs = []
for _ in range(n):
    imgs += voc_rand_crop(train_features[0], train_labels[0], 200, 300)
show_images(imgs[::2] + imgs[1::2], 2, n)



def getVOCSegDataset(is_train, crop_size, voc_dir, colormap2label, max_num=None):
    """
    crop_size: (h, w)
    """
    features, labels = read_voc_images(root=voc_dir, 
                        is_train=is_train,
                        max_num=max_num)
    def _filter(imgs, crop_size):
        return [img for img in imgs if (
            img.shape[0] >= crop_size[0] and
            img.shape[1] >= crop_size[1])]
    
    def _crop(features, labels):
        features_crop = []
        labels_crop = []
        for feature, label in zip(features, labels):
            feature, label = voc_rand_crop(feature, label, 
                            height=crop_size[0],
                            width=crop_size[1])
            features_crop.append(feature)
            labels_crop.append(label)
        return features_crop, labels_crop
    
    def _normalize(feature, label):
        rgb_mean = np.array([0.485, 0.456, 0.406])
        rgb_std = np.array([0.229, 0.224, 0.225])
        
        label = voc_label_indices(label, colormap2label)
        feature = tf.cast(feature, tf.float32)
        feature = tf.divide(feature, 255.)

        return feature, label

    features = _filter(features, crop_size)
    labels = _filter(labels, crop_size)
    features, labels = _crop(features, labels)

    print('read ' + str(len(features)) + ' valid examples')
    dataset = tf.data.Dataset.from_tensor_slices((features, labels))
    dataset = dataset.map(_normalize) #dataset map方法
    return dataset




crop_size = (320, 400)
max_num = 100

voc_train = getVOCSegDataset(True, crop_size, voc_dir, colormap2label, max_num)
voc_test = getVOCSegDataset(False, crop_size, voc_dir, colormap2label, max_num)



batch_size = 64
voc_train = voc_train.batch(batch_size)
voc_test = voc_test.batch(batch_size)



for x, y in iter(voc_train):
    print(x.dtype, x.shape)
    print(y.dtype, y.shape)
    break





