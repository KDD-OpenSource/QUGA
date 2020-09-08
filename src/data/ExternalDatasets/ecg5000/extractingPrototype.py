import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data_train = pd.read_csv('ECG5000_TRAIN', sep=',', header=None)
data_test = pd.read_csv('ECG5000_TEST', sep=',', header=None)

data = pd.concat([data_train, data_test])


classData = [data[data[0] == i] for i in range(1, 6)]

class0Samples = classData[0].transpose().sample(n=20, axis=1)
fig, ax = plt.subplots(1, sharey=True, figsize=(20, 10))
# for i in range(5):
# 	classData[i].transpose().plot(ax = ax, legend = False, alpha = 0.1, grid = True, color = 'blue')
class0Samples.plot(ax=ax, legend=False, alpha=0.1, grid=True, color='blue')
# classData[0].transpose().iloc[:,:20].plot(ax = ax, legend = False, alpha = 0.1, grid = True, color = 'blue')
# classData[1].transpose().iloc[:,:20].plot(ax = ax, legend = False, alpha = 0.1, grid = True, color = 'red')
print(classData)
start, end = ax.get_ylim()
ax.yaxis.set_ticks(np.arange(-6, 5, 1))
data.drop(columns=[0], inplace=True)
class0prototype = class0Samples.mean(axis=1)
class0lowerBound = class0Samples.min(axis=1)
class0upperBound = class0Samples.max(axis=1)


class1Samples = classData[1].transpose().sample(n=20, axis=1)
# for i in range(5):
# 	classData[i].transpose().plot(ax = ax, legend = False, alpha = 0.1, grid = True, color = 'blue')
class1Samples.plot(ax=ax, legend=False, alpha=0.1, grid=True, color='blue')
# classData[0].transpose().iloc[:,:20].plot(ax = ax, legend = False, alpha = 0.1, grid = True, color = 'blue')
# classData[1].transpose().iloc[:,:20].plot(ax = ax, legend = False, alpha = 0.1, grid = True, color = 'red')
print(classData)
start, end = ax.get_ylim()
ax.yaxis.set_ticks(np.arange(-6, 5, 1))
class1prototype = class1Samples.mean(axis=1)
class1lowerBound = class1Samples.min(axis=1)
class1upperBound = class1Samples.max(axis=1)

# class0prototype.plot(ax = ax, legend = False, alpha = 1, color = 'red')
class0lowerBound.plot(ax=ax, legend=False, alpha=1, color='red')
class0upperBound.plot(ax=ax, legend=False, alpha=1, color='red')

# class1prototype.plot(ax = ax, legend = False, alpha = 1, color = 'red')
class1lowerBound.plot(ax=ax, legend=False, alpha=1, color='green')
class1upperBound.plot(ax=ax, legend=False, alpha=1, color='green')

plt.show()
