#!/usr/bin/env python
# coding: utf-8

# ## BERT解决NER任务
# 
# ![jupyter](./imgs/bert_ner.png)

# In[2]:


import pickle
import numpy as np
import tensorflow as tf
from transformers import BertTokenizer, TFBertForTokenClassification, TFBertModel
from tensorflow.keras.preprocessing.sequence import pad_sequences

import util

import warnings
warnings.filterwarnings('ignore')


# ## 1. 构建数据集

# In[3]:


dataset_save_path = './data/dataset.pkl'

with open(dataset_save_path, 'rb') as f:
    train_sentences, val_sentences, test_sentences, tag_2_id, id_2_tag = pickle.load(f)
    
len(train_sentences), len(val_sentences), len(test_sentences)


# In[10]:


train_sentences[10]


# In[11]:


tag_2_id


# In[21]:


for x in train_sentences[100]:
    #print(x[2])
    print([tag_2_id.get(x[2], 0)][: 51])


# In[4]:


tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

test_sentence = '李正茂出任中国电信集团有限公司总经理。'

bert_input = tokenizer.encode_plus(
                        test_sentence,                      
                        add_special_tokens = True,  
                        max_length = 50,  
                        pad_to_max_length = True, 
                        truncation=True,
                        return_attention_mask = True, 
              )
for k, v in bert_input.items():
    print(k)
    print(v)


# In[ ]:





# In[5]:


def convert_sample_to_feature(text, max_length):
    return tokenizer.encode_plus(text, 
                                 add_special_tokens = True,  
                                 max_length=max_length,  
                                 padding='max_length',      
                                 truncation=True,
                                 return_attention_mask = True,  
                                )


def map_sample_to_dict(input_ids, token_type_ids, attention_masks, label):
    return {
      "input_ids": input_ids,
      "token_type_ids": token_type_ids,
      "attention_mask": attention_masks,
  }, label


def build_dataset(samples, tag_2_id, max_length, batch_size, is_train):
    input_ids_list = []
    token_type_ids_list = []
    attention_mask_list = []
    label_list = []

    for sample in samples:
        text = [x[0] for x in sample]
        label = [tag_2_id.get(x[2], 0) for x in sample][: MAX_SEQ_LEN-1]
        label.insert(0, 0)  # 开头加PAD，即CLS
        bert_input = convert_sample_to_feature(text, max_length)
        input_ids_list.append(bert_input['input_ids'])
        token_type_ids_list.append(bert_input['token_type_ids'])
        attention_mask_list.append(bert_input['attention_mask'])
        label_list.append(label)
    label_list = pad_sequences(label_list, padding='post', maxlen=MAX_SEQ_LEN, )
    dataset = tf.data.Dataset.from_tensor_slices((input_ids_list, attention_mask_list, token_type_ids_list, label_list))
    dataset = dataset.map(map_sample_to_dict)
    buffer_size = len(label_list)
    if is_train:
        dataset = dataset.shuffle(buffer_size)
    dataset = dataset.batch(batch_size).prefetch(buffer_size)
    return dataset


# In[6]:


BATCH_SIZE = 16
MAX_SEQ_LEN = 52

# dataset
train_dataset = build_dataset(train_sentences, tag_2_id, MAX_SEQ_LEN, BATCH_SIZE, True)
val_dataset = build_dataset(val_sentences, tag_2_id, MAX_SEQ_LEN, BATCH_SIZE, False)
test_dataset = build_dataset(test_sentences, tag_2_id, MAX_SEQ_LEN, BATCH_SIZE, False)


# ## 2. 模型训练
# 
# ![jupyter](./imgs/bert_token_classification.jpeg)

# In[7]:


NUM_LABELS = len(list(tag_2_id))
LR = 1e-5
EPOCHS = 10
PATIENCE = 2


# In[8]:


# 模型初始化
model = TFBertForTokenClassification.from_pretrained('bert-base-chinese',
                                                     from_pt=True,
                                                     num_labels=NUM_LABELS)
# 定义优化器
optimizer = tf.keras.optimizers.Adam(learning_rate=LR)

loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
metric = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')
model.compile(optimizer=optimizer,
              loss=loss,
              metrics=[metric])


# In[9]:


callback = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy',
                                            patience=PATIENCE,
                                            restore_best_weights=True)

# 模型训练
bert_history = model.fit(train_dataset,
                         epochs=EPOCHS,
                         callbacks=[callback],
                         validation_data=val_dataset)


# In[10]:


# 保存模型
save_model_path = "./bert/bert_ner"
model.save_pretrained(save_model_path, saved_model=True)


# ## 3. 模型评估

# In[11]:


output = model.predict(test_dataset)
pred_logits = output.logits
pred_label_ids = np.argmax(pred_logits, axis=2).tolist()

preds, trues = [], []

for sample, pred_ids in zip(test_sentences, pred_label_ids):
    label = [x[2] for x in sample]
    seq_len = len(label)  # 获取序列真实长度
    pred_label = [id_2_tag[x] for x in pred_ids[1: seq_len+1]] # 开头0为CLS，所以从1开始取
    assert len(label) == len(pred_label), (label, pred_label)
    preds.extend(pred_label)
    trues.extend(label)

# 对结果进行评估
metric_result = util.measure_by_tags(trues, preds)


# ## 4. 模型预测

# In[12]:


# 加载模型
save_model_path = "./bert/bert_ner"
saved_model = TFBertForTokenClassification.from_pretrained(save_model_path)


# In[13]:


# 使用模型进行预测
predict_sentences = ['李正茂出任中国电信集团有限公司总经理。',
                     '2012年成立中国电信国际有限公司,总部设于中国香港。',
                     '《长津湖》将于今年下半年上映。']

# tokenizer
predict_inputs = tokenizer(predict_sentences, padding=True, max_length=MAX_SEQ_LEN, return_tensors="tf")
# 模型前向运算
output = saved_model(predict_inputs)
# 获取标签分数
predict_logits = output.logits.numpy()
# 取最大标签分数结果
predict_label_ids = np.argmax(predict_logits, axis=2).tolist()


# In[14]:


# 格式化展示结果
for text, pred_ids in zip(predict_sentences, predict_label_ids):
    print(text)
    seq_len = len(text)
    bio_seq = [id_2_tag[x] for x in pred_ids[1: seq_len+1]]
    print(bio_seq)
    entities_result = util.bio_2_entities(bio_seq)
    json_result = util.formatting_result(entities_result, text)
    print(json_result)


# In[ ]:




