import json

def get(file_name):
    ec2_list = list()
    
    with open(file_name, 'rb') as file_json:
        ec2_json = json.load(file_json)

    for reservation in ec2_json["Reservations"]:
        for instance in reservation["Instances"]:
            ec2_values = list()
            
            ec2_values.append(instance['InstanceId'])
            for tag in instance.get('Tags', []):
                    if tag['Key'] == 'Name':
                            ec2_values.append(tag['Value'])
            
            ec2_values.append(instance['State']['Name'])
            ec2_values.append(instance['InstanceType'])
            ec2_values.append(instance['PrivateIpAddress'])
            try:
                ec2_values.append(instance['PublicIpAddress'])
            except:
                ec2_values.append(None)
            ec2_list.append(ec2_values)
    return ec2_list