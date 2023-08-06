#!/usr/bin/env python
# coding: utf-8

import os
import re
import json
import jieba
import joblib
import datetime
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.initializers import Constant

from sklearn.model_selection import train_test_split
random_seed = 100

import warnings
warnings.filterwarnings('ignore')




get_ipython().run_line_magic('config', 'Completer.use_jieba=False')




with open('./data/baidu_stopwords.txt','r') as f:
    stop_words=f.read().split('\n')




def cut_content(text,stop_words):
    x=' '.join(x for x in jieba.lcut(text) if x not in stop_words)
    return x


text=''
cut_content(text,stop_words)



def preprocess_text(text):
    text = text.lower()
    text = re.sub('[^a-z^0-9^\u4e00-\u9fa5]', '', text)
    text = re.sub('[0-9]', '0', text)
    text = ' '.join(text)
    text = re.sub('\s{2,}', ' ', text)
    return text.strip()


# In[7]:


raw_train_df = pd.read_csv('./processed_data/train.csv')
raw_train_df['text'] = raw_train_df['text'].apply(preprocess_text)
raw_train_df = raw_train_df[raw_train_df['text'] != '']
raw_train_df[['text', 'label']].head()


# In[8]:


raw_train_df.head()


# In[11]:


test_df = pd.read_csv('./processed_data/test.csv')
test_df['text'] = test_df['text'].apply(preprocess_text)
test_df = test_df[test_df['text'] != '']
test_df[['text', 'label']].head()



train_df, val_df = train_test_split(raw_train_df, test_size=5000, random_state=1234)  #
len(train_df), len(val_df)


train_df.to_csv('./dataset/train.csv', index=False)
val_df.to_csv('./dataset/val.csv', index=False)
test_df.to_csv('./dataset/test.csv', index=False)


train_text, train_label = train_df['text'], train_df['label']
val_text, val_label = val_df['text'], val_df['label']
test_text, test_label = test_df['text'], test_df['label']
len(train_label), len(val_label), len(test_label)

tokenizer = tf.keras.preprocessing.text.Tokenizer(
    num_words=None,
    filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
    lower=True,
    split=' ',
    char_level=False,
    oov_token=None
)

tokenizer.fit_on_texts(train_text)

text = ''

tokens = tokenizer.texts_to_sequences(text) 
print(tokens)

tokenizer_save_path = './model/tokenizer.pkl'


NUM_LABEL = 3
BATCH_SIZE = 64
MAX_LEN = 240
BUFFER_SIZE = tf.constant(len(train_text), dtype=tf.int64)  # bacth读取数据的缓存大小

def build_tf_dataset(text, label, is_train=False):
    sequence = tokenizer.texts_to_sequences(text)
    sequence_padded = pad_sequences(sequence, padding='post', maxlen=MAX_LEN)  #
    label_tensor = tf.convert_to_tensor(tf.one_hot(label, NUM_LABEL), dtype=tf.float32) #
    dataset = tf.data.Dataset.from_tensor_slices((sequence_padded, label_tensor))  #
    if is_train:
        dataset = dataset.shuffle(BUFFER_SIZE)
        dataset = dataset.batch(BATCH_SIZE, drop_remainder=True)  #
        dataset = dataset.prefetch(BUFFER_SIZE)
    else:
        dataset = dataset.batch(BATCH_SIZE, drop_remainder=False)
        dataset = dataset.prefetch(BATCH_SIZE)
    return dataset


train_dataset = build_tf_dataset(train_text, train_label, is_train=True)
val_dataset = build_tf_dataset(val_text, val_label, is_train=False)
test_dataset = build_tf_dataset(test_text, test_label, is_train=False)


for example, label in train_dataset.take(1):
    print('texts: ', example.numpy()[:3])
    print()
    print('labels: ', label.numpy()[:3])

VOCAB_SIZE = len(tokenizer.index_word) + 1
EMBEDDING_DIM = 100




from gensim.models.keyedvectors import KeyedVectors

def get_embeddings(pretrained_vec_path):
    word_vectors = KeyedVectors.load_word2vec_format(pretrained_vec_path, binary=False)
    word_vocab = set(word_vectors.key_to_index.keys())
    embeddings = np.random.uniform(-0.2, 0.2, size=(VOCAB_SIZE, EMBEDDING_DIM))
    for i in range(1, VOCAB_SIZE):
        word = tokenizer.index_word[i]
        if word in word_vocab:
            embeddings[i, :] = word_vectors.get_vector(word)
    return embeddings

pretrained_vec_path = "./word2vec/sg_ns_100.txt"
embeddings = get_embeddings(pretrained_vec_path)
embeddings[:2]




FILTERS = [2, 3, 5]
NUM_FILTERS = 128
DENSE_DIM = 256
CLASS_NUM = 3
DROPOUT_RATE = 0.5

