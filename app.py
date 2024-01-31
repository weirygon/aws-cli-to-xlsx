import openpyxl
import json
'''
file_xlsx = openpyxl.Workbook()

file_xlsx.create_sheet('EC2')

sheet_ec2 = file_xlsx['EC2']

sheet_ec2.append(['ID Instance', 'Name', 'State', 'ID Acconut', 'Local'])

file_xlsx.save('AWS.xlsx')
'''

def getEC2FromJson(ec2_json):

    ec2_list = list()

    for reservation in ec2_json["Reservations"]:
        

        for instance in reservation["Instances"]:
            ec2_values = list()

            print(f"InstanceId: {instance['InstanceId']}")
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

with open('ec2.json', 'r') as file_json:
    ec2_json = json.load(file_json)

getEC2FromJson(ec2_json)




#for chave, valor in ec2_json.items():
#    print(f"{chave}: {valor}")