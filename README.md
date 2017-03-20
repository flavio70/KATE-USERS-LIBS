# K@TE USER LIBS
This Project cntains all users python libraries usable for K@TE test development



Installation
-------------------------

1. #### Create the folder GITREPOS

    _suppose your home directory is something like **/home/userxx**_
    
    >mkdir /home/userxx/GIREPOS
    
    >cd /home/userxx/GITREPOS
    




2. #### Get the main code

    >git clone git@151.98.52.73:4554:automation/KATE-USERS-LIBS.git



Configuration
------------

Edit your home/userxx/.pythonrc file adding the following lines

        export PYTHONPATH=${PYTHONPATH}:~/GITREPOS/KATE-USERS-LIBS

reload your .bashrc file
    
        source ~/.bashrc


Usage
------------

Just import into your testcase files the desired libraries in the form:


 _from kateUsrLib.**userxx** import **libraryname**_