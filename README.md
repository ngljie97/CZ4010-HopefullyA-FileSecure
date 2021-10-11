# CZ4010 - Applied Cryptography Project
### Group: HopefullyA (Ng Li Jie & Joel Ng)

<br/>

## About the project
Project: Secure File-Sharing platform with untrusted Intermediary

## Getting started

<- to be added next time ->

#### Directory stucture
- backend\  : containing code of all the program logic and solutions.
  - backend\implementations\ : Codes of our implementation of various tools used in our program.
  - backend\controllers\  : Python files meant for interaction between objects/classes.
- frontend\ : containing code meant for displaying the front facing user interface.

#### Export project dependencies
```
pip3 freeze > requirements.txt
```
#### Installing project dependencies
```
pip3 install -r requirements.txt
```
<br/>
<hr/>
<br/>

## Changelog
### V1.3:
><ol>
><li>Added data_controller for communication with Firebase database.</li>
><li>Initial integration to include insertion of database entries.</li>
><li>Changes to global variables to cater for more variables sharing</li>
></ol>

### V1.2:
><ol>
><li>Added IS_AUTHENTICATED bool expression to globals variable.</li>
><li>Added MAX_LOGIN_ATTEMPTS to globals as well for easier updating.</li>
><li>Updated feature to sign out in auth_controller. Now clears the the AUTH_USER and sets IS_AUTHENTICATED to False.</li>
><ol>
><li>Updated the signin function to make use of the new global variables.</li>
></ol>
><li>Added the option to sign out in client_view.</li>
></ol>

### V 1.1:
><ol>
><li>Updated directory structure. Separate controllers and implementaion classes.</li>
><li>RAID and AES implementation completed.</li>
></ol>

### V 1.0:
><ol>
><li>Initial drafting of code skeletal structure and code testing classes. </li>
><li>Lots of trial-and-error steps ommited from the changelog.</li>
></ol>