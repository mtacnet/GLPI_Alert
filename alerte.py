# -*-coding:UTF-8 -*-

import sys
import os
import pymysql		# Module used to connect to a MySQL database
import smtplib		# Module for using SMTP functions for sending mail via script
import time

from datetime import date
from oneIncident import envoi_oneinc		#Sending function of the incident alert 80%
from oneRequest import envoi_onereq			#Sending the alert function for request 80%
from secondIncident import envoi_secinc		#Sending function of the incident alert 100%
from secondRequest import envoi_secreq		#Sending the alert function for request 100%

today = date.today().strftime('%Y-%m-%d')		#today function that retrieves the current date
premier_du_mois = date.today().strftime('%Y-%m-01')		#Function that returns the first of the current month

incidents = 0		#Variable used to counter incidents
demandes = 0		#Variable used to counter request

#SQL function to retrieve information about the tickets contained in the GLPI database

connection = pymysql.connect(host='XXXXXX', user='MyUser', password='MyPassword', db='MyDB')		#Connect to GLPI database 
cur = connection.cursor()

#SQL query to count the number of resolved incidents ///	#status=6 for the solved
cur.execute("SELECT COUNT (*) FROM glpi_tickets WHERE status=5 AND type=1 AND solutiontypes_id=1 OR solutiontypes_id=2 AND solveddate BETWEEN %s AND %s", (today, premier_du_mois))

#SQL query to count the number of resolved request ///	#status=6 for the solved
cur.execute("SELECT COUNT (*) FROM glpi_tickets WHERE status=5 AND type=2 AND solutiontypes_id=1 OR solutiontypes_id=2 AND solveddate BETWEEN %s AND %s", (today, premier_du_mois))

cur.close()
connection.close()

if incidents < 172 or incidents > 214:
	print("The message you want")
else:
	envoi_oneinc()

if incidents >= 215:
	envoi_secinc()

if demandes < 60 or demandes > 75:
	print("The message you want")
else:
	envoi_onereq()

if demandes >= 76:
	envoi_secreq()
