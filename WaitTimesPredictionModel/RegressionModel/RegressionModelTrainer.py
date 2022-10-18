from PostgresDataModel import PsDataModel

class RegressionModelTrainer():

    def TrainModel(self, parkName):#TODO
        dataModel = PsDataModel()
        data = dataModel.GetAllDataForPark(parkName)

        model = None
        return model

    def PreProcessData(self, data):#TODO
        return data