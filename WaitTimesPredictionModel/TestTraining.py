from RegressionModel.WaitTimeRegressionModel import WaitTimeRegressionModel
import logging



def main():
    #logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    model = WaitTimeRegressionModel()
    model.TrainModel("Disneyland")
    datapoint = {}
    result = model.Predict(datapoint)
    print(str(result) + "wasa predicted from: " + str(datapoint))



if __name__ == '__main__':
    main()
