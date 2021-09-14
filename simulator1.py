import random
import math
import csv
import pandas as pd
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
                                        impurity='variance', maxDepth=30, maxBins=128)

bat_clust = dict()
bowl_clust = dict()
team1 = []
team2 = []

with open('/home/shreyas/Downloads/BD_proj/matches/SRHvsRR.csv') as csvFile:
	reader = csv.reader(csvFile)
	next(reader)
	for row in reader:
		team1.append(row[0])
		team2.append(row[1])
csvFile.close()

player_prob = pd.read_csv('P2Pstat.csv')

def innings1(team1, team2):
	striker = team1[0]
	non_striker = team1[1]
	bowler = team2[len(team2)-1]
	nextbatsman = 2
	wick = 0
	runs = 0
	overs = 0.0
	prob = 0
	count = 2
	nprob = 1
	dic = {}
	dic[striker] = 1
	dic[non_striker]=1
	while(overs<20.0 and wick < 10):
		balls = 1
		while(balls<6 and wick <10):
			row = [0,0,30.0,100.0,20.0,6.000]
			try:
				row1 = player_prob.loc[player_prob['batsman'] == striker].loc[player_prob['bowler'] == bowler]
				row[0]=int(row1["BatCL"])
				row[1]=int(row1["BwlCL"])
				row[2]=float(row1["BatAvg"])
				row[3]=float(row1["BatSR"])
				row[4]=float(row1["BwlAvg"])
				row[5]=float(row1["BwlEco"])
			except:
				row = [0,0,30.0,100.0,20.0,6.000]
			score = 0
			flag = 0
			ov=0.0
			ov=overs+(balls/10.0)
			TD=[array([row[0],row[1],row[2],row[3],row[4],row[5],ov])]
			testData=sc.parallelize(TD)
			prediction=model.predict(testData)
			result=prediction.collect()
			print (result[0])
			result[0]*=1.5
			if (math.ceil(result[0])<=6):
				score = math.ceil(result[0])
				if score==5:
					score+=1
			else:
				wick = wick+1
				striker = team1[nextbatsman]
				nextbatsman = (nextbatsman+1)%11
				flag = 1
				dic[striker] = 1
			if(flag==0):
				runs = runs+score
				if (score==1 or score == 3):
					striker,non_striker = non_striker,striker
			balls = balls+1
		striker,non_striker = non_striker,striker                 
		bowler = team2[len(team2)-count]                    
		count = (count+1)%5 + 1 
		overs = overs+1
	return runs,wick

def innings2(team1, team2,runs1):
	striker = team1[0]
	non_striker = team1[1]
	bowler = team2[len(team2)-1]
	nextbatsman = 2
	wick = 0
	runs = 0
	overs = 0.0
	prob = 0
	count = 2
	nprob = 1
	dic = {}
	dic[striker] = 1
	dic[non_striker]=1
	while(overs<20.0 and wick < 10):
		balls = 1
		while(balls<6 and runs<=runs1 and wick <10):
			row = [0,0,30.0,100.0,20.0,6.000]
			try:
				row1 = player_prob.loc[player_prob['batsman'] == striker].loc[player_prob['bowler'] == bowler]
				row[0]=int(row1["BatCL"])
				row[1]=int(row1["BwlCL"])
				row[2]=float(row1["BatAvg"])
				row[3]=float(row1["BatSR"])
				row[4]=float(row1["BwlAvg"])
				row[5]=float(row1["BwlEco"])
			except:
				row = [0,0,30.0,100.0,20.0,6.000]
			score = 0
			flag = 0
			ov=0.0
			ov=overs+(balls/10.0)
			TD=[array([row[0],row[1],row[2],row[3],row[4],row[5],ov])]
			testData=sc.parallelize(TD)
			prediction=model.predict(testData)
			result=prediction.collect()
			print(result[0])
			result[0]*=1.5
			if (math.ceil(result[0])<=6):
				score = math.ceil(result[0])
				if score==5:
					score+=1
			else:
				wick = wick+1
				striker = team1[nextbatsman]
				nextbatsman = (nextbatsman+1)%11
				flag = 1
				dic[striker] = 1
			if(flag==0):
				runs = runs+score
				if (score==1 or score == 3):
					striker,non_striker = non_striker,striker
			balls = balls+1
		striker,non_striker = non_striker,striker                 
		bowler = team2[len(team2)-count]                    
		count = (count+1)%5 + 1 
		overs = overs+1
		if (runs>runs1):
			break
	return runs,wick

runs1 ,wicks1 = innings1(team1,team2)
runs2 ,wicks2 = innings2(team2,team1,runs1)
print(runs1,wicks1)
print(runs2,wicks2)
