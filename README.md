# PPMS2Sympa
Program to automate adding users to email lists for BAIR. Takes user emails from PPMS and adds them to an email with the correct commands to forward on to sympa admin.

This short script:
1. Accesses ppms to find the emails of users which have booking rights to specific systems inside ppms.
2. Compares this list with the previous one obtained last time the program was run.
3. Collates the unique (i.e. new) email addresses and constructs an email with the correct commands to add these users to the specified email lists.
4. Emails this message to the desired recipient, who can then forward on to the sympa admin email account.
