
expect -c "
spawn scp -P 30077 $* abc@10.134.34.69:
expect {
    \"*assword\" {set timeout 30000; send \"abc123\r\";}
    \"yes/no\" {send \"yes\r\"; exp_continue;}
}
expect eof"
