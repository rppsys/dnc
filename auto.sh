#!/usr/bin/env bash
# Filename: auto.sh

clNoColor='\033[0m'
clBlack='\033[0;30m'     
clRed='\033[0;31m'     
clGreen='\033[0;32m'     
clOrange='\033[0;33m'     
clBlue='\033[0;34m'     
clPurple='\033[0;35m'     
clCyan='\033[0;36m'     
clLight_Gray='\033[0;37m'
clDark_Gray='\033[1;30m'
clLight_Red='\033[1;31m'
clLight_Green='\033[1;32m'
clYellow='\033[1;33m'
clLight_Blue='\033[1;34m'
clLight_Purple='\033[1;35m'
clLight_Cyan='\033[1;36m'
clWhite='\033[1;37m'

if [[ $1 = 'pull' ]]
then
	git pull
fi

if [[ $1 = 'push' ]]
then
	msg="Auto $(date)"  
	git add --all
	git commit -m "$msg"
	echo -e "${clYellow}"
	git push
	echo -e "${clNoColor}"
	echo ""
	echo -e "${clLight_Red}Pushou ${clYellow}''$msg''${clLight_Red}"
	echo -e "${clNoColor}"
	echo ""	
fi
