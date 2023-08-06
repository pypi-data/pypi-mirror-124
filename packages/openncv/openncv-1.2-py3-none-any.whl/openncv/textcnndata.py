#!/usr/bin/env python
# coding: utf-8



get_ipython().system('ls raw_data/')




import pandas as pd

import warnings
warnings.filterwarnings('ignore')

raw_train_df = pd.read_csv('raw_data/nCoV_100k_train.labled.csv')
raw_train_df.head()


subset=['']

train_df = raw_train_df[subset].dropna(subset=subset).drop_duplicates([''])
train_df[' '] = train_df[' '].apply(lambda x: len(x))
train_df.head()


for col in train_df.columns:
    print(train_df[col].describe())
    print('=' * 100)

train_df[''].unique()

train_df[train_df[''] == 1]

 
train_df['good_sample'] = train_df[''].apply(lambda x: x in ['-1', '0', '1'])
train_df[train_df['good_sample'].isin(['-1','0','1'])][subset].head()


train_df = train_df[train_df['good_sample']][subset]
train_df.rename(columns={' ':'text', ' ': 'label', ' ': 'text_length'}, inplace=True)
train_df.head()



raw_test_df = pd.read_csv('raw_data/nCov_10k_test.csv')
raw_test_df.head()


test_df = raw_test_df[[' ']].dropna().drop_duplicates()
test_df.rename(columns={' ':'text'}, inplace=True)
test_df.describe()


raw_unlabeled_df = pd.read_csv('raw_data/nCoV_900k_train.unlabled.csv')
raw_unlabeled_df.head()

unlabeled_df = raw_unlabeled_df[['微博中文内容']].dropna().drop_duplicates()
unlabeled_df.rename(columns={'微博中文内容':'text'}, inplace=True)
unlabeled_df.describe()



for text in train_df['text'].sample(20):
    print(text)
    print('=' * 100)



import re

pattern = '(//@)[^: ]+\:'
re.sub(pattern, ' ', '')

 
pattern =
re.sub(pattern, '', '    ')

 
pattern = 'https?:\/\/\w+\.[a-z]{2,6}(\/[\da-zA-Z\_\-]*)*'
re.sub(pattern, '====', '    ')
 

def clean_text(text):
    pattern = 'https?:\/\/\w+\.[a-z]{2,6}(\/[\da-zA-Z\_\-]*)*'
    text = re.sub(pattern, ' ', text)
    pattern = '[( )(\?? c?)( \??)]'
    text = re.sub(pattern, ' ', text)
    pattern = '(//@)[^: ]+\:'
    text = re.sub(pattern, ' ', text)
    pattern = '\s{2,}'
    text = re.sub(pattern, ' ', text)
    text = text.strip().lower()
    return text
 


text = '  '
clean_text(text)
 


train_df['text'] = train_df['text'].apply(lambda x: clean_text(x))
train_df = train_df[train_df['text'] != '']
train_df.head()
 

test_df['text'] = test_df['text'].apply(lambda x: clean_text(x))
test_df = test_df[test_df['text'] != '']
test_df.head()
 


unlabeled_df['text'] = unlabeled_df['text'].apply(lambda x: clean_text(x))
unlabeled_df = unlabeled_df[unlabeled_df['text'] != '']
unlabeled_df.head()

 
for label, group in train_df.groupby(by='label'):
    print(label)
    print()
    sentences = group.sample(3)['text'].tolist()
    print('\n\n'.join(sentences))
    print("=" * 30)
 

get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
 

train_df['text_length'] = train_df['text'].apply(lambda x: len(x))
train_df.head()

 
sns.set()
sns.distplot(train_df['text_length'])
plt.show()

 

test_df['text_length'] = test_df['text'].apply(lambda x: len(x))
sns.set()
sns.distplot(test_df['text_length'])
plt.show()

 
plt.figure(figsize=[9,7])
train_df['label'].value_counts().plot.pie(autopct='%1.2f%%')
plt.show()

 

def text_length_bucket(text_length):
    if text_length < 100:
        return '<100'
    elif 100 <= text_length < 140:
        return '100-140'
    else:
        return '>=140'

train_df['text_length_bucket'] = train_df['text_length'].apply(text_length_bucket)

sns.countplot('label',hue='text_length_bucket',data=train_df)

plt.xlabel('length',fontsize=15)
plt.ylabel('count',fontsize=15)
plt.legend(loc='upper right')
plt.show()

 


import jieba

text = ' 。'
words = ' '.join(jieba.lcut(text))
words


# In[31]:


with open('./data/baidu_stopwords.txt', 'r') as f:
    stop_words = f.read().split('\n')

def cut_and_clean(text):
    cuted_text = ' '.join([x for x in jieba.lcut(text) if x not in stop_words and len(x) > 1])
    clean_text = re.sub('([\.，。、“”‘ ’？\?:#：【】\+!！])', ' ', cuted_text)
    clean_text = re.sub('\s{2,}', ' ', clean_text)
    return clean_text

cut_and_clean(text)


# In[32]:


train_text = ' '.join(train_df['text'].apply(cut_and_clean))
train_text[:1000]

 


import wordcloud
WC = wordcloud.WordCloud(font_path='./data/MSYH.TTC', 
                         max_words=1000,
                         height= 600,
                         width=1200,
                         background_color='white',
                         repeat=False,
                         mode='RGBA')


 


word_cloud_img = WC.generate(train_text)
plt.figure(figsize = (20,10))
plt.imshow(word_cloud_img, interpolation='nearest')
plt.axis("off")
WC.to_file('./data/wordcloud.png')

 

# In[35]:


print(f"trian data count: {len(train_df)}")
print(f"test data count: {len(test_df)}")
print(f"unlabeled data count: {len(unlabeled_df)}")

from sklearn.model_selection import train_test_split

##tranlabel [0, 1, 2]
train_df['label'] = train_df['label'].apply(lambda x: int(x)+1).astype(int)
 
train, test = train_test_split(train_df, test_size=10000, random_state=100)

len(train), len(test)


train[['text', 'label']].to_csv('./processed_data/train.csv', index=False, encoding='utf-8')
test[['text', 'label']].to_csv('./processed_data/test.csv', index=False, encoding='utf-8')

unlabeled = pd.concat([train_df[['text']], test_df[['text']], unlabeled_df])
unlabeled.head()
unlabeled.count()

unlabeled.to_csv('./processed_data/unlabeled.csv', index=False, encoding='utf-8')



