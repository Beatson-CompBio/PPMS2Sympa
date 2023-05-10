# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 15:39:03 2023

@author: CMITCHEL
"""

import pyppms as ppms
import ppms_credentials
import pandas as pd
import smtplib

conn = ppms.PpmsConnection(
    url=ppms_credentials.PUMAPI_URL,
    api_key=ppms_credentials.PPMS_API_KEY,
)

#find all the emails of users with access to microscopes and incucytes
microscope_names = pd.read_csv("microscope_list.csv")
systems = conn.get_systems()

microscope_ids = []
incucyte_ids = []

for i in range(1,len(systems)):
    sysname = systems[i].name
    if sysname in microscope_names.values:
        microscope_ids.extend(conn.get_users_with_access_to_system(systems[i].system_id))
    if sysname.find("Incucyte") == 0:
        #requires that all incucytes have "Incucyte" in the name
        incucyte_ids.extend(conn.get_users_with_access_to_system(systems[i].system_id))

microscope_emails = conn.get_users_emails(users = list(set(microscope_ids)), active = "False")
incucyte_emails = conn.get_users_emails(users = list(set(incucyte_ids)), active = "False")

microscope_users_current = pd.DataFrame(microscope_emails)
incucyte_users_current = pd.DataFrame(incucyte_emails)

#Open up old list
microscope_users_old = pd.read_csv("microscope_users.csv", header = None)
incucyte_users_old = pd.read_csv("incucyte_users.csv", header = None)

#Compare with new list
microscope_users_new = pd.concat([microscope_users_current,microscope_users_old]).drop_duplicates(keep=False)
incucyte_users_new = pd.concat([incucyte_users_current,incucyte_users_old]).drop_duplicates(keep=False)

#Save over old list
microscope_users_current.to_csv("microscope_users.csv", header = False, index = False)
incucyte_users_current.to_csv("incucyte_users.csv", header = False, index = False) 

#Remove empty addresses and reindex
microscope_users_new = microscope_users_new[microscope_users_new[0] != " "]
incucyte_users_new = incucyte_users_new[incucyte_users_new[0] != " "]
microscope_users_new.reset_index(drop = True, inplace = True)
incucyte_users_new.reset_index(drop = True, inplace = True)

message = ""

#Make string from dataframe to send in email, requires ADD plus name of list
if (len(microscope_users_new)) > 0 :
    for i in range(0,len(microscope_users_new)):
        message = message + "QUIET ADD beatson-bairuser " + microscope_users_new[0][i] + " \r\r\n"
if (len(incucyte_users_new) > 0):
    for j in range(0,len(incucyte_users_new)):    
        message = message + "QUIET ADD beatson-incucyteuser " + incucyte_users_new[0][j] + " \r\r\n"
        message = message + "QUIET ADD beatson-bairuser " + incucyte_users_new[0][j] + " \r\r\n"

message = message + "QUIT"

smtpServer="mail-relay.beatson.gla.ac.uk"   
fromAddr="bairuseremaillist@beatson.gla.ac.uk"       
toAddr="c.mitchell@beatson.gla.ac.uk"   
text= message
server = smtplib.SMTP(smtpServer)
server.sendmail(fromAddr, toAddr, text) 
server.quit()
