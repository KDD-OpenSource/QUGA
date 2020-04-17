import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tikzplotlib as tikz

data_train = pd.read_csv('ECG5000_TRAIN', sep= ',', header = None)
data_test = pd.read_csv('ECG5000_TEST', sep= ',', header = None)

data = pd.concat([data_train, data_test])
data = data_train

# filter points for the two classes
# get label and last 35 points in each data point
# check for both boxes whether each point is in one of them
# report the ratio

# class0bounds_106_140 = np.array([[1.27,1.77],[1.25,1.75],[1.13,1.63],[0.98,1.48],[0.80,1.30],[0.59,1.09],[0.34,0.84],[0.08,0.58],[-0.11,0.39],[-0.18,0.32],[-0.25,0.25],[-0.32,0.18],[-0.41,0.09],[-0.44,0.06],[-0.42,0.08],[-0.42,0.08],[-0.46,0.04],[-0.54,-0.04],[-0.54,-0.04],[-0.44,0.06],[-0.46,0.04],[-0.42,0.08],[-0.39,0.11],[-0.33,0.17],[-0.08,0.42],[0.34,0.84],[0.64,1.14],[0.73,1.23],[0.80,1.30],[0.77,1.27],[0.54,1.04],[0.29,0.79],[0.20,0.70],[0.11,0.61],[0.12,0.62]])

# class1bounds_106_140 = np.array([[0.50,1.00],[0.48,0.98],[0.48,0.98],[0.49,0.99],[0.51,1.01],[0.50,1.00],[0.51,1.01],[0.52,1.02],[0.49,0.99],[0.46,0.96],[0.43,0.93],[0.40,0.90],[0.34,0.84],[0.28,0.78],[0.23,0.73],[0.19,0.69],[0.13,0.63],[0.06,0.56],[-0.00,0.50],[-0.08,0.42],[-0.16,0.34],[-0.27,0.23],[-0.34,0.16],[-0.41,0.09],[-0.57,-0.07],[-0.80,-0.30],[-1.07,-0.57],[-1.50,-1.00],[-2.01,-1.51],[-2.53,-2.03],[-2.99,-2.49],[-3.30,-2.80],[-3.51,-3.01],[-2.99,-2.49],[-2.72,-2.22]])
# print(class1bounds_106_140)
# class1bounds_106_140[:,0] = class1bounds_106_140[:,0] -0.25
# class1bounds_106_140[:,1] = class1bounds_106_140[:,1] +0.25
# print(class1bounds_106_140)


# classData = [data[data[0]==i].iloc[:,106:141] for i in range(1,6)]
classData = [data[data[0]==i] for i in range(1,6)]

# print(class0bounds_106_140[:,0].shape)
# print(classData[0][[classData[0] > class0bounds_106_140[:,0]]])
# print([(classData[0] > class0bounds_106_140[:,0]) & (classData[0] < class0bounds_106_140[:,1])][0].shape)
# boundLabelsDataClass0 = (classData[0] > class0bounds_106_140[:,0]) & (classData[0] < class0bounds_106_140[:,1])
# boundLabelsDataClass1 = (classData[1] > class1bounds_106_140[:,0]) & (classData[0] < class1bounds_106_140[:,1])
# counts the number of 'true's for each datapoint
# print(boundLabelsDataClass0.transpose().sum().max())
# print(boundLabelsDataClass1.transpose().sum().max())

# for timeseries in classData[0].transpose().iteritems():
# 	print(np.array(timeseries))
# 	print(np.array(timeseries).shape)
# 	print(np.array(timeseries)[1])
# 	print(np.array(timeseries)[1].shape)
# 	print(np.array(timeseries)[1,1])
# 	if np.array(timeseries)[1][1] > class0bounds_106_140[:,0]:
# 		print(timeseries)
# # 	print(timeseries.iloc[105:140])t
# # 	print(class0bounds_106_140[:,0])
# # 		# print(timeseries)
	# print(timeseries)
# print(classData[0][classData[0].transpose().iloc[105:140] > class0bounds_106_140[:,0]].head())


print(classData[0].shape)
print(classData[1].shape)
# print(data_train[data_train[0]==5])
# print(classData)
# for i in range(5):
# 	print(classData[i].shape)
# # print(ClassData[1].shape)
# # print(data_train[0].unique())
# # print(data[0].count())
# # print(data[data[0]==1].count())
# data.drop(columns = [0], inplace = True)
for elem in classData:
	print(elem.shape)

