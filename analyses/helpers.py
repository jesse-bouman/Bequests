import inspect
import os
from typing import List, Any
import pandas as pd

class OutputData:
    def __init__(self, data_name):
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        basename = os.path.basename(module.__file__) + '_' + data_name + '.dat'
        self.target_path = os.path.join(os.path.dirname(__file__), 'data', basename)
        self.data = dict()

    def add_data(self, data: List[List[Any]], data_describer: str):
        for i, data_series in enumerate(data):
            self.data[f'{data_describer}_{i}'] = data_series

    def write_data(self):
        df = pd.DataFrame(data=self.data)
        df.to_csv(self.target_path)
