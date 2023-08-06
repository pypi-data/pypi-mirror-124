
from sklearn.model_selection import train_test_split

class Slicer:

    def __init__(self, dataframe):
        self.original_dataframe = dataframe
        self.train = None
        self.test  = None 

    def simple_split(self):
        pass

    def supervised_split(self, target:str=None):
        pass

    def unsupervised_split(self):
        pass
        