# class0Samples = classData[0].transpose().sample(n = 200, axis = 1)
fig, ax = plt.subplots(1, sharey = True, figsize = (20,10))
# for i in range(5):
	# print(classData[i].transpose().iloc[:,1:].shape)
classData[0].transpose().sample(n=50, axis = 1).iloc[1:,:].plot(ax = ax, legend = False, alpha = 0.5, grid = True, color = 'blue', linewidth = 0.5)
classData[1].transpose().sample(n=50, axis = 1).iloc[1:,:].plot(ax = ax, legend = False, alpha = 0.5, grid = True, color = 'blue', linewidth = 0.5)
classData[2].transpose().sample(n=5, axis = 1).iloc[1:,:].plot(ax = ax, legend = False, alpha = 0.05, grid = True, color = 'blue', linewidth = 0.5)
classData[3].transpose().sample(n=5, axis = 1).iloc[1:,:].plot(ax = ax, legend = False, alpha = 0.05, grid = True, color = 'blue', linewidth = 0.5)
classData[4].transpose().sample(n=1, axis = 1).iloc[1:,:].plot(ax = ax, legend = False, alpha = 0.05, grid = True, color = 'blue', linewidth = 0.5)
# class0Samples.plot(ax = ax, legend = False, alpha = 0.1, grid = True, color = 'blue')
# classData[0].transpose().iloc[:,:20].plot(ax = ax, legend = False, alpha = 0.1, grid = True, color = 'blue')
# classData[1].transpose().iloc[:,:20].plot(ax = ax, legend = False, alpha = 0.1, grid = True, color = 'red')
# print(classData)
start, end = ax.get_ylim()
ax.yaxis.set_ticks(np.arange(-6, 5, 1))
# class0prototype = class0Samples.mean(axis = 1)
# class0lowerBound = class0Samples.min(axis = 1)
# class0upperBound = class0Samples.max(axis = 1)
# class0lowerBoundImage = class0prototype - 0.25
# class0upperBoundImage = class0prototype + 0.25
# class0lowerBoundImage[:35] =  class0lowerBoundImage[:35] - 1.359
# class0upperBoundImage[:35] =  class0upperBoundImage[:35] + 1.359
# class0lowerBoundImage[35:70] =  class0lowerBoundImage[35:70] - 1.016
# class0upperBoundImage[35:70] =  class0upperBoundImage[35:70] + 1.016
# class0lowerBoundImage[70:105] =  class0lowerBoundImage[70:105] - 0.828
# class0upperBoundImage[70:105] =  class0upperBoundImage[70:105] + 0.828
# class0lowerBoundImage[105:140] =  class0lowerBoundImage[105:140] -1.078
# class0upperBoundImage[105:150] =  class0upperBoundImage[105:150] +1.078

# class0prototype.plot(ax = ax, legend = False, alpha = 1, color = 'red')
# class0lowerBound.plot(ax = ax, legend = False, alpha = 1, color = 'orange')
# class0upperBound.plot(ax = ax, legend = False, alpha = 1, color = 'orange')
# # class0lowerBoundImage.plot(ax = ax, legend = False, alpha = 1, color = 'green')
# # class0upperBoundImage.plot(ax = ax, legend = False, alpha = 1, color = 'green')
# # class0prototype.plot(ax = ax, legend = False, alpha = 1, color = 'red')
# # class0lowerBound.plot(ax = ax, legend = False, alpha = 1, color = 'red')
# # class0upperBound.plot(ax = ax, legend = False, alpha = 1, color = 'red')
# # class0lowerBoundImage.iloc[:35].plot(ax = ax, legend = False, alpha = 1, color = 'red')
# # class0upperBoundImage.iloc[:35].plot(ax = ax, legend = False, alpha = 1, color = 'red')
# class0lowerBoundImage.plot(ax = ax, legend = False, alpha = 1, color = 'red')
# class0upperBoundImage.plot(ax = ax, legend = False, alpha = 1, color = 'red')

# # class0bounds = pd.concat([class0lowerBound, class0upperBound],axis = 1)

