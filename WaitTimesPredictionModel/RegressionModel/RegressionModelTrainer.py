from PostgresDataModel import PsDataModel

class RegressionModelTrainer():

    def TrainModel(self, parkName):#TODO
        dataModel = PsDataModel()
        rawdata = dataModel.GetAllDataForPark(parkName)
        data = self.PreProcessData(rawdata)



        model = None
        return model

    def PreProcessData(self, data):#TODO
        

        return data

    