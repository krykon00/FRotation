import os
import pathlib
import pandas as pd
import numpy as np
import h5py
from abc import ABC, abstractmethod


class H5DataError(Exception):
    '''Error to rise when H5 file is without valid data.
    
        It will check for message aka file name that is invalid.
    '''
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
            
    def __str__(self):
        if self.message:
            return f"H5 error. File {self.message} cotains no valid data."
        else:
            return "H5 file contains no valid data."


class DataExtractor(ABC):

    file_path: str

    @abstractmethod
    def extract_data(self):
        pass


MAIN_CATALOG_PATH = os.path.join(pathlib.Path().resolve(), "data")


def get_file_list(files_path: str, extension: str):
    '''
    Generator for listing all files from data catalog with provided extension.
    '''

    for file in os.listdir(files_path):
        if file.endswith(extension):
            yield file


class FromCSVEctractor(DataExtractor):
    '''
    This class is responsible for creating data frame out from collected
    labolatory experiment in CSV file format.
    '''
    df_info: list = {}

    def __init__(self, file_path) -> None:
        '''
        Initialising class and creating pandas dataframe with valuable data
         and its discriptive dictionary.
        '''
        self.file_path = file_path

    def extract_data(self):
        df = pd.read_csv(filepath_or_buffer=self.file_path,
                         sep=",", header=0, usecols=["x-axis", "3", "4"])
        df.columns = ['time[s]', 'trace_1[V]', 'trace_2[V]']
        df = df.iloc[1:, :]
        df.dropna(how='any', inplace=True)
        for column in df.columns:
            df[column] = df[column].astype(float)
        t_adjust = abs(df['time[s]'].iloc[0])
        df['time[s]'] = df['time[s]'] + t_adjust
        return df


class FromH5Extractor(DataExtractor):
    '''
    This class is responsible for creating data frame out from collected
    labolatory experiment in H5 file format.
    '''
    df_info: list = {}

    def __init__(self, file_path) -> None:
        '''
        Initialising class and creating pandas dataframe with valuable data
        and its discriptive dictionary.
        '''
        self.file_path = file_path

    def extract_data(self):
        h5_file = h5py.File(self.file_path, 'r')
        df = pd.merge(
            pd.DataFrame(np.array(h5_file.get('/data/traces/AP1'))),
            pd.DataFrame(np.array(h5_file.get('/data/traces/AP2'))),
            how='left',
            on='t'
        )
        df.columns = ['time[s]', 'trace_1[V]', 'trace_2[V]']
        for column in df.columns:
            df[column] = df[column].astype(float)
        t_adjust = abs(df['time[s]'].iloc[0])
        df['time[s]'] = df['time[s]'] + t_adjust
        return df


print("**********************************************")
print('*******==> Testing code execution  <==********')
print(' ')

path_to_data: str = os.path.join(MAIN_CATALOG_PATH, "csv")
first_file = ""
for file in get_file_list(path_to_data, "csv"):
    first_file = file
    break

print("----> CSV FIle <-------")
csv_path = os.path.join(path_to_data, first_file)
mydf = FromCSVEctractor(csv_path)
print(mydf.extract_data())

path_to_data: str = os.path.join(MAIN_CATALOG_PATH, "h5")
first_file = ""
for file in get_file_list(path_to_data, "h5"):
    first_file = file
    break

print("----> H5 FIle <-------")
h5_path = os.path.join(path_to_data, first_file)
mydf = FromH5Extractor(h5_path)
try:
    print(mydf.extract_data())
except ValueError:
    print(H5DataError(first_file))
    pass
