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
from datetime import datetime


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
##    bhv_command = r'C:\browsinghistoryview-x64\BrowsingHistoryView.exe /scomma C:\GrimBouncer\Browsing_History'
##    os.system(bhv_command + "\\" + str(time.strftime("%Y-%m-%d_T%H%M%S"))  + ".csv")    # csv file generated

############
# function:     gen_csv
#
# Description:  Generates a new CSV containing information from bhv
#               and OpenSSL output
############
def gen_cert(filename):
    # delimit by commas
    # grab first element(URL) and third element(time and date visited)
    # use dict to store?

    certcsv_folder = r'C:\GrimBouncer\Certificate_CSVs'     # path folder to store URL csv files
    if not os.path.exists(certcsv_folder):                  # check to see if folder already exists
        os.makedirs(certcsv_folder)                         # create the folder
    certfile = open(r'C:\GrimBouncer\Certificate_CSVs\\' + filename[:-4] + '_certs.csv', 'w')

    domains = set()                # list to store just domains
    domains_certs = dict()      # dict to store domains and respective cert information
    FQDN = set()                   # list to store full domains

    # we know:
    #   browsing history csv has URLs
    # we want:
    #   use URLs 

    with open(r'C:\GrimBouncer\Browsing_History\\' + filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        write_to_cert = csv.writer(certfile, quoting=csv.QUOTE_ALL)
        write_to_export = csv.writer(exportfile, quoting=csv.QUOTE_ALL)

        for row in reader:
            url = row[0]
            if(url[0:4] == "http"):
                if(url not in FQDN):
                    FQDN.add(url)      # FQDN now has all the URLs

        for dn in FQDN:
            dn = dn.split("//")[-1].split("/")[0]
            if(dn not in FQDN):
                domains.add(dn)                # domains now has all domains

        lst_domains = []
        lst_domains.extend(domains)

        counting = 0
        for lst in lst_domains:
            counting += 1
        print(counting)

        i = 0
        while(i < len(lst_domains)):
            #for el in lst_domains:
            print("Trying " + lst_domains[i] + "...")           # cert being obtained for
            p = subprocess.Popen("openssl s_client -connect " + lst_domains[i] + ":443 | openssl x509 -noout -text"
                                 , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # uncomment out this block to generate the cert csv
            try:
                std_out, std_error = p.communicate(timeout=450) # time out after 5 minutes
            except subprocess.TimeoutExpired:
                domains_certs[lst_domains[i]] = [b'null']        # return a list containing "null"
                print(str(i + 1) + " has timed out")  # Python check to make sure process is working
            else:
                domains_certs[lst_domains[i]] = std_out.splitlines()
            #write_to_cert.writerow([lst_domains[i], std_out.splitlines()])
                print(str(i + 1) + " successful")  # Python check to make sure process is working
            i += 1
        print("Total certs attempted: " + str(i))

        # dict domains_certs now has the domains as the key and their certs as the value
        for key, value in domains_certs.items():
            cert_lst = []
            
##            write_to_cert.writerow([key, value])

    certfile.close()          
    f.close()
    exportfile.close()

def gen_export(filename):
    
    exportcsv_folder = r'C:\GrimBouncer\Export_CSVs'        # path folder to store URL csv files
    if not os.path.exists(exportcsv_folder):                # check to see if folder already exists
        os.makedirs(exportcsv_folder)                       # create the folder
    exportfile = open(r'C:\GrimBouncer\Export_CSVs\\' + filename[:-4] + '_export.csv', 'r+')

    no_dupe_URLs = set()

    with open(r'C:\GrimBouncer\Browsing_History\\' + filename, 'r') as bh, open(r'C:\GrimBouncer\Certificate_CSVs\\' + filename[:-4] + '_certs.csv') as cr:
        bh_reader = csv.reader(bh, delimiter=',')
        cr_reader = csv.reader(cr, delimiter=',')
        write_to_export = csv.writer(exportfile, quoting=csv.QUOTE_ALL)
        write_to_export.writerow(["URL","DateVisited","TimesVisited","SigAlgo",
                                  "IssuerC","IssuerO","IssuerOU","IssuerCN",
                                  "SubjectC","SubjectO","SubjectOU","SubjectCN",
                                  "IssueDate","ExpireDate","Security"])

        cr_urls = []
        cr_certs = []
        for cr_row in cr_reader:
            if(cr_row):
                cr_urls.append(cr_row[0])       # store cert csv urls into list
                cr_certs.append(cr_row[1])      # store cert csv certs into list

        months = dict(Jan=1,Feb=2,Mar=3,Apr=4,May=5,Jun=6,
                      Jul=7,Aug=8,Sep=9,Oct=10,Nov=11,Dec=12)

        count = 0
        for bh_row in bh_reader:
            url = bh_row[0]
            if( (url[0:4] == "http") and (url not in no_dupe_URLs) ):
                no_dupe_URLs.add(url)
                temp_url = url                 # temporary value to hold non-duplicate URL
                cert_lst = []
                cert_lst.append(bh_row[0])     # URL
                cert_lst.append(bh_row[2])     # date and time
                cert_lst.append(bh_row[3])     # times visited

                while(count < len(cr_certs)):  # does not work after 250 (size of cert file)
                    if(url.split("//")[-1].split("/")[0] == cr_urls[count]):
                        cert_lst.append(cr_certs[count])
                        if(cert_lst[3] == "[b'null']"):
                            cert_lst.extend(["[b'null']"] * 10)
                            cert_lst.append("Unknown")
                        elif(cert_lst[3] == "[]"):
                            cert_lst.extend(["[]"] * 10)
                            cert_lst.append("Unknown")
                        else:
                        # Issuer 
                            issuer = re.findall(r"\Issuer:(.*)\Validity", cert_lst[3])
                            issuer_str = "".join(issuer)
                            # Issuer C
                            issuer_c = re.findall(r"\C=(.*),", issuer_str)
                            if(issuer_c):
                                cert_lst.append(issuer_c[0].split(",")[0].strip("'"))
                            if(not issuer_c):
                                cert_lst.append("Not listed")
                            # Issuer O
                            issuer_o = re.findall(r"\O=(.*),", issuer_str)
                            if(issuer_o):
                                cert_lst.append(issuer_o[0].split(",")[0])
                            if(not issuer_o):
                                cert_lst.append("Not listed")
                            # Issuer OU
                            issuer_ou = re.findall(r"\OU=(.*),", issuer_str)
                            if(issuer_ou):
                                cert_lst.append(issuer_ou[0].split(",")[0])
                            if(not issuer_ou):
                                cert_lst.append("Not listed")
                            # Issuer CN
                            issuer_cn = re.findall(r"\CN=(.*),", issuer_str)
                            if(issuer_cn):
                                cert_lst.append(issuer_cn[0].split(",")[0].strip("'"))
                            if(not issuer_cn):
                                cert_lst.append("Not listed")
                        # Subject 
                            subject = re.findall(r"\Subject:(.*)\Info", cert_lst[3])
                            subject_str = "".join(subject)

                            # Subject C
                            subject_c = re.findall(r"\C=(.*),", subject_str)
                            if(subject_c):
                                cert_lst.append(subject_c[0].split(",")[0])
                            if(not subject_c):
                                cert_lst.append("Not listed")
                            # Subject O
                            subject_o = re.findall(r"\O=(.*),", subject_str)
                            if(subject_o):
                                cert_lst.append(subject_o[0].split(",")[0])
                            if(not subject_o):
                                cert_lst.append("Not listed")
                            # Subject OU
                            subject_ou = re.findall(r"\OU=(.*),", subject_str)
                            if(subject_ou):
                                cert_lst.append(subject_ou[0].split(",")[0])
                            if(not subject_ou):
                                cert_lst.append("Not listed")
                            # Subject CN
                            subject_cn = re.findall(r"\CN=(.*),", subject_str)
                            if(subject_cn):
                                cert_lst.append(subject_cn[0].split(",")[0].strip("'"))
                            if(not subject_cn):
                                cert_lst.append("Not listed")
                        # Validity
                            # Issue Date
                            issuedate = re.findall(r"\Before:(.*),", cert_lst[3])
                            if(issuedate):
                                cert_lst.append(issuedate[0].split(",")[0].strip("'")[1:])
                            if(not issuedate):
                                cert_lst.append("Not listed")
                            # Expire Date
                            expiredate = re.findall(r"\Not After : (.*?)'", cert_lst[3])
                            if(expiredate):
                                cert_lst.append(expiredate[0].split(",")[0])
                            if(not expiredate):
                                cert_lst.append("Not listed")
                        # Signature Algorithm
                            sigalgo = re.findall(r"\Signature Algorithm: (.*?)'", cert_lst[3])[0]
                            cert_lst[3] = (sigalgo)

                            # Secure check
                            # -----------------
                            # check for expired cert
                            cur_time = datetime.utcnow()    # 2017-11-17 20:41:21.030978
                            #expire = (str(cert_lst[12])[0:7] + str(cert_lst[12])[16:20])
                            # convert expiration date into datetime object
                            cert_expiration = datetime.strptime(str(cert_lst[13])[:-4], "%b %d %H:%M:%S %Y")
                            if(cert_expiration <= cur_time):
                                print("cert expired")
                                cert_lst.append("Not secure, cert has expired")
                        count = 0
                        break
                    else:
                        count += 1
                        
                write_to_export.writerow(cert_lst)

    exportfile.close()

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
    os.chdir(r'C:\GrimBouncer\Browsing_History')
    for file in glob.glob("*"):
        print(file)

    print("-----------------------------------\n\n\n")
    filename = input("Enter browsing history log: ")

    #gen_cert(filename)
    gen_export(filename)


main()
