#!/usr/bin/python

data_parsed = open('/home/toca/ansible_lb_automation/ansible/ips.txt', 'r')

drogas = data_parsed.read()

def slicer(my_str,sub):
   index=my_str.find(sub)
   if index !=-1 :
         return my_str[index:] 
   else :
         raise Exception('Sub string not found!')


ip = drogas.split(',')
print ip[0]
droguinhas = slicer(drogas,',')
droguinhas_nova = droguinhas[1:]
zezinho = open('/home/toca/ansible_lb_automation/ansible/ips.txt', 'w')

zezinho.write(droguinhas_nova)
