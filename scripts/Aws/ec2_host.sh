#!/bin/bash
#wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1R6ngkpkf7DIhwqlr-dFXziRyel3_8fGO' -O deploy.sh

sudo yum update

sudo yum install --downloadonly --downloaddir=/home/ec2-user/deps/ python3

sudo yum install deps/*
sudo pip3 install proxy.py

wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1MEHZsztAkQUv6a6MCX805b8LQM6LG_WI' -O key.pem
chmod 400 key.pem

wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1EYqtdJiTJ8b0-uWUKcGzWlJT8yJ6ojHp' -O server.py
scp -i key.pem server.py ec2-user@10.0.1.10:~

scp -r -i key.pem deps/ ec2-user@10.0.1.10:~/deps
ssh -i key.pem ec2-user@10.0.1.10 "sudo rpm -ivh deps/*"
