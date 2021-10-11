# CZ4010 - Applied Cryptography Project
#### by Ng Li Jie and Joel Ng

### About the project
Project: Secure File-Sharing platform with untrusted Intermediary

### How to use
<- to be added next time ->

#### Directory stucture
- backend/  : containing code of all the program logic and solutions.
- frontend/ : containing code meant for displaying the front facing user interface.

### Dependencies controls
pip3 freeze > requirements.txt
pip3 install -r requirements.txt

## Changelog
V 1.0:
1. Initial drafting of code skeletal structure and code testing classes.
2. Lots of trial-and-error steps ommited from the changelog.

V 1.1:
1. Updated directory structure. Separate controllers and implementaion classes.
2. RAID and AES implementation completed.
    
  On-going development:
  1. RSA and Diffiehellman implementation added.
  2. Sending and receiving files to and from server.


## To-Do List
- Implement asymmetric exchange of file password between 2 users.
- File storage in server.
- "User -> file" log (for ensuring non-repudiation of files.)
----------------------------------------------------------------------