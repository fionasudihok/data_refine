from datetime import datetime, timedelta
import csv
import jsonlines
import test_files
from pathlib import Path
import os, sys
import json



class JsonLineParser():
    write_file = open("method_data.csv", 'a')
    csvwriter = csv.writer(write_file)
    csvwriter.writerow(['IMEI', 'COUNT'])
    list_of_imeis = []

    @classmethod
    def tearDownClass(cls):
        cls.write_file.close()

    @classmethod
    def directory_iterator(cls, file_path):
        """
        :param file_path: Parent Directory where all the folders are
        :return:
        """

        # Iterate through directory
        for folder in os.listdir(file_path):
            if folder != '.DS_Store':
                for subfolder in os.listdir(file_path + "/" + folder):
                    if subfolder != '.DS_Store':
                        for startdayfolder in os.listdir(file_path + "/" + folder + "/" + subfolder):
                            if startdayfolder != '.DS_Store':
                                for file in os.listdir(file_path + "/" + folder + "/" + subfolder + "/" + startdayfolder):
                                    cls.file_parser(file_path + "/" + folder + "/" + subfolder + "/" + startdayfolder + "/" + file)


        cls.print_csv(cls.list_of_imeis)


    @classmethod
    def file_parser(cls, path):
        """
        :param path: input json file
        :return:
        """
        input = path
        with jsonlines.open(input) as reader:
            # Iterate through json lines - compile list of offending IMEIs into one list
            for obj in reader:
                sensorAnomalies = obj["sensorAnomalies"]

                for i in range(len(sensorAnomalies)):
                    if len(sensorAnomalies[i]["repeatingRpmAndSpeed"]) != 0:
                        temp_imei = obj['imei']
                        # if temp_imei not in cls.list_of_imeis:
                        cls.list_of_imeis.append(temp_imei)



    @classmethod
    def print_csv(cls, imeis):
        distinct = []
        for i in imeis:
            if i not in distinct:
                distinct.append(i)
                counter = cls.list_of_imeis.count(i)
                cls.csvwriter.writerow([i, counter])



