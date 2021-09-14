import csv
import time
import os
import glob
start = time.time()

bowlVul={}
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
			if int(row[7])!=0:
				bat=row[4]
				bowl=row[6]
				if bowl in bowlVul:
					if bat in bowlVul[bowl]:
						bowlVul[bowl][bat]+=int(row[7])
					else:
						bowlVul[bowl][bat]=int(row[7])
				else:
					bowlVul[bowl]={}
					bowlVul[bowl][bat]=int(row[7])
	csvfile.close()
"""
for a in bowlVul.keys():
	for c in bowlVul[a].keys():
		print (a,c,bowlVul[a][c])
"""

f1=open('bowlvul', 'w')
for a in bowlVul.keys():
	maxValue = max(bowlVul[a].values())  #<-- max of values
	st=str(a)+" is Vulnerable to "+str([key for key in bowlVul[a] if bowlVul[a][key]==maxValue])+" and has given "+str(maxValue)+" runs.\n"
	f1.write(st)

end = time.time()
print(end - start)
f1.close()

