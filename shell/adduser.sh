#!/bin/bash
creat_user(){
useradd $user
echo "$pass" | passwd --stdin $user
}

let seed=($RANDOM%2+1)

users='lyl ffy zhoumi wch chr loki cyl llm dlj wdh'

for user in $users
do
	pass=$user"123"
	homedir="/search/data$seed/$user"
	useradd $user -d $homedir -m -g users

	echo "$pass" | passwd --stdin $user

	let seed=seed%2+1

	ln -s $homedir /home/$user
done

