#!/bin/bash

regions=(
    "us-east-1"
    "us-east-2"
    "us-west-1"
    "us-west-2"
    "sa-east-1"
)

for region in "${regions[@]}"
do
    echo "Region: $region"

    instances=$(aws ec2 describe-instances --region $region --output json)

    if [ "$(echo "$instances" | wc -l)" -eq 3 ]; then
        echo "Não existe EC2 na regiao"
    
    else
        echo $instances >> ./ec2/ec2-$region.json

    fi
    
done
