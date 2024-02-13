import json

def get(file_name):
    elb_list = list()

    with open(file_name, 'rb') as file_json:
        elb_json = json.load(file_json)

    for elb in elb_json['LoadBalancers']:
        elb_value = list()
        
        elb_value.append(elb['LoadBalancerName'])
        elb_value.append(elb['Type'])
        elb_value.append(elb['VpcId'])
        elb_value.append(elb['State']['Code'])
        
        elb_list.append(elb_value)
    return elb_list 