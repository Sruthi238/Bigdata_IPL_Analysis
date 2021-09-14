import random
import csv
import pandas as pd 

bat_CL=dict()
bl_CL=dict()

files1 = pd.read_csv('bat_cl.csv')
for i in range(len(files1)):
	batname = files1.loc[i].batsman.strip()     
	bat_CL[batname] = files1.loc[i].batclustno
files3 = pd.read_csv('bowl_cl.csv')
for i in range(len(files3)):
	blname = files3.loc[i].bowler.strip()     
	bl_CL[blname] = files3.loc[i].bowlclustno
	
l=[]
l1=[]
files2 = pd.read_csv('player-stat.csv')
for i in range(len(files2)):
	batname2 = files2.loc[i].Batsman.strip()
	blname2 = files2.loc[i].Bowler.strip()
	l1=files2.loc[i].tolist()
	try:
		l1.append(bat_CL[batname2])
	except:
		l1.append(0)
	try:
		l1.append(bl_CL[blname2])
	except:
		l1.append(0)
	
	l.append(l1)
	l1=[]
	#print(batname2)
	
	
with open('P2P.csv','w') as f:
	writer = csv.writer(f)
	writer.writerows(l)
f.close()


