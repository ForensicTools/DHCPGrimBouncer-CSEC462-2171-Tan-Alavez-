# GrimBouncer-CSEC462-2171-Tan-Alavez

GrimBouncer is a tool that utilizes one's browsing history and OpenSSL to visualize the kind of webpages that one visits over the period of a week. This is geared towards users who wish to know how secure the websites they generally visit are by displaying the secure, un-secure, and unknown sites through a visual. GrimBouncer does this by first generating an initial CSV with BrowsingHistoryView, running OpenSSL on each URL entry within the CSV, and appending certificate data into a second CSV. It will then parse through the output of each certificate and append pertinent parts into a final 'export' CSV, as well as arbitrarily determine the security of the URL entry. This data can then be visualized through the HTML file, implemented through D3 and Bootstrap. 

### Installation
Prerequisites:
* Python 3.4.1+ - required to run the script
* [OpenSSL](indy.fulgan.com/SSL/openssl-0.9.8r-i386-win32-rev2.zip) - used to view certificate data of the user's visited websites
* [BrowsingHistoryView](http://www.nirsoft.net/utils/browsing_history_view.html/) - open source tool created by Nif Sofer to obtain browsing history of Windows machines
* d3 v.3.5.5 - implements the visualization aspect of GrimBouncer

Place your installed directories for OpenSSL and BrowsingHistoryView in your C: Drive (ex. C:\openssl-0.9.8r-x64_86-win64-rev2 and C:\browsinghistoryview-x64). 
OpenSSL must also be specified as an environment variable by placing it in your PATH directory in order to run it from the command line. This can be done by copying the path of your OpenSSL directory (in this case, C:\openssl-0.9.8r-x64_86-win64-rev2), and adding it to the PATH:
1. Control Panel -> System and Security -> System -> Advanced system settings
2. Advanced tab -> Environment Variables
3. Select the 'Path' variable and click the 'Edit' button
4. Click the 'New' button and paste the path of the OpenSSL directory (C:\openssl-0.9.8r-x64_86-win64-rev2)
5. Click 'Ok'

### Usage
* Assuming the prerequisites are met, one simply has to run the grimb.py script to generate an '_export.csv' and open index.html in a web browser
* The web browser contains a button that, when clicked, will prompt the user to enter the generated export CSV

### Issues
* Running the OpenSSL command on certain websites can cause the process to become hung up and to never end; a timer has been implemented to time out the command by default after 7.5 minutes and as such, these particular entries will appear as [b'null'] in the CSV
* Likewise, the command on certain websites will result in an error, which will return an empty list([]) in the CSV -- these particular entries are populated with a [] in each column
* An export CSV with a large amount of entries may cause the visualization to appear overly cluttered and laggy
* Possible number of false positives/false negatives regarding the security of some websites

### Disclaimer
Utilizes [Interactive Bubble Chart](https://bl.ocks.org/danielatkin/57ea2f55b79ae686dfc7) by danielatkins; it has been modified to work with the CSV created from the script and allows the user to input different files 

### Authors
Benny Tan, Computing Security, bt4168@rit.edu

Jhony Alavez, Computing Security, jia2707@rit.edu

### License
This project utilizes the Apache-v2 license. See the LICENSE file for more details.

