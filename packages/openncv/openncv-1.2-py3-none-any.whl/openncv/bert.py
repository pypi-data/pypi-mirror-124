#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
import tensorflow as tf

import warnings
warnings.filterwarnings('ignore')


train_df = pd.read_csv('./dataset/train.csv')
val_df = pd.read_csv('./dataset/val.csv')
test_df = pd.read_csv('./dataset/test.csv')
val_df.head()

from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

test_sentence =


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

def convert_sample_to_feature(text, max_length):
    return tokenizer.encode_plus(text, 
                                 add_special_tokens=True, 
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

def build_dataset(df, max_length):
    input_ids_list = []
    token_type_ids_list = []
    attention_mask_list = []
    label_list = []
    for _, row in df.iterrows():
        text, label = row["text"], row["label"]
        bert_input = convert_sample_to_feature(text, max_length)  #
        input_ids_list.append(bert_input['input_ids'])
        token_type_ids_list.append(bert_input['token_type_ids'])
        attention_mask_list.append(bert_input['attention_mask'])
        label_list.append([label])
    dataset = tf.data.Dataset.from_tensor_slices((input_ids_list, attention_mask_list, token_type_ids_list, label_list))
    dataset = dataset.map(map_sample_to_dict)
    return dataset


BATCH_SIZE = 32
MAX_SEQ_LEN = 240
NUM_LABELS = 3
BUFFER_SIZE = len(train_df)

train_dataset = build_dataset(train_df, MAX_SEQ_LEN).shuffle(BUFFER_SIZE).batch(BATCH_SIZE).prefetch(BUFFER_SIZE)
val_dataset = build_dataset(val_df, MAX_SEQ_LEN).batch(BATCH_SIZE)
test_dataset = build_dataset(test_df, MAX_SEQ_LEN).batch(BATCH_SIZE)


from transformers import TFBertForSequenceClassification

model = TFBertForSequenceClassification.from_pretrained('bert-base-chinese',
                                                        num_labels=NUM_LABELS
                                                       )

LR = 3e-6
EPOCHS = 5
PATIENCE = 1
optimizer = tf.keras.optimizers.Adam(learning_rate=LR)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
metric = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')
model.compile(optimizer=optimizer,
              loss=loss,
              metrics=[metric])
callback = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy',
                                            patience=PATIENCE,
                                            restore_best_weights=True)

bert_history = model.fit(train_dataset,
                         epochs=EPOCHS,
                         callbacks=[callback],
                         validation_data=val_dataset)

save_model_path = "./bert/bert_classification"
model.save_pretrained(save_model_path, saved_model=True)

output = model.predict(test_dataset)
output

preds = np.argmax(output.logits, axis=-1)

preds[:10]

from sklearn.metrics import classification_report
test_label = test_df['label']
result = classification_report(test_label, preds)
print(result)

save_model_path = "./bert/bert_classification"
saved_model = TFBertForSequenceClassification.from_pretrained(save_model_path, 
                                                              num_labels=NUM_LABELS)
saved_model.summary()

predict_sentences = []

predict_inputs = tokenizer(predict_sentences,
                           padding=True,
                           max_length=MAX_SEQ_LEN, 
                           return_tensors="tf")
output = saved_model(predict_inputs)

predict_logits = output.logits.numpy()

predict_logits
predict_results = np.argmax(predict_logits, axis=1)
predict_labels = [label - 1 for label in predict_results]
predict_labels

for text, label in zip(predict_sentences, predict_labels):
    print(f'文本: {text}\n预测标签: {label}')
from transformers import TFBertModel

bert_model = TFBertModel.from_pretrained('bert-base-chinese')
input_ids = tf.keras.layers.Input(shape=(MAX_SEQ_LEN,), name='input_ids', dtype='int32')
token_type_ids = tf.keras.layers.Input(shape=(MAX_SEQ_LEN,), name='token_type_ids', dtype='int32')
attention_masks = tf.keras.layers.Input(shape=(MAX_SEQ_LEN,), name='attention_mask', dtype='int32') 
embedding_layer = bert_model(input_ids, attention_masks)[0]
X = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(100,
                                                       return_sequences=True,
                                                       dropout=0.1))(embedding_layer)
X = tf.keras.layers.GlobalMaxPool1D()(X)
X = tf.keras.layers.BatchNormalization()(X) 
X = tf.keras.layers.Dense(256, activation='relu')(X)
X = tf.keras.layers.Dropout(0.5)(X)
y = tf.keras.layers.Dense(3, activation='softmax', name='outputs')(X)

model = tf.keras.Model(inputs=[input_ids, attention_masks, token_type_ids], outputs = y)

for layer in model.layers[:3]:
     layer.trainable = False
model.summary()


