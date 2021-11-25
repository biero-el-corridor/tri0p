# -*- coding: utf-8 -*-
"""
Name: Harydan
Created on Mon Nov  8 10:45:21 2021
@author: ecordier
this script dont have the pretentions of replace shodan but this script give adventage like
    --run subnet scaning in mass from file
    -use audit script on targeted service or service verions
    --all the ip / subnet who is in IP scan will be scann , no user entry will be use for
        the selections of ip range
add the following feature

        
"""
import collections
import shodan
import time
import os
import argparse
import matplotlib.pyplot as plt
import sys

parser = argparse.ArgumentParser()
####if word doe not contain / 
parser.add_argument('-pr','--product', help='service use ex: OpenSSH or Apache', action="store_true")
parser.add_argument('-base', '--basic', help='show IP , port, and service + version ', action="store_true")
parser.add_argument('-sc', '--script', help='add audit script ', action='store_true')
parser.add_argument('-api_Key', '--api_key' , help='add the api key of your shodan account',type=str)
parser.add_argument('-gr', "--graph", help='whil show the graph', action="store_true")
#parser.add_arguemnt('-s', '--script', help='try an audit script on the desired service / port',type=str)

args = parser.parse_args()
#print(args.port)
class Shodan_search():
    #definitions of 2 main variable (api_key and api)
    def __init__(self):
        #retreve of the api key
        self.API_key = args.api_key
        #funtions that run shodan scan
        self.api = shodan.Shodan(self.API_key)
    
    #this functions whill enter the informations about the script we whant to use
    def add_script(self):

        print("add the aplsolute file path to the directory of your script, if not satisfied pres Ctrl+c \n")
        self.filePath = input()
        #affichage du file path
        print('you are curently in the following file path', end='')
        os.getcwd()
        #déplacement dans le fichier qui contient le script 
        os.chdir(self.filePath)
        print("write the begening of the script launght ex: python3 ssh_audit.py \n")
        self.Header_script = input()
        
        print("the folowing questions depend of the spécific argument of your audit script\n")
        print("write down the name of the argument for the ip target ex: -ip | --ip_dest \n")
        self.ip_argument = input()
        
        print("write down the name of the argument for the port target ex: -p | -port | --port_dest \n")
        self.port_argument = input()
        
        print("for the last questions put the name of the service or the name + versions down bellow")
        self.Key_Word = input()
    
    #found in shodan base on the subnet
    
    def file_net_not_defined_product(self):
         with open("IP_list.txt", "r") as file:
            self.lines = file.readlines()
            
            self.Product_List = []
            self.IP_List = []
            self.Port_List = []
            self.IP_cont = 0 
            if len(self.API_key) != 32:
                print("the given api_key have not the right size")
                sys.exit()
            #lancement de add_script
            if args.script:
                self.add_script()
            
            for self.line in self.lines:
                #detect if the line is a subnet or not 
                if ("/" and ".")  in self.line:
                    self.IsASubnet = True
                else:
                    self.IsASubnet = False
                
                #time to sleep , use for not bee kicked out from shodan 
                time.sleep(0.21)
                
                #search for subnet or ip 
                if self.IsASubnet == True:
                    res = self.api.search(f'net:{self.line}')
                else:
                    res = self.api.search(f'ip:{self.line}')
                #point = self.ai

                for item in res['matches']:
                    try:
                        try:
                            if item['ip_str'] in self.IP_List: 
                                pass
                            else:
                                self.IP_List.append(item['ip_str'])
                                self.IP_cont += 1 
                                    
                        except:
                            print("pass ip str ")
                        try:
                            
                            if item['port'] in self.Port_List:
                                self.Port_List.append(item['port'])
                                pass
                            else:
                                self.Port_List.append(item['port'])
                        except:
                            print("pass port")
                        try:
                            self.Product_Versions = f"{item['product']} {item['version']}"
                            #print("this sis the product of this line {}".format(item['prouct']))
                            
                            if self.Product_Versions in self.Product_List:
                                self.Product_List.append(self.Product_Versions)
                            else:
                                self.Product_List.append(self.Product_Versions)
                        except:
                            print("error in the producte area")
                        print('the ip is : ',item['ip_str'])
                        print('the port is : ',item['port'])
                        try:
                            print('the service is : ', item['product'])
                        except:
                            pass
                        
                        #call du script pour ssh audit
                        if args.script:
                            if self.Key_Word in self.Product_Versions and "." in self.Product_Versions:

                                #print("le contenue de product versions et ",self.Product_Versions )
                                self.ip = item['ip_str']
                                self.port = item['port']
                                self.Output_File_Name = f'audit_script_{self.ip}'
                                print(self.Output_File_Name)
                                self.launght_script = f'{self.Header_script} {self.ip_argument} {self.ip} {self.port_argument} {self.port} > {self.Output_File_Name}.txt'
                                try:
                                    print(self.launght_script)
                                    #call the line that will instanciate the script
                                    os.system(self.launght_script)
                                    
                                    #self.line = f"python3 ssh-audit.py -p {self.port} {self.ip} > {self.Output_File_Name}.txt "
                                except:
                                    print("error in openssh")
                        #print(item['data'])
                    except:
                        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                        print(f"\n the line:{self.line} have trubble find the data fiels \n ")
                        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            
                
                
                print(f"\n the line :{self.line} have been tested \n ")
            
            """
            yourList = []
    
            with open('yourNewFileName.csv', 'w', ) as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                for word in yourList:
                    wr.writerow([word])
                    
            """
            print(self.IP_List, "\n")
            
            for i in range(len(self.IP_List)):
                print(self.IP_List[i])
                i += 1
            
            print(collections.Counter(self.Port_List),"\n")
            #créations du dictionnaire pour la représentations graphique
            print("\n")
            print(self.Port_List)
            print("\n")
            print(collections.Counter(self.Product_List),"\n")
            
            print(f"le nombre d'ip et de {self.IP_cont}")
            
            #if the -gr or --graph is enable
            if args.graph:
                self.Port_dict = collections.Counter(self.Port_List)
                
                #apelle de la fontions de représentations graphique 
                self.Plt_Show(self.Port_dict)
                self.Product_List = collections.Counter(self.Product_List)
                #apelle de la fontions de représentations graphique 
                self.Plt_Show(self.Product_List)
            print("\n")
            
    def Plt_Show(self,Dictionary):
        self.dict = Dictionary
        ########################################################
        #présentations des valeur dans un graph
        #######################################################
        plt.bar(range(len(self.dict)), list(self.dict.values()), align='center')
        plt.xticks(range(len(self.dict)), list(self.dict.keys()), rotation=90)
        #plt.tick_params(axis='x', rotation=70)
        #print(self.ConteurIIs)
        
        plt.text(0,0,'Hello World !',horizontalalignment='center',verticalalignment='center')
        #plt.plot
        plt.show()    
        #######################################################
    #found on shodan based on the subnet and the product
    def file_net_defined_product(self,Product):
        #self.net = Net
        self.product = Product
        #get the product versions 
        print("Enter versions of service (if none pres enter)")
        self.version = input()        
        print(f"the versions that you have chose is {self.version}")
        #selections between product with or wothout showing versions
        if self.version == "" or self.version == " ":
            self.Product_version = f"product:{self.product}"
        else:
            self.Product_version = "product:{self.product} version:{self.version}"
        
        #changer la value du nom du fichier par le fichier selectionne
        #
        with open("IP_list.txt", "r") as file:
            self.lines = file.readlines()
            for self.line in self.lines:
                if len(self.API_key) != 32:
                    print("the given api_key have not the right size")
                    break
                #définitions d'un temps de repos pour éviter les probléme lier a de trop 
                #nombreuse requéte
                time.sleep(0.21)
                #search in shodan whit the 2 posisional argument
                self.res = self.api.search(f'net:{self.line} {self.Product_version}')
                print("la valeur de res et {self.res}")
                try:   
                    for item in self.res['matches']:
                        print(item['ip_str'])
                        print(item['port'])
                        #call       
                except: 
                    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                    print(f"\n the line:{self.line} have trubble find the data fiels \n ")
                    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                
                print(f"\n the line :{self.line} have been tested \n ")

if __name__ == "__main__":
    # Define the program description
    #permet de faire apelle a des script python a appliquer au différente adresse ip        
    #net:'220.130.170.0/24' product:"OpenSSH"
    Res = Shodan_search()
    if args.basic:
        Res.file_net_not_defined_product()
    if args.product:    
        Res.file_net_defined_product(args.product)