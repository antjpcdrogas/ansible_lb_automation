#!/usr/bin/python
import os
import sys

data_parsed = open(sys.argv[1], 'r')
ip_string = data_parsed.read()
data_parsed.close()

def slicer(my_str,sub):
   index=my_str.find(sub)

   if index !=-1 :   
         return my_str[index:] 

ip = ip_string.split(',')
new_ip =  ip[0].replace('\r','')
print new_ip
remaining_ip_string = slicer(ip_string,',')

if not remaining_ip_string:
  exit(1)

final_ip_string = remaining_ip_string[1:]
file_handler = open(sys.argv[1], 'w')
file_handler.write(final_ip_string)
file_handler.close()
