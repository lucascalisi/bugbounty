#!/bin/bash

subdomains=$(curl https://certspotter.com/api/v0/certs\?domain\=$1 | jq '.[].dns_names[]' | sed 's/\"//g' | sed 's/\*\.//g' | uniq)
for i in $asd
do
	echo $i |httprobe
done
