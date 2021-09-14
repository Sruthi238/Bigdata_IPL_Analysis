from __future__ import print_function
import csv
import time
import os
import glob


start = time.time()

batVul={}
path = '/home/shreyas/Desktop/BD/ipl_csv'
extension = 'csv'
os.chdir(path)
filelinks = [i for i in glob.glob('*.{}'.format(extension))]

for ipl in filelinks:
	i=path+"/"+ipl
	with open(i,'r+') as csvfile:
		csvreader = csv.reader(csvfile)
		for row in csvreader:	
			if len(row)<9:
				continue
			if row[9]!="run out" and row[9]!="":
				bat=row[10]
				bowl=row[6]
				if bat in batVul:
					if bowl in batVul[bat]:
						batVul[bat][bowl]+=1
					else:
						batVul[bat][bowl]=1
				else:
					batVul[bat]={}
					batVul[bat][bowl]=1
	csvfile.close()
"""for a in batVul.keys():
	for c in batVul[a].keys():
		print (a,c,batVul[a][c])"""

f1=open('batvul', 'w')

for a in batVul.keys():
	maxValue = max(batVul[a].values())  #<-- max of values
	st=str(a)+" is Vulnerable to "+str([key for key in batVul[a] if batVul[a][key]==maxValue])+" and has got out "+str(maxValue)+" times.\n"
	f1.write(st)

end = time.time()
print(end - start)
f1.close()
