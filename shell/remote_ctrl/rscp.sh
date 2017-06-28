
expect -c "
spawn scp -P 30077 abc@10.134.34.69:$1 ./
expect {
    \"*assword\" {set timeout 300; send \"abc123\r\";}
    \"yes/no\" {send \"yes\r\"; exp_continue;}
}
set timeout 1800
expect eof"