# # class0bounds_0_35 = pd.concat([class0lowerBound, class0upperBound],axis = 1).iloc[:35]
# # class0bounds_36_70 = pd.concat([class0lowerBound, class0upperBound],axis = 1).iloc[35:70]
# # class0bounds_71_105 = pd.concat([class0lowerBound, class0upperBound],axis = 1).iloc[70:105]
# # class0bounds_106_140 = pd.concat([class0lowerBound, class0upperBound],axis = 1).iloc[105:140]

# # class0bounds.to_csv('class0Bounds.csv', index = False, line_terminator = '][\n', float_format = '%.2f')
# # class0bounds_0_35.to_csv('class0bounds_0_35.csv', index = False, line_terminator = '][\n', float_format = '%.2f')
# # class0bounds_36_70.to_csv('class0bounds_36_70.csv', index = False, line_terminator = '][\n', float_format = '%.2f')
# # class0bounds_71_105.to_csv('class0bounds_71_105.csv', index = False, line_terminator = '][\n', float_format = '%.2f')
# # class0bounds_106_140.to_csv('class0bounds_106_140.csv', index = False, line_terminator = '][\n', float_format = '%.2f')




# class1prototype = classData[1].transpose().sample(n = 20, axis = 1).mean(axis = 1)
# class1lowerBound = class1prototype - 0.25
# class1upperBound = class1prototype + 0.25
# class1lowerBoundImage = class1prototype - 0.25
# class1upperBoundImage = class1prototype + 0.25
# class1lowerBoundImage[:35] =  class1lowerBoundImage[:35] - 1.453
# class1upperBoundImage[:35] =  class1upperBoundImage[:35] + 1.453
# class1lowerBoundImage[35:70] =  class1lowerBoundImage[35:70] - 0.766
# class1upperBoundImage[35:70] =  class1upperBoundImage[35:70] + 0.766
# class1lowerBoundImage[70:105] =  class1lowerBoundImage[70:105] - 0.766
# class1upperBoundImage[70:105] =  class1upperBoundImage[70:105] + 0.766
# class1lowerBoundImage[105:140] =  class1lowerBoundImage[105:140] -0.953
# class1upperBoundImage[105:150] =  class1upperBoundImage[105:150] +0.953


# # class1prototype.plot(ax = ax, legend = False, alpha = 1, color = 'red')
# # class1lowerBound.plot(ax = ax, legend = False, alpha = 1, color = 'orange')
# # class1upperBound.plot(ax = ax, legend = False, alpha = 1, color = 'orange')
# # class1lowerBoundImage.plot(ax = ax, legend = False, alpha = 1, color = 'green')
# # class1upperBoundImage.plot(ax = ax, legend = False, alpha = 1, color = 'green')
# # class1prototype.plot(ax = ax, legend = False, alpha = 1, color = 'green')
# # class1lowerBound.plot(ax = ax, legend = False, alpha = 1, color = 'green')
# # class1upperBound.plot(ax = ax, legend = False, alpha = 1, color = 'green')
# # class1lowerBoundImage.iloc[106:140].plot(ax = ax, legend = False, alpha = 1, color = 'green')
# # class1upperBoundImage.iloc[106:140].plot(ax = ax, legend = False, alpha = 1, color = 'green')
# class1lowerBoundImage.plot(ax = ax, legend = False, alpha = 1, color = 'green')
# class1upperBoundImage.plot(ax = ax, legend = False, alpha = 1, color = 'green')


# # class1bounds = pd.concat([class1lowerBound, class1upperBound],axis = 1)

# # class1bounds_0_35 = pd.concat([class1lowerBound, class1upperBound],axis = 1).iloc[:35]
# # class1bounds_36_70 = pd.concat([class1lowerBound, class1upperBound],axis = 1).iloc[35:70]
# # class1bounds_71_105 = pd.concat([class1lowerBound, class1upperBound],axis = 1).iloc[70:105]
# # class1bounds_106_140 = pd.concat([class1lowerBound, class1upperBound],axis = 1).iloc[105:140]

# # class1bounds.to_csv('class1Bounds.csv', index = False, line_terminator = '][\n', float_format = '%.2f')
# # class1bounds_0_35.to_csv('class1bounds_0_35.csv', index = False, line_terminator = '][\n', float_format = '%.2f')
# # class1bounds_36_70.to_csv('class1bounds_36_70.csv', index = False, line_terminator = '][\n', float_format = '%.2f')
# # class1bounds_71_105.to_csv('class1bounds_71_105.csv', index = False, line_terminator = '][\n', float_format = '%.2f')
# # class1bounds_106_140.to_csv('class1bounds_106_140.csv', index = False, line_terminator = '][\n', float_format = '%.2f')


