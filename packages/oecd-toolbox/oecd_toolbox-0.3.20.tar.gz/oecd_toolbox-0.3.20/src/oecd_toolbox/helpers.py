# ---------------------------------------------------------------------------------------------
# convert.py library functions
# ---------------------------------------------------------------------------------------------
import logging
from pathlib import Path
import json
import os
import psutil

#----------------------replace_symbols----------------------
# DELETED functions - JUST USE slugify(x, separator = '_') 


#----------------------datetime_tuple_to_str----------------------
# TODO check if DbNomics toolbox in its model handling does not already cover this
def datetime_tuple_to_str(val:tuple):

    " Transform tuple date into Dbnomics valid string date format: (YYYY,M,D) ==> (YYYY-MM-DD) "
    
    day=str(val[2])
    month=str(val[1])
    year=str(val[0])
    if val[1]<10:
        month='0' + str(val[1])
    if val[2]<10:
        day='0' + str(val[2])
    return year + '-' + month + '-' + day

#----------------------datetime_str_to_str----------------------
# TODO: check usages
def datetime_str_to_str(val:str):
    " Transform string date with hours, minutes and seconds into Dbnomics valid string date format: (YYYY-MM-DD HH:MM:SS) ==> (YYYY-MM-DD) or (YYYY,MM,DD HH:MM:SS) ==> (YYYY-MM-DD)"
    return val.split(' ',1)[0]

#----------------------write_series_jsonl----------------------

def write_series_jsonl(series_filepath: Path, prep_df_list: list):
    """Write series list to series.jsonl file at once."""
    with series_filepath.open('wt', encoding='utf-8') as fd:
        fd.write('\n'.join(map(lambda dict_:json.dumps(dict_, ensure_ascii=False, sort_keys=True),prep_df_list)))


#----------------------memory_usage----------------------

# turn this into a logging function rather then printing
def memory_usage():
    "Measure the total memory used by Python process. Result in bytes"
    process = psutil.Process(os.getpid())
    print(str(process.memory_info().rss) + ' bytes')

#----------------------clear_entries_wo_data----------------------

def clear_entries_wo_data(D : dict):

    """Clear dictionaries from entries without data.
    Example : If we input D = {1 : 'A', 2 : '', 3 : 'E'}, the output will be {1: 'A', 3: 'E'}
    """
    return {k: v for k, v in D.items() if v}


#----------------------dataset_json_to_csv----------------------
import csv

def dataset_json_to_csv(source_dir : Path):


    """Convert dataset.json into a csv file"""
    json_file = json.load(open(source_dir,"r",encoding="utf-8"))
    dict_data=json_file['dimensions_values_labels']
    
    def create_list_dimension(dimension_name_code : str):
        # return a list dict_type like with all data from ONE dimension code/label 
        L=[]
        dim_dict=dict()
        for keys in dict_data[dimension_name_code]:
                if keys != 'nan':
                    dim_dict=dict()
                    dim_dict[dimension_name_code + '_code'] = keys
                    dim_dict[dimension_name_code + '_label'] = dict_data[dimension_name_code][keys]
                    L.append(dim_dict)
        return L

    def create_combine_csv():
    
        dim_list_df=[]
        ext='.csv'

        for i in json_file['dimensions_codes_order']:

            dim_csv_file = i + ext

            with open (dim_csv_file , 'w',encoding="utf-8" ) as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=[i + '_code' ,i +'_label'])
                writer.writeheader()
                for data in create_list_dimension(i):
                    writer.writerow(data)


            dim_list_df.append(pd.read_csv(dim_csv_file))
            os.remove(dim_csv_file)

        combined_csv=pd.concat(dim_list_df,axis=1)
        combined_csv.to_csv("dataset.csv", index=False, encoding='utf-8-sig')
    
    create_combine_csv()


#----------------------series_jsonl_to_csv----------------------

def series_jsonl_to_csv(source_dir : Path):

    """Convert series.jsonl into a csv file"""

    json_file = []
    for line in open(source_dir, 'r', encoding="utf-8"):
        json_file.append(json.loads(line))
        
    def create_list_observations():
        L=[]
        dim_dict=dict()

        for keys in json_file:

            tmp = keys['observations'][1:]

            for j in range(len(tmp)):
                date = tmp[j][0]
                obs = tmp[j][1]

                dim_dict=dict()
                dim_dict['code'] = keys['code']
                dim_dict['PERIOD'] = date
                dim_dict['VALUE'] = obs

                L.append(dim_dict)

        return L
    
    def create_csv_file():  
        csv_file = 'series.csv' 
        with open (csv_file , 'w',encoding="utf-8-sig",newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['code' ,'PERIOD','VALUE'])
            writer.writeheader()
            for data in create_list_observations():
                writer.writerow(data)
    
    create_csv_file()


log = logging.getLogger(__name__)
# ---------------------------------------------------------------------------------------------
# Recovery of environment variables
# ---------------------------------------------------------------------------------------------
def recov_env_var(env_var:str):
    """Retrieve environment variables from os """
    var=os.environ.get(env_var)
    if len(var)==0:
        log.error('environment variables {} not found'.format(env_var))
        raise ValueError('environment variables {} not found'.format(env_var))
    else:
        return var


# ---------------------------------------------------------------------------------------------
# Arguments checking and loggin setting
# ---------------------------------------------------------------------------------------------

# TODO: phase out for alternative pattern?
import argparse

def parseArguments(arguments_list):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for positional_args, keyword_args in arguments_list:
        parser.add_argument(positional_args, **keyword_args)
    args = parser.parse_args()
    return args


