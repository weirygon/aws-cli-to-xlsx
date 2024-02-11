import os
import sys

modules = dict()

def __init():   #Import directory resources/
    pwd_root = os.getcwd()
    os.chdir(pwd_root + '/getServices/services')
    sys.path.append(os.getcwd())

    for resource_file in os.listdir():
        if resource_file.endswith('.py'):
            resource_name = resource_file.split('.')[0]
            modules[resource_name] = __import__(resource_name)

    os.chdir(pwd_root)

def all():
    print('ALL')

    print(os.getcwd())

    dict_services = dict()

    for service_name in os.listdir():
        dict_services[service_name] = dict()
        os.chdir(service_name)

        for file_name in os.listdir():
            region = __getRegionFromFileName(file_name)
            dict_services[service_name][region] = list()

            dict_services[service_name][region].append(modules[service_name].get(file_name))
            print(dict_services)
            
        os.chdir('..')  #cd <services>

def ec2():
    try:
        os.chdir('ec2/')
    except FileNotFoundError:
        print('[-] Not found EC2!')
        return None
    
    print('[+] Find EC2!')

    ec2_module = modules['ec2']
    ec2_dict = dict()

    for file_name in os.listdir():
        region = __getRegionFromFileName(file_name)

        try:
            ec2_dict[region]
        except KeyError:    #Putting region for the first time
            ec2_dict[region] = list()
        finally:
            ec2_dict[region].append(ec2_module.get(file_name))

    os.chdir('..')
    
    return ec2_dict

def __getRegionFromFileName(file_name):
    file_name = file_name.split('-', 1)
    file_name = file_name[1].split('.')
    
    return file_name[0]

if __name__ != "__main__":
    __init()
