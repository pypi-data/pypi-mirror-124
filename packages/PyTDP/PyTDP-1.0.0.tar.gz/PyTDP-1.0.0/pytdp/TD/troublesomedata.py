from pytdp.analyzer.api import DataScience
from pytdp.preprocessor.api import Missing
from pytdp.reader.api import Tdp_reader
import os

class TroublesomeData(DataScience, Missing, Tdp_reader):
    def __init__(self, data_list_or_directory = os.getcwd(), working_directory = os.getcwd()):
        self.preprocess_data = {}
        super(TroublesomeData, self).__init__(data_list_or_directory, working_directory)

    def set_preprocess_key(self, *args):
        self.preprocessing_data = {}
        for key in args:
            if key in self.key:
                self.preprocessing_data[key] = self.data[key]
            else :
                print(f'{key} が見つかりません。 \nself.key で確認してください。')
    
    def set_analyze_key(self, *args):
        self.analyzing_data = {}
        for key in args:
            if key in self.key:
                if len(self.preprocessing_data.keys()) == 0:
                    self.analyzing_data[key] = self.data[key]
                else :
                    self.analyzing_data[key] = self.preprocessing_data[key]
            else :
                print(f'{key} が見つかりません。 \nself.key で確認してください。')