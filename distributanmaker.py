from matplotlib import pyplot
from numpy import asarray
from numpy import exp
from numpy import loadtxt
import numpy as np
import os
from sklearn.neighbors import KernelDensity


class DistributionMaker:

    def __init__(self):
        self.model = KernelDensity(bandwidth=2, kernel='gaussian')
        self.data = False

    def _add_from_file(self, address,column_number):
        data = loadtxt(address)
        if self.data is False:
            self.data = data[:, column_number].reshape((len(data), 1))
        else:
            self.data = np.append(self.data, data[:, -1].reshape((len(data), 1)), axis=0)

    def get_address(self, address, directory=False,column_number=-1):
        if directory is not False:
            for subdir, dirs, files in os.walk(address):
                for filename in files:
                    filepath = subdir + os.sep + filename
                    if filepath.endswith(".txt"):
                        #print(999,filepath)
                        self._add_from_file(filepath,column_number)
        else:
            self._add_from_file(address,column_number)

        self.model.fit(self.data)

    def show_chart(self, bins=150):
        values = asarray([value for value in range(1, 60)])
        values = values.reshape((len(values), 1))
        probabilities = self.model.score_samples(values)
        probabilities = exp(probabilities)
        new_samples = self.model.sample(1000, random_state=None)
        pyplot.hist(self.data, bins=bins, density=True,label='real samples')
        pyplot.title(label='chart')
        pyplot.xlabel(xlabel='data value')
        pyplot.ylabel(ylabel='histogram (number of sample)')
        pyplot.hist(new_samples, bins=100, density=True,label='simulated data')
        pyplot.plot(values[:], probabilities,)
        pyplot.legend()
        pyplot.show()

    def generate_sample(self, samples=1):
        return self.model.sample(samples, random_state=None)


if __name__ == '__main__':
    d = DistributionMaker()
    #d.get_address(directory=True,address='./stadia_cloud_gaming_dataset_2020/stadia_cloud_gaming_dataset_2020/Dataset_D1')
    d.get_address('ds.txt')
    d.show_chart(bins=150)
    print(d.generate_sample(samples=100))

