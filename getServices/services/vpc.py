import json

def get(file_name):
    vpc_list = list()

    with open(file_name, 'rb') as file_json:
        vpc_json = json.load(file_json)

    for vpc in vpc_json['Vpcs']:
        vpc_value = list()
        #print(vpc, type(vpc))

        vpc_value.append(vpc['VpcId'])
        vpc_value.append(vpc['CidrBlock'])
        vpc_value.append(vpc['State'])
        if vpc['IsDefault']:
            vpc_value.append('default')
        else:
            vpc_value.append(None)
            if 'Tags' in vpc:
                for tag in vpc.get('Tags', []):
                    if tag['Key'] == 'Name':
                            vpc_value[-1] = tag['Value']
        vpc_list.append(vpc_value)

    return vpc_list