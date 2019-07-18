# ansible_lb_automation

Scenario

You work somewhere.
Your job requires you to automate API calls used in the creation of a production environment for our services.
We have just acquired a new load balancing solution that exposes a REST API which allows us to fully automate it and integrate it with our automated deployment pipelines.
You do not have to worry about deploying the service or it's provisioning, assume all VMs/Containers were deployed previously and are already running.s

Setup

You need to have Docker installed in order to spin up the load balancing API container.
To spin up the API locally run the following command:
docker run -p 9090:8080 -d <location>
The API is now running on http://localhost:9090/, you will find the documentation for the API in http://localhost:9090/doc

Challenge
NOTE:

All text shown as preformated should be configurable, the values shown are examples only
All missing information, such as load balancer, service and monitor names, can be chosen by you, in the way you see fit.

The service in question is called awesomeapp, serves traffic on port 8080 and exposes a health monitor in /webping with the content OK if everything is ok with the service, otherwise it answers with FAIL.
For every deployment, new IPs are automatically assigned to the boxes.
We want to balance the traffic with the following FQDN awesomeapp.blip.pt with a TTL of 1 minute. The services should be queried for health check every 5 seconds by the load balancer.
Using the language, tools or framework of your choice, automate the deployment of a service using a rolling update strategy.
The final result should be called in the following format <program> <new_ip_1> <new_ip_2> <new_ip_3>, this would place the 3 new IPs under the load balancers and remove the old ones.

Submission
Add a README or change this one, with the comments you see fit and an explination of how and why you chose your approach.
Commit and push your solution to a branch on this repo and open a MR to master.



#################################################################################################################################

Challenge Solution


This challenge was solved using the automation tool Ansible and python.
Development environment:
OS: Fedora 29 4.18.16-300.fc29.x86_64
Ansible: 2.8.1
Python: 2.7.15
I know that Ansible is not by far the best tool to solve this challenge but is the tool that i am more confortable.
Writing a python script could be boring and i wanted to try something diferent.
Since Ansible was not created to solve this kind of tasks i had more troubles because of it:

iterating through a dictionary or list sequentially in a block of tasks is not possible
in some situations set_fact only registers the last entry from a dict/list
Modern list manipulation is almost impossible( to bypass this point a python script was written and included in the playbook)

Expected pre-requisites:
It is expected that a infraestruture will all components( binded to the core LB) is already present.
Main playbook to solve the challenge: update_ip.yml
Usage: ansible-playbook update_ip.yml -k -e new_ips=<ip1,ip2,...>
ex: ansible-playbook update_ip.yml -k -e new_ips=10.118.0.1,10.118.0.2,10.118.0.3,10.118.0.4
The library libselinux-python needs to be installed before.
The challenge was split in 4 phases to resume playbook behavior.
1º phases:

Collect all existent components on the API( only loadbalancers and services collected. Theres no point collecting monitor because we already have all the necessary info from the previous components)
Create temporary loadbalancer( this LB will be used to perform QA tests after the ip change )

2º phases:

Destroy first service collected
Recreate it using the same specs as before with an updated IP ( ansible extra var "new_ips")

3º phases:

Bind first service with temporary loadbalancer
Perform QA tests
Unbind first service with temporary loadbalancer

4º phases:

Bind first service with main loadbalancer
repeat all previous steps untill all services are updated or all ips used.
destroy temporary load balancer

Execution time with 3 services: 28 seg
Playbook finish when all services have been update or when all IPs have been used.
Variable that contains the API address is located at files/global_vars.yml
Additionally from what as been asked in the challenge i created 2 more playboks to help during the development process. The purpose of these playbooks is to create and delete an entire infrastruture.
Usage: ansible-playbook create_infra.yml
This play create 1 LoadBalancer, 3 services and 3 monitor  with all components binded.
This plays are distributed hierarchically by roles, 1 per component and 1 more for the bind.
Features that could be implemented:

Logging
Create objects per item collected
Choose with services should be updated first based on metrics or others factors.
