import pandas as pd
from sklearn.model_selection import ParameterGrid,GridSearchCV
from sklearn.base import clone
from sklearn.cluster import MeanShift
from sklearn import metrics
import numpy as np
import joblib
import datetime
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve

class MS:
    def MSGridsearch(self,dmodel, data, labels, param_dict):
        """
          dmodel: default model
          data：training data
          labels: real classification
          param_dict: hyperparameter combination dictionary
        """
        output_models = []

        # Create parameter grid
     # Create hyperparameter grid
        param_grid = ParameterGrid(param_dict)

        # Change the parameter attributes in dbscan according to the param_grid
        # Modify the corresponding parameters of DBSCAN object according to the grid super parameters, train the model, and get the output data
        for param in param_grid:
            for key, value in param.items():
                setattr(dmodel, key, value)

            dmodel.fit(data)
            model = clone(dmodel)
            output_models.append(model)
    #If you have other data to output, just add it
        return (output_models)

#Evaluation criteria, for testing, not the final modular function block
    
    def get_marks(self,estimator, data, labels, name=None):
        """
           To get the score, there are five kinds of actual classification information that are required to know the data set, and there are three kinds that are not required,
       refer to the readme.txt
       
    :param estimator: model
    :param name: initial method
    :param data: feature data set
        """
        estimator.fit(data.astype(np.float64))
        print(30 * '*', name, 30 * '*')
        print("Model and parameters: ", estimator)
        print("Homogeneity Score         : ", metrics.homogeneity_score(labels, estimator.labels_))
        print("Completeness Score        : ", metrics.completeness_score(labels, estimator.labels_))
        print("V-Measure Score           : ", metrics.v_measure_score(labels, estimator.labels_))
        print("Adjusted Rand Score       : ", metrics.adjusted_rand_score(labels, estimator.labels_))
        print("Adjusted Mutual Info Score: ", metrics.adjusted_mutual_info_score(labels, estimator.labels_))
        print("Calinski Harabasz Score   :   ", metrics.calinski_harabasz_score(data, estimator.labels_))
        print("Silhouette Score          : ", metrics.silhouette_score(data, estimator.labels_))

    def read_para(self):
        para = pd.read_excel('para.xlsx', header=None, dtype='object')
        dic = para.set_index(0).T.to_dict('list')
        for i in dic:
            dic[i] = [x for x in dic[i] if x == x]
        return dic

    def plot_learning_curve(self,model, data, labels):
        train_sizes, train_scores, test_scores = learning_curve(model, data, labels,
                                                                scoring='adjusted_rand_score', cv=5)
        train_scores_mean = np.mean(train_scores, axis=1) # To average the training score set by row 
        train_scores_std = np.std(train_scores, axis=1) #  Calculate the standard deviation of training matrix
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)
        plt.grid()  # Set the background to gridlines


        plt.fill_between(train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std,
                         alpha=0.1,
                         color='r')
    # plt.fill_between(function fills the space of the upper and lower variances of the average model accuracy with colors.
        plt.fill_between(train_sizes, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, alpha=0.1,
                         color='g')
        plt.plot(train_sizes, train_scores_mean, 'o-', color='r', label='Training score')
    # Then use plt.plot The () function draws the average of the model accuracy.
        plt.plot(train_sizes, test_scores_mean, 'o-', color='g', label='Cross_validation score')
        plt.legend(loc='best')  # Show legend
        plt.show()
