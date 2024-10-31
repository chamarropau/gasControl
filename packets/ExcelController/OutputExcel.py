from termcolor import colored
from termcolor import colored

import pandas as pd

class OutputExcel:

    def __init__(self, filename, data):
        self.filename = filename
        self.data = data
        
    def save_excel(self):
        df = pd.DataFrame(self.data)
        df = df.apply(pd.Series.explode)
        df = df.loc[:, ~df.columns.duplicated()]

        df.to_excel(self.filename, index=False)
