#!/usr/bin/env python
# coding: utf-8
path = './input/xAPI-Edu-Data.csv'

import pandas as pd 
pandas_data = pd.read_csv(path)
print(pandas_data.shape)
pandas_data.head()
str_columns = pandas_data.dtypes[pandas_data.dtypes == 'object'].index

from pyspark import SparkContext
#设置运行模式为本地，应用名称为student
sc=SparkContext('local','student')
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)
data = sqlContext.read.csv(path, 
                        header=True, 
                        inferSchema=True)
data.show(3)
cols = data.columns
print(cols)
print(len(cols))
data.describe(cols[:10]).show()
data.describe(cols[10:]).show()
data.groupBy('gender').count().show()
data.groupBy('Class').count().show()
from pyspark.ml.feature import StringIndexer

for col in str_columns:
    indexer = StringIndexer(inputCol=col, outputCol=col+'Index')
    data = indexer.fit(data).transform(data)
#删除未转换格式的列
for col in str_columns:
    data = data.drop(col)
data.show(2)
columns = data.columns
print(columns)
from pyspark.ml.feature import OneHotEncoder
selected_features = columns[4:-1]
#创建编码规则并对列进行编码
encoder = OneHotEncoder(inputCols=selected_features,
                             outputCols=[i + 'vec' for i in selected_features])
data_encodered = encoder.fit(data).transform(data)
#删除未编码列
for col in selected_features:
    data_encodered = data_encodered.drop(col)
data_encodered.show(2)
encodered_columns = data_encodered.columns
encodered_columns.remove('ClassIndex')
#创建features列
import pyspark.ml.feature as ft
featuresCreator = ft.VectorAssembler(
    inputCols=encodered_columns, 
    outputCol='features')
data_encodered=featuresCreator.transform(data_encodered)
from pyspark.ml.classification import LogisticRegression
logistic = LogisticRegression(
    maxIter=10,#最大迭代次数
    regParam=0.1, #Elastic net正则化(同时包含L1和L2正则化)系数
    labelCol='ClassIndex')#目标变量

train, test = data_encodered     .randomSplit([0.7, 0.3], seed=1)

lrmodel=logistic.fit(train)
test_model = lrmodel.transform(test)

test_model.select('prediction').show()
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
#模型评估
evaluator = MulticlassClassificationEvaluator(
    predictionCol='prediction', #预测结果列
    labelCol='ClassIndex')#目标变量列
print('LR_Accuracy:{0:.3f}'.format(evaluator.evaluate(test_model, {evaluator.metricName: "accuracy"})))

import pyspark.ml.tuning as tune
# 指定模型
logistic = LogisticRegression(labelCol='ClassIndex')
# 指定要循环遍历的参数列表
# 最大迭代次数调优
# Elastic net正则化(同时包含L1和L2正则化)系数调优
grid = tune.ParamGridBuilder().addGrid(logistic.maxIter, [2,10,30,50])               .addGrid(logistic.regParam,[0.01,0.05,0.1,0.15]).build()
evaluator2 = MulticlassClassificationEvaluator(
    predictionCol='prediction', #预测结果列
    labelCol='ClassIndex')#目标变量列

cv = tune.CrossValidator(estimator=logistic,#选择模型
                         estimatorParamMaps=grid,#参数列表
                         evaluator=evaluator2)#模型评估
# 寻找模型的最佳参数组合
cvModel2 = cv.fit(train)
# 使用最佳模型做出预测
test_model2 = cvModel2.transform(test)

print('LR_gd_Accuracy:{0:.3f}'      .format(evaluator2.evaluate(test_model2, {evaluator2.metricName: "accuracy"})))

from pyspark.ml.classification import RandomForestClassifier
#设置随机森林中决策树个数为10
rf = RandomForestClassifier(labelCol="ClassIndex", #目标列
                            featuresCol="features", #特征列
                            numTrees=10)#设置随机森林中决策树个数为10

train, test = data_encodered     .randomSplit([0.7, 0.3], seed=1)
#训练模型
rf_model=rf.fit(train)
#对测试集进行预测
test_model = rf_model.transform(test)


test_model.select('prediction').show()


from pyspark.ml.evaluation import MulticlassClassificationEvaluator
#模型评估
evaluator = MulticlassClassificationEvaluator(
    predictionCol='prediction',#预测结果列 
    labelCol='ClassIndex')#目标变量列

print('RF_Accuracy:{0:.3f}'      .format(evaluator.evaluate(test_model, {evaluator.metricName: "accuracy"})))

import pyspark.ml.tuning as tune

rf = RandomForestClassifier(labelCol="ClassIndex",                             featuresCol="features")
# 建树个数调优
grid = tune.ParamGridBuilder()                 .addGrid(rf.numTrees, [10,20,50,100,150,200])                 .build()

evaluator2 = MulticlassClassificationEvaluator(
    predictionCol='prediction', #预测结果列
    labelCol='ClassIndex')#目标变量列
cv = tune.CrossValidator(estimator=rf,#选择模型
                         estimatorParamMaps=grid,#参数列表
                         evaluator=evaluator2)#模型评估
cvModel2 = cv.fit(train)
#对测试集进行预测
test_model2 = cvModel2.transform(test)
print('RF_gd_Accuracy:{0:.2f}'      .format(evaluator2.evaluate(test_model2, {evaluator2.metricName: "accuracy"})))

cvModel2.bestModel


