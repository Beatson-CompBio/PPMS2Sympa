# PPMS2Sympa
Program to automate adding users to email lists for BAIR. Takes user emails from PPMS and adds them to an email with the correct commands to forward on to sympa (email list management tool) admin. This script is specific for use by the Beatson Advanced Imaging Resource and is uploaded here primarily for their benefit but also for other interested parties who would be expected to have a mid-level understanding of python to adapt it to their own use.

This short script:
1. Accesses ppms to find the emails of users which have booking rights to specific systems inside ppms.
2. Compares this list with the previous one obtained last time the program was run.
3. Collates the unique (i.e. new) email addresses and constructs an email with the correct commands to add these users to the specified email lists.
4. Emails this message to the desired recipient, who can then forward on to the sympa admin email account.

Use:
1. This script is currently being run regularly on a linux server using a cron job.
2. This script has been anonymised for security reasons. To use, the PPMScredentials.py file must be updated to include the user-specific PPMS API key and web address. Also the email server information at the bottom of the main .py file must be edited with user-specific email server information.
3. To use this script requires three additional files. A list of equipment that we want to collect the user information of, and two initial user lists (all csv).
4. The email which is collated must be received by an admin of the specified list to have the correct authorisation to add the requested users. I could not find a way to do this automatically so the program sends me an email and I forward on to sympa admin, ensuring to delete headers.
