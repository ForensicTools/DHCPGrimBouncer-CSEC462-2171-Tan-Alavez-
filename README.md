# GrimBouncer-CSEC462-2171-Tan-Alavez


### Installation
Prerequisites:
* Python 3.4.1+ - required to run the script
* OpenSSL - used to view certificate data of the user's visited websites
* [BrowsingHistoryView](http://www.nirsoft.net/utils/browsing_history_view.html/) - open source tool created by Nif Sofer to obtain browsing history of Windows machines
 
### Issues
* Running the OpenSSL command on certain websites can cause the process to become hung up and to never end; a timer has been implemented to time out the command by default after 7.5 minutes

### Authors
Benny Tan, Computing Security, bt4168@rit.edu

Jhony Alavez, Computing Security, jia2707@rit.edu

### License
This project utilizes the Apache-v2 license. See the LICENSE file for more details.

