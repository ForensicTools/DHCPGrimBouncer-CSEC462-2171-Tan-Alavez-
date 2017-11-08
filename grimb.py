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
# uncomment this to make a bhv csv
    #bhv_command = r'C:\browsinghistoryview-x64\BrowsingHistoryView.exe /scomma C:\GrimBouncer\Browsing_History'
    #os.system(bhv_command + "\\" + str(time.strftime("%Y-%m-%d_T%H%M%S"))  + ".csv")    # csv file generated
 
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
        for row in reader:
            url = row[0]
            if(url[0:4] == "http"):
##                for r in csv.reader(newfile, delimiter=','):
##                    if(url == r[0]):
##                        pass
                cert_lst= []
                cert_lst.append(row[0])     # URL
                cert_lst.append(row[2])     # date and time
                cert_lst.append(row[3])     # times visited

                ossl = os.system(

                wr.writerow(cert_lst)
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
