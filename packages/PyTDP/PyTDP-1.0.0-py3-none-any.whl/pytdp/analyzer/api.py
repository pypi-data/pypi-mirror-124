from pytdp.preprocessor.api import(
    Missing
)



class DataScience(Missing):
    def __init__(self, data_list_or_directory, working_directory):
        self.analyzing_data = {}
        super().__init__(data_list_or_directory, working_directory)

    
    def check_analyzing_data(self):
        if len(self.analyzing_data.keys()) == 0:
            if len(self.latest_preprocessed_data.keys()) == 0:
                return self.data
            return self.latest_preprocessed_data