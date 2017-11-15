########################################################################
###
### file: grimb.py
###
### Implementation script for Grim Bouncer 
###
### Windows version
###
### authors: Benny Tan bt4168, Jhony Alavez jia2707
###
########################################################################

import sys
import os
import re
import platform
import time
import glob
import csv
import subprocess

##readfile = open("test.webtest", 'r')
##
##for line in readfile:
##    lst = line.split("<Request", "</Request>")
####    if(re.findall(r'Upgrade-Insecure-Requests', line)):
####        print(lst)
##    print(lst)
##
##readfile.close()

###########
# function: bhv
#
# Description: Runs Browsing History executable. Generates plaintext file
#
# Return: .csv file
###########
def bhv():			 	
    if(os.path.isdir("C:\browsinghistoryview-x64")):
        print("Yes")
    else:
        print("No")

    URL_folder = r'C:\GrimBouncer\Browsing_History'         # path folder to store URL csv files
    if not os.path.exists(URL_folder):                      # check to see if folder already exists
        os.makedirs(URL_folder)                             # create the folder
##    #uncomment this to make a bhv csv
##    bhv_command = r'C:\browsinghistoryview-x64\BrowsingHistoryView.exe /scomma C:\GrimBouncer\Browsing_History'
##    os.system(bhv_command + "\\" + str(time.strftime("%Y-%m-%d_T%H%M%S"))  + ".csv")    # csv file generated

############
# function:     grab_cert
# 
#
#
#
############
def grab_certs(entry):
    # 1) loop through url_certs set and split URLs by domains
    # 2) check again for duplicates and remove
    # 3) map domains to subdomains ... somehow
    domains = set()
    for url in entry:
        url = url.split("//")[-1].split("/")[0]
        if(url not in domains):
            domains.add(url)
    testfile = open("testf.csv", 'w')
    for el in domains:
##        ossl = subprocess.check_output("openssl s_client -connect " + el
##                                       + ":443 | openssl x509 -noout -text")
##        for row in ossl.split('\n'):
##            print(row)
##    p = subprocess.Popen("openssl s_client -connect " + "example.com"
##                                       + ":443 | openssl x509 -noout -text", stdout=subprocess.PIPE)
##    out, _ = p.communicate()
##    print(out)
        p = os.popen("openssl s_client -connect " + el + ":443 | openssl x509 -noout -text")
        testfile.write(p.read())
    testfile.close()
############
# function:     gen_CSV
#
# Description:  Generates a new CSV containing information from bhv
#               and OpenSSL output
############
def gen_csv(filename):
    # delimit by commas
    # grab first element(URL) and third element(time and date visited)
    # use dict to store?
##    f = open(r'C:\GrimBouncer\Browsing_History\\' + filename, 'r')

    certcsv_folder = r'C:\GrimBouncer\Certificate_CSVs'         # path folder to store URL csv files
    if not os.path.exists(certcsv_folder):                      # check to see if folder already exists
        os.makedirs(certcsv_folder)                             # create the folder
    newfile = open(r'C:\GrimBouncer\Certificate_CSVs\\' + filename[:-4] + '_cert.csv', 'w')

    with open(r'C:\GrimBouncer\Browsing_History\\' + filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        wr = csv.writer(newfile, quoting=csv.QUOTE_ALL)
        #categories = ['objectName','URL','datetime','URL'

        counter = 0
        entry = set()
        for row in reader:
            url = row[0]
            if(url[0:4] == "http"):
##                for r in csv.reader(newfile, delimiter=','):
##                    if(url == r[0]):
##                        pass
                cert_lst = []
                cert_lst.append(row[0])     # URL
                cert_lst.append(row[2])     # date and time
                cert_lst.append(row[3])     # times visited

                #ossl = os.system(
                if(url not in entry):
                    wr.writerow(cert_lst)
                    entry.add(url)          # prevents duplicate entries
                    
        grab_certs(entry)                   # 

    f.close()
    newfile.close()

############
# function: main
#
# Description: Driver for program, grimb.
############
def main():    

    print("Welcome to the GrimBouncer backend interface!")  # welcome message

    operating_system = platform.system()    # check operating system for Windows
    if(operating_system != "Windows"):
        print("OS is not Windows")
        return

    bhv()           # call BrowsingHistoryView.exe to generate a .txt file

    print("\n----------------------------------")
    print("Current browsing history logs: ")
##    os.listdir(r'C:\browsinghistoryview-x64\URL_Folder')
    os.chdir(r'C:\GrimBouncer\Browsing_History')
    for file in glob.glob("*"):
        print(file)

    print("-----------------------------------\n\n\n")
    filename = input("Enter browsing history log: ")

    gen_csv(filename)


main()
