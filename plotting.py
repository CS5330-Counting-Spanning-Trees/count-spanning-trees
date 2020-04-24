import os
import matplotlib.pyplot as plt
import numpy as np
import db

# this will plot data onto a simple x,y graph, and save it into the location specified by path
# data is a dict mapping {label : dataset}
# label is the name of that dataset
# each dataset is a bunch of points (x_i, y_i), which will appear 1 line
# so each dataset gives one line, all plotted on the same axes
# WARNING: will overwrite files!!!

# currently I don't know how to plot data and return some object, which can be viewed or saved later.
# i only know how to immediately save LOL
def plot_data_and_save(data, path):
    fig = plt.figure()
    for label, dataset in data.items():
        xs, ys = map(list, zip(*dataset))
        plt.plot(xs, ys, label=label)
        plt.legend()
    plt.savefig(path)

def test():
    save_dir = 'pics'
    filename = 'plotting_test.png'
    path = (os.path.join(save_dir, filename))
    ds1 = [(i, i) for i in range(20)]
    ds2 = [(i, 2*i) for i in range(30)]
    data = [ds1, ds2]
    plot_data_and_save(data, path)

def plot_termwise_data():
    path = 'termwise-num-samples-for-0.01-error.json'
    save_path = 'pics/termwise-num-samples-for-0.01-error.png'
    data = db.load_data(path)
    ns = list(range(40, 190, 10))
    plt.plot(ns, data)
    xla
    plt.savefig(save_path)

if __name__ == "__main__":
    pass
    #plot_termwise_data()