from pytdp.analyzer.api import DataScience
from pytdp.preprocessor.api import Missing
from pytdp.reader.api import Tdp_reader
from pytdp.bases.api import Base
import os

class TroublesomeData(DataScience, Missing, Tdp_reader, Base):
    def __init__(self,
                 data_list_or_directory = os.getcwd(), 
                 working_directory = os.getcwd(), 
                 detail = {
                     'auto' : False,
                     
                     'model' : None,

                 }):
        super(TroublesomeData, self).__init__(data_list_or_directory, working_directory)

        if detail['auto'] :
            self.set_preprocess_key()
            self.delete_null()
            self.set_analyze_key()
            self.train_test_split()
            self.machine_learning(detail['model'])