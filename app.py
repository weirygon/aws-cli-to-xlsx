import openpyxl
import json
import os
import re

ec2_list = list()
rds_list = list()
s3_list = list()

def main():
    account_list = getAccounts()
    pwd_root = os.getcwd()
    global ec2_list

    account_dict = dict()

    for id_account in account_list:
        ec2_list = list()
        rds_list = list()
        s3_list = list()

        print(f'Account: {id_account}')

        try:
            os.chdir(id_account)
        except FileNotFoundError:
            print(f'[-] Directory Not Found: {id_account}')
            continue


        services_account = getServices()
        account_dict[id_account] = services_account

        os.chdir(pwd_root)
    
    saveInXlxs(account_dict)
    with open('log.json', 'w') as file_json:
        json.dump(account_dict, file_json, indent=2)

def saveInXlxs(account_dict):
    

    file_xlsx = openpyxl.Workbook()

    file_xlsx.create_sheet('EC2')
    sheet = file_xlsx['EC2']
    sheet.append(['idInstance', 'name', 'state', 'type', 'ipPrivate', 'ipPublic', 'local','idAcconut'])
    file_xlsx.create_sheet('RDS')
    file_xlsx.create_sheet('S3')

    for account_id in account_dict:
        sheet = None

        if account_dict[account_id]['ec2']:
            sheet = file_xlsx['EC2']
           
            for ec2 in account_dict[account_id]['ec2']:
                ec2.append(account_id)
                sheet.append(ec2)

    file_xlsx.save('AWS.xlsx')
    file_xlsx.close()

def getAccounts():
    pwd=os.getcwd()
    pattern_regex = re.compile(r'^\d{12}$')

    ls = os.listdir(pwd)

    account_list = [name for name in ls if os.path.isdir(os.path.join(pwd, name)) and pattern_regex.match(name)]

    return account_list

def getServices():
    account_id_pwd = os.getcwd()
    
    service_list = os.listdir(os.getcwd())
    service_dict = dict()

    for service_name in service_list:
        os.chdir(service_name)
        service_dict[service_name] = list()

        for service_file_name in os.listdir():
            if 'ec2' in service_file_name:
                getEC2FromFile(service_file_name)
            
            '''
            elif 'rds' in service_file_name:
                print('RDS=>', service_file_name)
            elif 's3' in service_file_name:
                 print('S3=>', service_file_name)
            '''
        os.chdir(account_id_pwd)  

    if ec2_list:
        service_dict['ec2'] = ec2_list
    if rds_list:
        service_dict['rds'] = rds_list
    if s3_list:
        service_dict['s3'] = s3_list
    
    return service_dict

def getRegionOfFileName(file_name):
    file_name = file_name.split('-', 1)
    file_name = file_name[1].split('.')
    
    return file_name[0]

def getEC2FromFile(file_name):
    ec2_json = None
    ec2_region = getRegionOfFileName(file_name)
    global ec2_list

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

            ec2_values.append(ec2_region)

            ec2_list.append(ec2_values)

main()