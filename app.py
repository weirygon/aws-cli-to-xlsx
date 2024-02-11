import openpyxl
import json
import os
import re
from getServices import getService as getService

def main():
    pwd_root = os.getcwd()
    account_dict = dict()

    for id_account in getIdAccounts():
        print(f'Account: {id_account}')

        try:
            os.chdir(id_account)
        except FileNotFoundError:
            print(f'[-] Directory Not Found: {id_account}')
            continue

        account_dict[id_account] = getService.ec2()
        print(json.dumps(account_dict[id_account], indent=2))

        os.chdir(pwd_root)
    #saveInXlxs(account_dict)
    with open('log.json', 'w') as file_json:
        json.dump(account_dict, file_json, indent=2)
'''
def saveInXlxs(account_dict):
    file_xlsx = openpyxl.Workbook()

    #HEADER EC2
    file_xlsx.create_sheet('EC2')
    sheet = file_xlsx['EC2']
    sheet.append(['idInstance', 'name', 'state', 'type', 'ipPrivate', 'ipPublic', 'local','idAcconut'])
    #HEADER RDS
    file_xlsx.create_sheet('RDS')
    sheet = file_xlsx['RDS']
    sheet.append(['id', 'engine', 'status', 'type', 'local', 'idAccount'])
    #HEADER S3
    file_xlsx.create_sheet('S3')
    sheet = file_xlsx['S3']
    sheet.append(['name', 'local', 'idAccount'])

    #HEADER ELB
    file_xlsx.create_sheet('ELB')
    sheet = file_xlsx['ELB']
    sheet.append(['name', 'type', 'vpcId', 'state','idAccount'])

    #HEADER VPC
    file_xlsx.create_sheet('VPC')
    sheet = file_xlsx['VPC']
    sheet.append(['id', 'ipRange', 'state', 'name', 'idAccount'])

    for account_id in account_dict:
        sheet = None

        try:
            print(account_dict[account_id]['elb'])

            if account_dict[account_id]['ec2']:
                sheet = file_xlsx['EC2']
            
                for ec2 in account_dict[account_id]['ec2']:
                    ec2.append(int(account_id))  #add idAccount in last column
                    sheet.append(ec2)

            if account_dict[account_id]['rds']:
                sheet = file_xlsx['RDS']

                for rds in account_dict[account_id]['rds']:
                    rds.append(int(account_id))  #add idAccount in last column
                    sheet.append(rds)

            if account_dict[account_id]['s3']:
                sheet = file_xlsx['S3']

                for s3 in account_dict[account_id]['s3']:
                    s3.append(int(account_id))  #add idAccount in last column
                    sheet.append(s3)

            if account_dict[account_id]['elb']:
                print('if')
                sheet = file_xlsx['ELB']

                for elb in account_dict[account_id]['elb']:
                    print(account_id, elb)
                    elb.append(int(account_id)) #add idAccount in last calumn
                    sheet.append(elb)

            if account_dict[account_id]['vpc']:
                sheet = file_xlsx['VPC']

                for vpc in account_dict[account_id]['vpc']:
                    vpc.append(int(account_id)) #add idAccount in last calumn
                    sheet.append(vpc)

        except KeyError as error:
            #service not find in account
            pass

    with open('log.json', 'w') as f:
        json.dump(account_dict, f, indent=2)
    
    file_xlsx.save('AWS.xlsx')
    file_xlsx.close()
'''
def getIdAccounts():
    pwd=os.getcwd()
    pattern_regex = re.compile(r'^\d{12}$')

    ls = os.listdir(pwd)

    account_list = [name for name in ls if os.path.isdir(os.path.join(pwd, name)) and pattern_regex.match(name)]

    return account_list
'''
def getServices():
    account_id_pwd = os.getcwd()
    
    service_list = os.listdir(os.getcwd())
    service_dict = dict()

    for service_name in service_list:
        os.chdir(service_name)  #cd <servide_name>
        service_dict[service_name] = list()

        for service_file_name in os.listdir():
            if 'ec2' in service_file_name:
                getEC2FromFile(service_file_name)
            
            elif 'rds' in service_file_name:
                getRDSFromFile(service_file_name)

            elif 's3' in service_file_name:
                getS3FromFile(service_file_name)

            elif 'elb' in service_file_name:
                getELBFromFile(service_file_name)
            
            elif 'vpc' in service_file_name:
                getVPCFromFile(service_file_name)

        os.chdir(account_id_pwd)    #cd ..

    if ec2_list:
        service_dict['ec2'] = ec2_list
    if rds_list:
        service_dict['rds'] = rds_list
    if s3_list:
        service_dict['s3'] = s3_list
    if elb_list:
        service_dict['elb'] = elb_list
    if vpc_list:
        service_dict['vpc'] = vpc_list

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

def getRDSFromFile(file_name):
    rds_json = None
    rds_region = getRegionOfFileName(file_name)
    global rds_list

    with open(file_name, 'rb') as file_json:
        rds_json = json.load(file_json)
    
    for db_instance in rds_json['DBInstances']:
        rds_value = list()

        rds_value.append(db_instance['DBInstanceIdentifier'])
        rds_value.append(db_instance['Engine'])
        rds_value.append(db_instance['DBInstanceStatus'])
        rds_value.append(db_instance['DBInstanceClass'])
        rds_value.append(rds_region)

        rds_list.append(rds_value)

def getS3FromFile(file_name):
    s3_json = None
    s3_region = getRegionOfFileName(file_name)
    global s3_list

    with open(file_name, 'rb') as file_json:
        s3_json = json.load(file_json)
    
    for bucket in s3_json['Buckets']:
        s3_value = list()

        s3_value.append(bucket['Name'])
        s3_value.append(s3_region)

        s3_list.append(s3_value)

def getELBFromFile(file_name):
    elb_json = None
    elb_json = getRegionOfFileName(file_name)
    global elb_list

    with open(file_name, 'rb') as file_json:
        elb_json = json.load(file_json)

    for elb in elb_json['LoadBalancers']:
        elb_value = list()
        
        elb_value.append(elb['LoadBalancerName'])
        elb_value.append(elb['Type'])
        elb_value.append(elb['VpcId'])
        elb_value.append(elb['State']['Code'])
        
        elb_list.append(elb_value)

def getVPCFromFile(file_name):
    vpc_json = None
    vpc_region = getRegionOfFileName(file_name)
    global vpc_list

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
        vpc_value.append(vpc_region)
        vpc_list.append(vpc_value)
    #for vpc in vpc_list:
    #    print(vpc)
'''
main()