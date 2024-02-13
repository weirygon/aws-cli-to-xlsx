import json

def get(file_name):
    s3_list = list()

    with open(file_name, 'rb') as file_json:
        s3_json = json.load(file_json)
    
    for bucket in s3_json['Buckets']:
        s3_value = list()

        s3_value.append(bucket['Name'])

        s3_list.append(s3_value)
    return s3_list