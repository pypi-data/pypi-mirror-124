#!/usr/bin/env python
# coding: utf-8

from pyspark import SparkContext
#设置运行模式为本地，应用名称为bank
sc=SparkContext('local','bank')

from pyspark.sql import SQLContext
#读入并输出数据
sqlContext = SQLContext(sc)
#读入数据
bank_df=sqlContext.read.csv('input/bank.csv',header=True,inferSchema=True)
#显示数据
bank_df.show(10)
bank_df.printSchema()
bank_df.groupBy('deposit').count().show()
bank_df=bank_df.drop('day','month')

categoricalColumns = ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'poutcome']

from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
#生成机器学习流水线stage变量
stages = []
for categoricalCol in categoricalColumns:
    #进行数值编码
    stringIndexer = StringIndexer(inputCol = categoricalCol, outputCol = categoricalCol + 'Index')
    #进行独热编码
    encoder = OneHotEncoder(inputCols=[stringIndexer.getOutputCol()], outputCols=[categoricalCol + "classVec"])
    stages += [stringIndexer, encoder]
stages

label_stringIdx = StringIndexer(inputCol = 'deposit', outputCol = 'label')
stages += [label_stringIdx]
numericCols = ['age', 'balance', 'duration', 'campaign', 'pdays', 'previous']
assemblerInputs = [c + "classVec" for c in categoricalColumns] + numericCols
#添加features列
assembler = VectorAssembler(inputCols=assemblerInputs, outputCol="features")
stages += [assembler]
from pyspark.ml import Pipeline
#创建流水线
pipeline = Pipeline(stages = stages)
#生成实例
pipelineModel = pipeline.fit(bank_df)
#对数据集进行预处理操作
bank_df = pipelineModel.transform(bank_df)
bank_df.printSchema()

bank_df=bank_df.select('features','label')
#显示DataFrame
bank_df.show(10)

train, test = bank_df.randomSplit([0.7, 0.3])

from pyspark.ml.classification import LogisticRegression
#设置模型的相关参数
lr = LogisticRegression(featuresCol = 'features', #特征值列
                        labelCol = 'label', #目标值列
                        maxIter=10)#最大迭代次数
#模型训练
lrModel = lr.fit(train)

get_ipython().system('pip install --upgrade pip')

get_ipython().system('pip install matplotlib pandas')

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

#输出模型的参数
trainingSummary = lrModel.summary
#将ROC相关数据转化为Pandas-DataFrame
roc = trainingSummary.roc.toPandas()
#绘图
plt.plot(roc['FPR'],roc['TPR'])
plt.ylabel('False Positive Rate')
plt.xlabel('True Positive Rate')
plt.title('ROC Curve')
plt.show()
#输出ROC曲线下面积
print('Training set area Under ROC: ' + str(trainingSummary.areaUnderROC))

predictions = lrModel.transform(test)
#得到预测结果前10行
predictions.show(10)

from pyspark.ml.evaluation import BinaryClassificationEvaluator
#创建评估器
evaluator = BinaryClassificationEvaluator()
#打印结果
print('Test Accuracy', evaluator.evaluate(predictions))

from pyspark.ml.classification import DecisionTreeClassifier
#设置决策树模型相关参数
dt = DecisionTreeClassifier(featuresCol = 'features', #特征值列
                            labelCol = 'label')#目标值列
#训练模型
dtModel = dt.fit(train)
#对测试集进行预测
predictions = dtModel.transform(test)
#输出预测结果
predictions.show(10)

evaluator = BinaryClassificationEvaluator()
#打印结果
print("Test Accuracy: " + str(evaluator.evaluate(predictions)))

from pyspark.ml.classification import RandomForestClassifier
#创建随机森林模型
rf = RandomForestClassifier(featuresCol = 'features', #特征值列
                            labelCol = 'label',#目标值列
                            numTrees=10)#建树数量
#训练模型
rfModel = rf.fit(train)
#对测试集进行预测
predictions = rfModel.transform(test)
#输出预测结果
predictions.show(10)

evaluator = BinaryClassificationEvaluator()
#输出预测结果
print("Test Accuracy: " + str(evaluator.evaluate(predictions)))

from pyspark.ml.classification import GBTClassifier
#创建GBDT模型
gbt = GBTClassifier(featuresCol = 'features', #特征值列
                    labelCol = 'label',#目标值列
                    maxIter=10)#最大迭代次数
#训练模型
gbtModel = gbt.fit(train)
#对测试集进行预测
predictions = gbtModel.transform(test)
#输出预测结果
predictions.show(10)

evaluator = BinaryClassificationEvaluator()
#输出预测结果
print("Test Accuracy: " + str(evaluator.evaluate(predictions)))

from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
#调整参数
paramGrid = (ParamGridBuilder()
             .addGrid(gbt.maxDepth, [2, 4, 6])#最大建树深度
             .addGrid(gbt.maxBins, [20, 60])#最大装箱数
             .addGrid(gbt.maxIter, [10, 20])#最大迭代次数
             .build())
#生成调优模型
cv = CrossValidator(estimator=gbt, #选择模型
                    estimatorParamMaps=paramGrid, #参数列表
                    evaluator=evaluator)#模型评估
#训练模型
cvModel = cv.fit(train)
#对测试集进行预测
predictions = cvModel.transform(test)
#对预测结果进行评估
evaluator.evaluate(predictions)





