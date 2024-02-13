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

        account_dict[id_account] = getService.all()
        
        os.chdir(pwd_root)

    with open('log.json', 'w') as file_json:
        json.dump(account_dict, file_json, indent=2)

    saveInXlxs(account_dict)
    
def saveInXlxs(account_dict):
    file_xlsx = openpyxl.Workbook()

    for id_account in account_dict:
        for service_name in account_dict[id_account]:
            try:
                file_xlsx[service_name.upper()]
            except KeyError:
                file_xlsx.create_sheet(service_name.upper())
            finally:
                sheet = file_xlsx[service_name.upper()]
                
                for region in account_dict[id_account][service_name]:
                    for row in account_dict[id_account][service_name][region]:
                        row.append(region)
                        row.append(id_account)
                        sheet.append(row)

    file_xlsx.save('AWS.xlsx')
    file_xlsx.close()

def getIdAccounts():
    pwd=os.getcwd()
    pattern_regex = re.compile(r'^\d{12}$')

    ls = os.listdir(pwd)

    account_list = [name for name in ls if os.path.isdir(os.path.join(pwd, name)) and pattern_regex.match(name)]

    return account_list

main()