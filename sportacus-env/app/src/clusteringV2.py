from sklearn.cluster import KMeans
from sklearn.externals import joblib
import matplotlib.pyplot as plt
import pickle

model = KMeans(n_clusters = 3)
X = [[0,1], [1,0], [2,0],[1,1],[0,2]]
labels = model.fit(X)

joblib.dump(model, 'model.pkl')  
model_loaded = joblib.load('model.pkl')


X.append([2,1])
X.append([1,2])
# predict using the loaded model
pred_y = model.predict(X)
pred_new_y = model_loaded.predict(X)

print("predicted: %s" % labels)
print("predicted: %s" % pred_y)
print("predicted new: %s" % pred_new_y)

# get centroids
centroids = model.cluster_centers_
cen_x = [i[0] for i in centroids] 
cen_y = [i[1] for i in centroids]

colors = ['#DF2020', '#81DF20', '#2095DF']

#Plotting the results
filtered_label0_X = [X[i][0] for i in range(len(X)) if pred_y[i] == 0 ]
filtered_label0_Y = [X[i][1] for i in range(len(X)) if pred_y[i] == 0 ]

filtered_label1_X = [X[i][0] for i in range(len(X)) if pred_y[i] == 1 ]
filtered_label1_Y = [X[i][1] for i in range(len(X)) if pred_y[i] == 1 ]

filtered_label2_X = [X[i][0] for i in range(len(X)) if pred_y[i] == 2 ]
filtered_label2_Y = [X[i][1] for i in range(len(X)) if pred_y[i] == 2 ]


plt.figure()

plt.scatter(filtered_label0_X, filtered_label0_Y, color = 'red')
plt.scatter(filtered_label1_X, filtered_label1_Y, color = 'blue')
plt.scatter(filtered_label2_X, filtered_label2_Y, color = 'black')
plt.scatter(cen_x, cen_y, color = 'green', s=10)

plt.show()