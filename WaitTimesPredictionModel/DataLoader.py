from ParkTimeDataPoint import *
import os
import json

class DataLoader():

    def __init__(self, path):
        self.basePath = path

    def loadDataFrames(self, dataFileName, graphFileName):
        dataPointsRaw, graphRaw = self.parseInputFiles(dataFileName, graphFileName)
        dataPoints = self.preprocessData(dataPointsRaw)
        graph = self.preprocessGraph(graphRaw)

        return dataPoints, graph


    def parseInputFiles(self, dataFileName, graphFileName):
        dataFilePath =  os.path.join(self.basePath, dataFileName)
        graphFilePath =  os.path.join(self.basePath, graphFileName)

        dataPointsRaw = []
        with open(dataFilePath) as df:
            for line in df:
                dataPointsRaw.append(json.loads(line))

        with open(graphFilePath, 'r') as gf:
            graphRaw = json.loads(gf.read())

        return dataPointsRaw, graphRaw

    def preprocessData(self, dataPointsRaw):
        dataPoints = []
        #TODO

        return dataPoints

    def preprocessGraph(self, graphRaw):
        graph = None
        #TODO

        return graph