# # print(np.array(pd.concat([class0lowerBound, class0upperBound],axis = 1)))

# # class1prototype = classData[1].transpose().sample(n = 20, axis = 1).mean(axis = 1)
# # class1lowerBound = class1prototype - 0.25
# # class1upperBound = class1prototype + 0.25
# # class1prototype.plot(ax = ax, legend = False, alpha = 1, color = 'red')
# # class1lowerBound.plot(ax = ax, legend = False, alpha = 1, color = 'orange')
# # class1upperBound.plot(ax = ax, legend = False, alpha = 1, color = 'orange')


# # classData[0].transpose().iloc[:,0].plot(ax = ax, legend = False, alpha = 1, color = 'red')
# # classData[0].transpose().iloc[:,1].plot(ax = ax, legend = False, alpha = 1, color = 'red')
# # classData[0].transpose().iloc[:,2].plot(ax = ax, legend = False, alpha = 1, color = 'red')
# # classData[0].transpose().iloc[:,3].plot(ax = ax, legend = False, alpha = 1, color = 'red')
# # classData[0].transpose().iloc[:,4].plot(ax = ax, legend = False, alpha = 1, color = 'red')
# # classData[0].transpose().iloc[:,5].plot(ax = ax, legend = False, alpha = 1, color = 'red')
# # classData[0].transpose().iloc[:,6].plot(ax = ax, legend = False, alpha = 1, color = 'red')
# # classData[0].transpose().iloc[:,7].plot(ax = ax, legend = False, alpha = 1, color = 'red')
# # classData[0].transpose().iloc[:,8].plot(ax = ax, legend = False, alpha = 1, color = 'red')
# # classData[0].transpose().iloc[:,9].plot(ax = ax, legend = False, alpha = 1, color = 'red')







# plot all samples in blue and with alpha = 0.1
# plot lower and upper bounds
# plot mean of bounds


