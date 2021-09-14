import os
import glob
import time
start = time.time()

path = '/home/student/Desktop/BD/ipl_csv'
extension = 'csv'
os.chdir(path)
result = [i for i in glob.glob('*.{}'.format(extension))]
print(result)

end = time.time()
print(end - start)
