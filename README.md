# tri0p

<p align="center">
    <img src="https://lh3.googleusercontent.com/proxy/ONK5xbQBmAYn3-P-o0h7X0sot29r4iLSl8EfsERgM8cYET_LU2UB84ppH9fE9GQK_JkN8g" alt="alt text" width="50" height="50">
</p>

### tri0p is a shodan base script for scan multiple subnets ans use python audit script

this tool is for people that need to scan multiple subnet or ip in a fast way , with the minimal subscriptions of shodan

P.S: you need a API key , use the -api flag to use it

## use 

put your subnet or ip in the IP_list.txt file this way.
>x.x.x.x/xx \
>x.x.x.x \
>x.x.x.x/xx \
x.x.x.x/xx 

If you whant a fast representations use the -base flag.
this will show you the service running and open port 

for a graph representation of the number or port and services open use the -gr flag 

after that you can use the script while targeting a specified service / port , with the flag -pr

if you have a python audi script that take for argument ONLY the ip and the port , that target found services , use the -sc flag and read the instructions 