class0_0_35_bounds = pd.DataFrame([[0.75,1.25],[-1.01,-0.51],[-2.71,-2.21],[-3.63,-3.13],[-4.23,-3.73],[-4.15,-3.65],[-3.60,-3.10],[-2.62,-2.12],[-1.91,-1.41],[-1.44,-0.94],[-0.91,-0.41],[-0.56,-0.06],[-0.49,0.01],[-0.46,0.04],[-0.46,0.04],[-0.48,0.02],[-0.40,0.10],[-0.36,0.14],[-0.40,0.10],[-0.43,0.07],[-0.44,0.06],[-0.43,0.07],[-0.47,0.03],[-0.51,-0.01],[-0.52,-0.02],[-0.54,-0.04],[-0.57,-0.07],[-0.58,-0.08],[-0.61,-0.11],[-0.62,-0.12],[-0.63,-0.13],[-0.68,-0.18],[-0.74,-0.24],[-0.77,-0.27],[-0.78,-0.28]])
class0_36_70_bounds = pd.DataFrame([[-0.78,-0.28],[-0.78,-0.28],[-0.84,-0.34],[-0.82,-0.32],[-0.78,-0.28],[-0.75,-0.25],[-0.67,-0.17],[-0.64,-0.14],[-0.57,-0.07],[-0.46,0.04],[-0.39,0.11],[-0.36,0.14],[-0.31,0.19],[-0.29,0.21],[-0.23,0.27],[-0.15,0.35],[-0.16,0.34],[-0.20,0.30],[-0.21,0.29],[-0.20,0.30],[-0.22,0.28],[-0.20,0.30],[-0.18,0.32],[-0.15,0.35],[-0.15,0.35],[-0.15,0.35],[-0.13,0.37],[-0.08,0.42],[-0.09,0.41],[-0.11,0.39],[-0.06,0.44],[0.01,0.51],[-0.03,0.47],[0.01,0.51],[0.09,0.59]])
class0_71_105_bounds = pd.DataFrame([[0.12,0.62],[0.13,0.63],[0.14,0.64],[0.17,0.67],[0.21,0.71],[0.25,0.75],[0.25,0.75],[0.27,0.77],[0.26,0.76],[0.27,0.77],[0.28,0.78],[0.21,0.71],[0.19,0.69],[0.20,0.70],[0.15,0.65],[0.06,0.56],[0.09,0.59],[0.14,0.64],[0.16,0.66],[0.12,0.62],[0.09,0.59],[0.07,0.57],[0.03,0.53],[0.08,0.58],[0.12,0.62],[0.19,0.69],[0.28,0.78],[0.38,0.88],[0.46,0.96],[0.58,1.08],[0.76,1.26],[0.96,1.46],[1.13,1.63],[1.24,1.74],[1.27,1.77]])
class0_106_140_bounds = pd.DataFrame([[1.27,1.77],[1.25,1.75],[1.13,1.63],[0.98,1.48],[0.80,1.30],[0.59,1.09],[0.34,0.84],[0.08,0.58],[-0.11,0.39],[-0.18,0.32],[-0.25,0.25],[-0.32,0.18],[-0.41,0.09],[-0.44,0.06],[-0.42,0.08],[-0.42,0.08],[-0.46,0.04],[-0.54,-0.04],[-0.54,-0.04],[-0.44,0.06],[-0.46,0.04],[-0.42,0.08],[-0.39,0.11],[-0.33,0.17],[-0.08,0.42],[0.34,0.84],[0.64,1.14],[0.73,1.23],[0.80,1.30],[0.77,1.27],[0.54,1.04],[0.29,0.79],[0.20,0.70],[0.11,0.61],[0.12,0.62]])
class1_0_35_bounds = pd.DataFrame([[1.75,2.25],[-0.47,0.03],[-1.29,-0.79],[-1.82,-1.32],[-2.51,-2.01],[-2.74,-2.24],[-2.82,-2.32],[-2.67,-2.17],[-2.40,-1.90],[-1.98,-1.48],[-1.55,-1.05],[-1.26,-0.76],[-1.01,-0.51],[-0.74,-0.24],[-0.49,0.01],[-0.29,0.21],[-0.13,0.37],[-0.01,0.49],[0.05,0.55],[0.07,0.57],[0.10,0.60],[0.09,0.59],[0.07,0.57],[0.09,0.59],[0.09,0.59],[0.09,0.59],[0.10,0.60],[0.10,0.60],[0.09,0.59],[0.09,0.59],[0.10,0.60],[0.09,0.59],[0.08,0.58],[0.09,0.59],[0.10,0.60]])
class1_36_70_bounds = pd.DataFrame([[0.08,0.58],[0.04,0.54],[0.01,0.51],[0.00,0.50],[-0.00,0.50],[-0.00,0.50],[-0.01,0.49],[-0.02,0.48],[-0.05,0.45],[-0.06,0.44],[-0.06,0.44],[-0.08,0.42],[-0.09,0.41],[-0.10,0.40],[-0.11,0.39],[-0.12,0.38],[-0.13,0.37],[-0.15,0.35],[-0.15,0.35],[-0.13,0.37],[-0.14,0.36],[-0.14,0.36],[-0.16,0.34],[-0.17,0.33],[-0.15,0.35],[-0.15,0.35],[-0.14,0.36],[-0.13,0.37],[-0.12,0.38],[-0.10,0.40],[-0.09,0.41],[-0.07,0.43],[-0.07,0.43],[-0.05,0.45],[-0.03,0.47]])
class1_71_105_bounds = pd.DataFrame([[-0.02,0.48],[0.01,0.51],[0.04,0.54],[0.06,0.56],[0.08,0.58],[0.11,0.61],[0.13,0.63],[0.16,0.66],[0.19,0.69],[0.22,0.72],[0.23,0.73],[0.25,0.75],[0.26,0.76],[0.27,0.77],[0.27,0.77],[0.29,0.79],[0.32,0.82],[0.32,0.82],[0.33,0.83],[0.35,0.85],[0.36,0.86],[0.37,0.87],[0.36,0.86],[0.39,0.89],[0.41,0.91],[0.42,0.92],[0.40,0.90],[0.41,0.91],[0.43,0.93],[0.45,0.95],[0.44,0.94],[0.45,0.95],[0.48,0.98],[0.48,0.98],[0.50,1.00]])
class1_106_140_bounds = pd.DataFrame([[0.50,1.00],[0.48,0.98],[0.48,0.98],[0.49,0.99],[0.51,1.01],[0.50,1.00],[0.51,1.01],[0.52,1.02],[0.49,0.99],[0.46,0.96],[0.43,0.93],[0.40,0.90],[0.34,0.84],[0.28,0.78],[0.23,0.73],[0.19,0.69],[0.13,0.63],[0.06,0.56],[-0.00,0.50],[-0.08,0.42],[-0.16,0.34],[-0.27,0.23],[-0.34,0.16],[-0.41,0.09],[-0.57,-0.07],[-0.80,-0.30],[-1.07,-0.57],[-1.50,-1.00],[-2.01,-1.51],[-2.53,-2.03],[-2.99,-2.49],[-3.30,-2.80],[-3.51,-3.01],[-2.99,-2.49],[-2.72,-2.22]])

