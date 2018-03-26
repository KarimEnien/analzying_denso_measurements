import pylab as plt
import numpy as np
import cPickle as pickle
from dataset_preparation import Dataset



def get_classifier_data():
    """
    Getting the dictionary dataset from the pickeled file
    return: dictonary contains the Denso states occurances and its corresponding force measurements
    rtype: dict
    """
    result = pickle.load(open( "../results/result.dat", "r" ))
    return result

def evaluation(dataset):
    """"
    This function evaluates if the process has any faults by comparing the BMD(best match distance) between a shapelet and a time series...
    If this distance is less than a specific threshold, this means that the shapelet belongs to this specific time series and the process
    is successful, and vice versa.
    param: dataset: Feeding the evaluation function with a Dataset object
    type: Dataset object
    return: true for a successful process and false for unseccessful process

    evaluation_states = ['59d638667bfe0b5f22bd6420: Motek - Erebus Unmount', '59d638667bfe0b5f22bd6443: Motek - White Part Mount Tilted',
             '59d638667bfe0b5f22bd6446: Pitasc-Sub - White Part Mount Tilted',
             '59d638667bfe0b5f22bd6449: Pitasc - Insert Upright']
    """
    ts_data = []
    dict_training_data = dataset.get_training_data()
    data_of_interest = dict_training_data['59d638667bfe0b5f22bd6449: Pitasc - Insert Upright'][0] # Change the random time-series as desired
    for state_data in data_of_interest:
        ts_data.append(state_data.values())
    data_nd = np.array(ts_data)
    data_nd = data_nd[:, 0:3]
    temp = np.copy(data_nd[:, 0:1])
    data_nd[:, 0:1] = data_nd[:, 1:2]
    data_nd[:, 1:2] = temp

    dict_classifiers = {}
    result = get_classifier_data()
    for label, (classifier, _) in result.items():
        dict_classifiers[label] = classifier
    cls = dict_classifiers['59d638667bfe0b5f22bd6449: Pitasc - Insert Upright'] # Change the classifier as desired
    mins, ds = cls.predict_all(data_nd)
    # plt.plot(ds)
    # plt.ylabel('BMD')
    # plt.show()

    classifier_threshold = cls.delta # the classifier threshold which is a characteristic value for each different state
    flag = False
    for distance in ds:
        if distance < classifier_threshold:
            flag = True
            break
    if flag:
        print"Successful process!"
    else:
        print "Unsuccessful process"
    print("Finishing...")
    return flag


def main():
    dataset = Dataset()
    status = evaluation(dataset)


if __name__ =='__main__':
    main()
