import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

df_batsman = pd.read_csv('file:///home/shreyas/Downloads/batting.csv')
df_batsman = df_batsman[['Ave' ,'SR']]

mms = MinMaxScaler()
mms.fit(df_batsman)
dft = mms.transform(df_batsman)


Sum_of_squared_distances_bat = []
K = range(1,20)
for k in K:
    km = KMeans(n_clusters=k)
    km = km.fit(dft)
    Sum_of_squared_distances_bat.append(km.inertia_)
print(Sum_of_squared_distances_bat)
print(len(Sum_of_squared_distances_bat))


plt.plot(K, Sum_of_squared_distances_bat, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum_of_squared_distances')
plt.title('Elbow Method For Optimal k')
plt.show()