class0Bounds = pd.concat([class0_0_35_bounds, class0_36_70_bounds, class0_71_105_bounds, class0_106_140_bounds])
class0Mean = class0Bounds.mean(axis = 1)


class1Bounds = pd.concat([class1_0_35_bounds, class1_36_70_bounds, class1_71_105_bounds, class1_106_140_bounds])
class1Mean = class1Bounds.mean(axis = 1)

print(class0Mean)
print(class0Mean.transpose().iloc[0])
# print(class0Bounds)
# class0BoundsIndex = class0Bounds.reset_index()
# class0BoundsIndex['newIndex'] = range(1,141)
# class0BoundsIndex.set_index('newIndex')
# print(class0BoundsIndex)
# print(range(1,141))
# classBoundsIndex2 = class0BoundsIndex.set_index(range(1,141))

# print(classBoundsIndex2)
# print(classData[0])

plt.plot(range(1,141), class0Bounds.transpose().iloc[0].values, color = 'red',linewidth=2.0)
plt.plot(range(1,141), class0Bounds.transpose().iloc[1].values, color = 'red',linewidth=2.0)
plt.plot(range(1,141), class0Mean, color = 'red',linewidth=2.0)


plt.plot(range(1,141), class1Bounds.transpose().iloc[0].values, color = 'yellow',linewidth=2.0)
plt.plot(range(1,141), class1Bounds.transpose().iloc[1].values, color = 'yellow',linewidth=2.0)
plt.plot(range(1,141), class1Mean, color = 'yellow',linewidth=2.0)

# plt.plot(range(1,141), class0BoundsIndex.transpose().iloc[1]['1'].values)

# class0BoundsIndex.transpose().iloc[1].plot(x = ['newIndex'],y = ['0'],ax = ax, legend = False, alpha = 1, grid = True, color = 'red')
# class0BoundsIndex.transpose().iloc[2].plot(y = ['newIndex', '1'],ax = ax, legend = False, alpha = 1, grid = True, color = 'red')

# print(class0Bounds.transpose().iloc[:,0])
# class0bounds.plot()
# print(class0bounds)

























































plt.savefig('prototypeBounds')
tikz.save('prototypeBounds.tex')

plt.show()
# # print(data.isnull().values.any())


# 		# dataClass1 = dataNoNa[dataNoNa['Class'] == 1]
# 		# dataClass1WithoutClass = dataClass1.drop(columns = ['Class'])
# 		# cleanedData = dataClass1WithoutClass.values.reshape(-1,1)
# 		# lengthAdjustedData = cleanedData[:length]
# 		# self.data = pd.DataFrame(lengthAdjustedData)
# 		# os.chdir(cwd)







# # fig, ax = plt.subplots(2, sharey = True)
# # classData[0].transpose().iloc[1:,:].plot(ax = ax[0], legend = False, color = 'blue', alpha = 0.1)
# # classData[1].transpose().iloc[1:,:].plot(ax = ax[0], legend = False, color = 'red', alpha = 0.1)

# # classData[1].transpose().iloc[1:,:].plot(ax = ax[1], legend = False, color = 'red', alpha = 0.1)
# # classData[0].transpose().iloc[1:,:].plot(ax = ax[1], legend = False, color = 'blue', alpha = 0.1)

# # for i in range(2):
# # 	classData[i].transpose().iloc[1:,:].plot(ax = ax, legend = False)
# # print(classData)
# # data.transpose().iloc[:20,:50].plot(legend = False)
# # plt.show()