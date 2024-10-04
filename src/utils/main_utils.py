#this will generate a class that will read the file,understand the schema,
# write the object and it will also club categorical,discrete,continues column in a list 

import sys
from typing import Dict, Tuple
import os

import numpy as np
import pandas as pd
import pickle
import yaml
import boto3

from src.constant import *
from src.exception import CustomException
from src.logger import logging

class MainUtils:
    def __init__(self)->None:
        pass

    def read_yaml_file(self,filename:str)->dict:
        try:
            with open(filename,"rb") as yaml_file:
                return yaml.safe_load(yaml_file)    #return the binary file in a dictionary file for better understanding
            
        except Exception as e:
            raise CustomException(e,sys) from e     #the exception is raised again, wrapped in a CustomException, with e as the original exception and sys as an additional context.

    def read_schema_config_file(self)->dict:
        try:
            schema_config = self.read_yaml_file(os.path.join("config","model.yaml"))    #provides the path to model.yaml and reads it by using read_yaml_file function
            return schema_config
        
        except Exception as e:
            raise CustomException(e,sys) from e
        
        
    @staticmethod       #we are using static files so that we can easily access it from anywhere without creating an instance of the class
    def save_object(file_path:str,obj:object)->None:
        logging.info("Entered the save_object method of MainUtils class")

        try:
            with open(file_path,"wb") as file_obj:        
                pickle.dump(obj,file_obj)               #converting the object(ex--dict,list,..) to byte stream and storing in file_obj which is opened in write mode(binary) 
            
            logging.info("Exited the save_object method of MainUtils class")
        except Exception as e:
            raise CustomException(e,sys) from e
        
    @staticmethod
    def load_object(file_path:str)->object:
        logging.info("Entered the load_object method of MainUtils class")

        try:
            with open(file_path,"rb") as file_obj:      #just reading and sending the file by deserializing it for use of it
                obj = pickle.load(file_obj)

            logging.info("Entered the load_object method of MainUtils class")
            return obj
        
        except Exception as e:
            raise CustomException(e,sys) from e
        
    @staticmethod
    def upload_file(from_filename,to_filename,bucket_name):
        try:
            s3_resource = boto3.resource("s3")      #boto3.resource("s3") creates a low-level, service-level resource object for Amazon S3 using boto3.

            s3_resource.meta.client.upload_file(from_filename,bucket_name,to_filename)  #it helps to upload the file from "from_filename" to "to_filename" by having bucket name in Amazon "bucket_name"

        except Exception as e:
            raise CustomException(e,sys) from e
        
    @staticmethod
    def download_model(bucket_name, bucket_file_name, dest_file_name):
        try:
            s3_client = boto3.client("s3")

            s3_client.downloaded_file(bucket_name, bucket_file_name, dest_file_name)    #helps to download the file in our local system

            return dest_file_name   
        
        except Exception as e:
            raise CustomException(e,sys) from e

    @staticmethod
    def remove_unwanted_spaces(data:pd.DataFrame)->pd.DataFrame:
        try:
            df_without_spaces = data.apply(
                lambda x:x.str.strip() if x.dtype == 'object' else x)

            logging.info('Unwanted spaces removal Successful.Exited the remove_unwanted_spaces method of the Preprocessor class')

            return df_without_spaces

        except Exception as e:
            raise CustomException(e,sys) from e
        
    @staticmethod
    def identify_feature_types(dataframe:pd.DataFrame):
        data_types=dataframe.dtypes

        categorical_features=[]
        continuous_features=[]
        discrete_features=[]

        for column,dtype in dict(data_types).items():
            unique_values = dataframe[column].nunique()

            if(dtype=='object' or unique_values<10):
                categorical_features.append(column)
            
            elif dtype in [np.int64 or np.float64]:
                if(unique_values>20):
                    continuous_features.append(column)
                else:
                    discrete_features.append(column)
            
            else:
                pass
        
        return categorical_features,continuous_features,discrete_features


        
