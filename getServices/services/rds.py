import json

def get(file_name):
    rds_list = list()

    with open(file_name, 'rb') as file_json:
        rds_json = json.load(file_json)
    
    for db_instance in rds_json['DBInstances']:
        rds_value = list()

        rds_value.append(db_instance['DBInstanceIdentifier'])
        rds_value.append(db_instance['Engine'])
        rds_value.append(db_instance['DBInstanceStatus'])
        rds_value.append(db_instance['DBInstanceClass'])

        rds_list.append(rds_value)
    
    return rds_list