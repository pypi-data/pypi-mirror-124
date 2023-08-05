import numpy as np
from numpy.core.numeric import tensordot
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor as MLP
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import plot_confusion_matrix

class MLPRegressor:
    def __init__(self,dataset,input_data,label,test_size=0.2,random_state=42):
        self.label = label
        dataset = pd.read_csv(dataset)
        input_data = dataset[input_data]
        input_data = (input_data - input_data.mean()) / (input_data.max() - input_data.min()) # stap 3
        label = dataset[self.label]

        self.input_data_train, self.input_data_test, self.labels_train, self.labels_test = train_test_split(input_data,label,test_size=test_size,random_state=random_state)

    def accuracy(self):
        lengte = len(self.true_labels)
        all_errors = 0
        for pred_label,true_label in zip(self.pred_labels,self.true_labels):
            if pred_label < 0.5:
                pred_label = 0
            else:
                pred_label = 1
            if pred_label == true_label:
                all_errors += 1
            

        MAE = all_errors / lengte
        return MAE

    def plot(self,length,yrange=None,ax=None):
        if ax == None:
            fig, ax = plt.subplots()
        index = np.arange(length)
        bar_width = 0.25
        opacity = 0.8

        rects1 = ax.bar(index, self.true_labels[:length], bar_width, alpha=opacity,color='r',label='True_labels')
        rects2 = ax.bar(index + bar_width, self.pred_labels[:length], bar_width,alpha=opacity,color='b',label='Pred_labels')
        rects2 = ax.bar(index + 2*bar_width, abs(self.true_labels[:length]-self.pred_labels[:length]), bar_width,alpha=opacity,color='g',label='Absolute Error')
        ax.ticklabel_format(style='plain')
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_title(self.label)
        if yrange != None:
            ax.set_ylim(yrange)
        ax.legend()

        if ax == None:
            plt.show()

    def train(self,hidden_layer_sizes):
        self.model = MLP(hidden_layer_sizes)
        self.model.fit(self.input_data_train,self.labels_train)
        
        self.pred_labels = self.model.predict(self.input_data_test)
        self.true_labels = self.labels_test