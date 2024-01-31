import openpyxl
import json
import os
import re
'''
file_xlsx = openpyxl.Workbook()

file_xlsx.create_sheet('EC2')

sheet_ec2 = file_xlsx['EC2']

sheet_ec2.append(['ID Instance', 'Name', 'State', 'ID Acconut', 'Local'])

file_xlsx.save('AWS.xlsx')
'''
def main():
    account_list = getAccounts()
    print(account_list, type(account_list[0]))

    #with open('ec2.json', 'r') as file_json:
    #    ec2_json = json.load(file_json)
    #getEC2FromJson(ec2_json)

def getAccounts():
    pwd = '.'
    pattern_regex = re.compile(r'^\d{12}$')

    ls = os.listdir(pwd)

    account_list = [name for name in ls if os.path.isdir(os.path.join(pwd, name)) and pattern_regex.match(name)]

    return account_list

def getEC2FromJson(ec2_json):

    ec2_list = list()

    for reservation in ec2_json["Reservations"]:
        

        for instance in reservation["Instances"]:
            ec2_values = list()

            print(f"Instance ID: {instance['InstanceId']}")
            print(f"State: {instance['State']['Name']}")
            print(f"Type: {instance['InstanceType']}")
            print(f"Zone: {instance['Placement']['AvailabilityZone']}")
            for tag in instance.get('Tags', []):
                    if tag['Key'] == 'Name':
                            print(f"Name: {tag['Value']}")
    
            print(f"Private IP: {instance['PrivateIpAddress']}")
            try:
                print(f"Public IP: {instance['PublicIpAddress']}")
            except:
                 print('Public IP: ')

        print(f"Owner: {reservation['OwnerId']}")
        print('\n')

main()