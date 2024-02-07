#!/bin/bash

regions=(
    "us-east-1"
    "us-east-2"
    "sa-east-1"
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
        echo "[+] Find RDS!"
        mkdir -p rds
        echo "$rds" > ./rds/rds-$region.json
        
    else
        echo "[-] Not found RDS!"

    fi
}

getEC2(){
    local region=$1

    instances=$(aws ec2 describe-instances --region $region --output json)

    if [ "$(echo "$instances" | wc -l)" -gt 3 ]; then
        echo "[+] Find EC2!"
        mkdir -p ec2
        echo "$instances" > ./ec2/ec2-$region.json
        
    else
        echo "[-] Not found EC2!"

    fi

}

getS3(){
    buckets=$(aws s3api list-buckets --output json)

    if [ "$(echo "$buckets" | wc -l)" -gt 7 ]; then
        echo "[+] Find S3!"
        mkdir -p s3
        echo "$buckets" > ./s3/s3-global.json
        
    else
        echo "[-] Not found S3!"

    fi
}

getELB(){
    elb=$(aws elbv2 describe-load-balancers --region $region --output json )

    if [ "$(echo "$elb" | wc -l)" -gt 3 ]; then
        echo "[+] Find ELB!"
        mkdir -p elb
        echo "$elb" > ./elb/elb-$region.json
        
    else
        echo "[-] Not found ELB!"

    fi
}

main(){
    init
    
    #Global
    echo "[ ] Global"

    getS3

    echo "========================="
    #Regions
    for region in "${regions[@]}"
    do
        echo "[ ] Region: $region..."

        getEC2 $region
        getRDS $region
        getELB $region

        echo "========================="
    done

}

main