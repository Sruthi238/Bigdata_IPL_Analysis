import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

df_bowler = pd.read_csv('file:///home/shreyas/Downloads/bowling.csv')
df_bowler = df_bowler[['Ave','Eco']]

mms = MinMaxScaler()
mms.fit(df_bowler)
dft = mms.transform(df_bowler)


Sum_of_squared_distances_bwl = []
K = range(1,20)
for k in K:
    km = KMeans(n_clusters=k)
    km = km.fit(dft)
    Sum_of_squared_distances_bwl.append(km.inertia_)
print(Sum_of_squared_distances_bwl)
print(len(Sum_of_squared_distances_bwl))


plt.plot(K, Sum_of_squared_distances_bwl, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum_of_squared_distances')
plt.title('Elbow Method For Optimal k')
plt.show()