def build_text_cnn_model():
    inputs = tf.keras.Input(shape=(None, ), name='input_data')
    embed = tf.keras.layers.Embedding(
        input_dim=VOCAB_SIZE,
        output_dim=EMBEDDING_DIM,
        embeddings_initializer=tf.keras.initializers.Constant(embeddings),
        mask_zero=True
    )(inputs)
    embed = tf.keras.layers.Dropout(DROPOUT_RATE)(embed)

    pool_outputs = []
    for filter_size in FILTERS:
        conv = tf.keras.layers.Conv1D(NUM_FILTERS,
                                      filter_size,
                                      padding='same',
                                      activation='relu',
                                      data_format='channels_last',
                                      use_bias=True
                                     )(embed)
        max_pool = tf.keras.layers.GlobalMaxPooling1D(data_format='channels_last')(conv)
        pool_outputs.append(max_pool)
    outputs = tf.keras.layers.concatenate(pool_outputs, axis=-1)
    outputs = tf.keras.layers.Dense(DENSE_DIM, activation='relu')(outputs)
    outputs = tf.keras.layers.Dropout(DROPOUT_RATE)(outputs)
    outputs = tf.keras.layers.Dense(CLASS_NUM, activation='softmax')(outputs)
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    return model

text_cnn_model = build_text_cnn_model()
text_cnn_model.summary()



LR = 3e-4
EPOCHS = 10
EARLY_STOP_PATIENCE = 5

loss = tf.keras.losses.CategoricalCrossentropy()
optimizer=tf.keras.optimizers.Adam(LR)


text_cnn_model.compile(loss=loss,
                       optimizer=optimizer,
                       metrics=['accuracy']
                      )


callback = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy',
                                            patience=EARLY_STOP_PATIENCE,  #
                                            restore_best_weights=True #
                                           ) 

class_weight = {0: 0.4, 1: 0.2, 2: 0.4}

history = text_cnn_model.fit(train_dataset,
                             epochs=EPOCHS,
                             callbacks=[callback],
                             validation_data=val_dataset,
                             class_weight=class_weight
                            )

test_loss, test_acc = text_cnn_model.evaluate(test_dataset)  

print('Test Loss:', test_loss)
print('Test Accuracy:', test_acc)



import matplotlib.pyplot as plt

def plot_graphs(history, metric):
    plt.plot(history.history[metric])
    plt.plot(history.history['val_'+metric], '')
    plt.xlabel("Epochs")
    plt.ylabel(metric)
    plt.legend([metric, 'val_'+metric])



plt.figure(figsize=(16, 8))
plt.subplot(1, 2, 1)
plot_graphs(history, 'accuracy')
plt.ylim(None, 1)
plt.subplot(1, 2, 2)
plot_graphs(history, 'loss')
plt.ylim(0, None)


model_save_path = './model/text_cnn'

text_cnn_model.save(model_save_path)


predictions = text_cnn_model.predict(test_dataset)
predictions[:10]

preds = np.argmax(predictions, axis=-1)
preds[:10]


from sklearn.metrics import classification_report


result = classification_report(test_label, preds)
print(result)


tokenizer_save_path = './model/tokenizer.pkl'
tokenizer = joblib.load(tokenizer_save_path)


model_save_path = './model/text_cnn'
text_cnn_model = tf.keras.models.load_model(model_save_path)
text_cnn_model.summary()




predict_sentences = []

predict_texts = [preprocess_text(text) for text in predict_sentences]

predict_sequences = tokenizer.texts_to_sequences(predict_texts)

sequence_padded = pad_sequences(predict_sequences, padding='post', maxlen=MAX_LEN)

predict_logits = text_cnn_model.predict(sequence_padded)
predict_logits


predict_results = np.argmax(predict_logits, axis=1)

predict_labels = [label - 1 for label in predict_results] 
predict_labels


for text, label in zip(predict_sentences, predict_labels):
    print(f'Text: {text}\nPredict: {label}')




LSTM_DIM = 256
DENSE_DIM = 128

text_rnn_model = tf.keras.Sequential([
    tf.keras.layers.Embedding(
        input_dim=VOCAB_SIZE,
        output_dim=EMBEDDING_DIM,
        embeddings_initializer=tf.keras.initializers.Constant(embeddings),
        trainable=True,
        mask_zero=True),
    tf.keras.layers.Dropout(DROPOUT_RATE),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(LSTM_DIM)),
    tf.keras.layers.Dense(DENSE_DIM, activation='relu'),  
    tf.keras.layers.Dropout(DROPOUT_RATE),
    tf.keras.layers.Dense(CLASS_NUM, activation='softmax')
])
text_rnn_model.summary()




labels = [0, 1, 2] 
blance_weights = [0.3, 0.4, 0.3]
dataset_each_label = []

for current_label in labels:

    current_label_dataset = train_dataset.unbatch().filter(lambda example, label: tf.argmax(label)==current_label).repeat()
    dataset_each_label.append(current_label_dataset)


balanced_train_dataset = tf.data.experimental.sample_from_datasets(dataset_each_label, 
                                                                   weights=blance_weights)
balanced_train_dataset = balanced_train_dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE).prefetch(BUFFER_SIZE)




for example, label in balanced_train_dataset.take(1):
    print('texts: ', example.numpy()[:3])
    print()
    print('labels: ', label.numpy()[:3])



text_cnn_model_new = build_text_cnn_model()
text_cnn_model_new.compile(loss=loss,
                           optimizer=optimizer,
                           metrics=['accuracy']
                          )

history = text_cnn_model_new.fit(balanced_train_dataset,
                                 epochs=EPOCHS,
                                 callbacks=[callback],
                                 validation_data=val_dataset,
                                 class_weight=class_weight,
                                 steps_per_epoch=20000,
                                )


predictions = text_cnn_model.predict(test_dataset)
preds = np.argmax(predictions, axis=-1)
result = classification_report(test_label, preds)
print(result)




import tensorflow_addons as tfa

loss = tfa.losses.SigmoidFocalCrossEntropy(from_logits=True)




