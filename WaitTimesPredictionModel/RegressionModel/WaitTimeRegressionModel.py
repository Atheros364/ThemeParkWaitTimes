



from RegressionModel.RegressionModelTrainer import RegressionModelTrainer


class WaitTimeRegressionModel():

    def LoadModelFromFile(self, modelPath):#TODO
        self.model = None

    def SaveModelToFile(self, modelPath):#TODO
        self.model = None

    def TrainModel(self, parkName):#TODO
        trainer = RegressionModelTrainer()
        self.model = trainer.TrainModel(parkName)

    def Predict(self, dataPoint):#TODO

        return 0
        


    