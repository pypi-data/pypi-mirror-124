#!/usr/bin/env python
# coding: utf-8

# -*- coding: utf-8 -*-

import os
import shutil
import random

random.seed(123)

BASE_DIR = os.getcwd()

def make_dir(dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

root_dir = os.path.join(BASE_DIR, "..", "data", "dataset")
out_dir = os.path.join(BASE_DIR, "..", "data", "dataset", "voc_format")
train_per = 0.9

if os.path.exists(out_dir):
    
    shutil.rmtree(out_dir)
    print(" ".format(out_dir))

 
img_list = []
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".png") and not file.endswith("matte.png"):
            path_img = os.path.join(root, file)
            img_list.append(path_img)

print(" ".format(root_dir, len(img_list)))


 
random.shuffle(img_list)

split_point = int(len(img_list) * train_per)
train_list = img_list[:split_point]
valid_list = img_list[split_point:]
train_msk_list = [i[:-4] + "_matte.png" for i in train_list]
valid_msk_list = [i[:-4] + "_matte.png" for i in valid_list]
print(" ".format(len(train_list), len(valid_list)))

 
def cp_batch(path_lst, dst_dir):
    for idx, p in enumerate(path_lst):
        src_path = p
        file_name = os.path.basename(p)
        base_dir = os.path.dirname(p)
        set_name = os.path.basename(base_dir)
        new_file_name = set_name + "_" + file_name
        dst_path = os.path.join(dst_dir, new_file_name)
        shutil.copy(src_path, dst_path)
        print("\r{}/{}".format(idx, len(path_lst)), end="", flush=True)


out_img_dir = os.path.join(out_dir, "JPEGImages")
out_msk_dir = os.path.join(out_dir, "SegmentationClass")
make_dir(out_img_dir)
make_dir(out_msk_dir)

cp_batch(train_list + valid_list, out_img_dir)
cp_batch(train_msk_list + valid_msk_list, out_msk_dir)
print("  :{}".format(out_img_dir, out_msk_dir))

 
txt_dir = os.path.join(out_dir, "ImageSets", "Segmentation")
make_dir(txt_dir)
path_train_txt = os.path.join(txt_dir, "train.txt")
path_valid_txt = os.path.join(txt_dir, "val.txt")

def gen_txt(path_lst, path_txt):
    "   "
    with open(path_txt, "w") as f:
        for path in path_lst:
            p = path
            file_name = os.path.basename(p)
            base_dir = os.path.dirname(p)
            set_name = os.path.basename(base_dir)
            new_file_name = set_name + "_" + file_name[:-4]
            f.writelines(str(new_file_name) + "\n")
    print("write done, path:{}".format(path_txt))


gen_txt(train_list, path_train_txt)
gen_txt(valid_list, path_valid_txt)

 




