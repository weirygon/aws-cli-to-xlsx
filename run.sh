#!/bin/bash

#Terminal Colors Output

color_red="\e[31m"
color_green="\e[32m"
color_yellow="\e[33m"
color_reset="\e[0m"

regions=(
    "us-east-1"
    "us-east-2"
    "sa-east-1"
    "us-west-2"
    )

init(){
    output=$(aws sts get-caller-identity)


    # Extrai o valor da propriedade "Account" (owner)
    account_id="${output#*\"Account\": \"}"
    account_id="${account_id%%\"*}"

    mkdir -p $account_id && cd $account_id

}

getRDS(){
    local region=$1

    rds=$(aws rds describe-db-instances --region $region --output json)

    if [ "$(echo "$rds" | wc -l)" -gt 3 ]; then
        echo -e "${color_green}[+] Find RDS! ${color_reset}"
        mkdir -p rds
        echo "$rds" > ./rds/rds-$region.json
        
    else
        echo -e "${color_red}[-] Not found RDS! ${color_reset}"

    fi
}

getEC2(){
    local region=$1

    instances=$(aws ec2 describe-instances --region $region --output json)

    if [ "$(echo "$instances" | wc -l)" -gt 3 ]; then
        echo -e "${color_green}[+] Find EC2!${color_reset}"
        mkdir -p ec2
        echo "$instances" > ./ec2/ec2-$region.json
        
    else
        echo -e "${color_red}[-] Not found EC2! ${color_reset}"

    fi

}

getS3(){
    buckets=$(aws s3api list-buckets --output json)

    if [ "$(echo "$buckets" | wc -l)" -gt 7 ]; then
        echo -e "${color_green}[+] Find S3! ${color_reset}"
        mkdir -p s3
        echo "$buckets" > ./s3/s3-global.json
        
    else
        echo -e "${color_red}[-] Not found S3! ${color_reset}"

    fi
}

getELB(){
    elb=$(aws elbv2 describe-load-balancers --region $region --output json )

    if [ "$(echo "$elb" | wc -l)" -gt 3 ]; then
        echo -e "${color_green}[+] Find ELB! ${color_reset}"
        mkdir -p elb
        echo "$elb" > ./elb/elb-$region.json
        
    else
        echo -e "${color_red}[-] Not found ELB! ${color_reset}"

    fi
}

getVPC(){
    vpc=$(aws ec2 describe-vpcs --region $region --output json)

    if [ "$(echo "$vpc" | wc -l)" -gt 3 ]; then
        echo -e "${color_green}[+] Find VPC!${color_reset}"
        mkdir -p vpc
        echo "$vpc" > ./vpc/vpc-$region.json
    
    else
        echo -e "${color_red}[-] Not found VPC!${color_reset}"

    fi
}

main(){
    init
    
    #Global
    echo -e "${color_yellow}[ ] Global ${color_reset}"

    getS3

    echo "========================="
    #Regions
    for region in "${regions[@]}"
    do
        echo -e "${color_yellow}[ ] Region: $region... ${color_reset}"

        getEC2 $region
        getRDS $region
        getELB $region
        getVPC $region

        echo "========================="
    done

}

main