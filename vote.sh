#!/bin/bash

# author: Samar Acharya

# I'm voting to Menuka Paudel by default
# as she's truly talented
# and she can not do what most of us can do
# yet she is happy and hard-working
contestant_id="${1:-10}"
email="${VOTE_EMAIL:-samarhaxx@yopmail.com}"
name="${VOTE_NAME:-Samar}"
country="${VOTE_COUNTRY:-US}"

response=$(curl -sS http://ap1.tv/nepalIdol/api/emailVoting -d \
  "email=${email}&name=${name}&country=${country}&contestant_id=${contestant_id}")

echo "${response}"
