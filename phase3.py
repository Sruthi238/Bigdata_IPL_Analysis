from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree
from pyspark import SparkConf, SparkContext
from numpy import array
import sys
conf=SparkConf().setMaster("local")
sc=SparkContext(conf=conf)


        
def Runs(fields): 
	BatAve=float(fields[0])
	BatSR=float(fields[1])
	BowlAve=float(fields[2])
	BowlEco=float(fields[3])
	Overs=float(fields[4])
	Run=int(fields[5])
	BatCL=int(fields[6])
	BowlCL=int(fields[7])
	return LabeledPoint(Run, array([BatCL,BowlCL,BatAve,BatSR,BowlAve,BowlEco,Overs]))

rawData=sc.textFile('file:///home/shreyas/Desktop/BD/P2P_1.csv')


csvData=rawData.map(lambda x:x.split(","))
trainingData=csvData.map(Runs)
model=DecisionTree.trainRegressor(trainingData, categoricalFeaturesInfo={},
                                        impurity='variance', maxDepth=10, maxBins=7)

TD=[array([4,0,30.58,123.57,18,6,0.1])]
"""TD=[array(["4","0","30.58","123.57","18.7","6.855","0.1"])]"""
testData=sc.parallelize(TD)
prediction=model.predict(testData)
result=prediction.collect()


print (result)

print('Learned classification tree model:')
print(model.toDebugString())
