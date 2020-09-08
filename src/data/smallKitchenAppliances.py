from .dataset import dataset
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class smallKitchenAppliances(dataset):
    """docstring for smallKitchenAppliances"""

    def __init__(self, name, seed, purposeFlg, length):
        super(
            smallKitchenAppliances,
            self).__init__(
            name,
            seed,
            purposeFlg,
            tsFlg=True)
        cwd = os.getcwd()
        os.chdir('./src/data/ExternalDatasets/SmallKitchenAppliances')
        if purposeFlg == 'train':
            for file in os.listdir():
                if 'TRAIN' in file:
                    filename = file
        if purposeFlg == 'test':
            for file in os.listdir():
                if 'TEST' in file:
                    filename = file
        data = pd.read_csv('./' + filename, header=None)
        dataNoNa = data.dropna()
        dataNoNa.columns = dataNoNa.columns.astype(str)
        columns = dataNoNa.columns.values
        columns[0] = 'Class'
        dataNoNa.columns = columns
        dataClass1 = dataNoNa[dataNoNa['Class'] == 1]
        dataClass1WithoutClass = dataClass1.drop(columns=['Class'])
        cleanedData = dataClass1WithoutClass.values.reshape(-1, 1)
        lengthAdjustedData = cleanedData[:length]
        self.data = pd.DataFrame(lengthAdjustedData)
        os.chdir(cwd)
