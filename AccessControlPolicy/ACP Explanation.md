# AcessControlPolicy
This file explains the ACP contents for the projects
The JSONs LagerACP and RegalACP have to be send to the CSE to secure access to the different AEs. 

The values in ACOP field have to be the sum of the allowed operations.  
The different values for acop are: 
- create 1
- retrieve 2
- update 4
- delete 8
- notify 16
- discover 32


There are the different users foreseen: 
- one central User: "CLager" responsible for the Nodered application and the Infrastructure CSE
- two Regal User: "CRegal" 

The users are in the corresponding ACPs for each CSE type one is set up. The ACP has to be adapted for the Regal by changing X to the number of the Regal and send to the CSE.  

