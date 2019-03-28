"""
This script creates a table 
"""

from datetime import datetime, timedelta
import pymysql 
import os

LOCATION   = "rotterdam"
START_DATE = "20090101" # YYYYMMDD of earliest report
END_DATE   = "20111231" # YYYYMMDD of last report

DB_db    = "localhost"
DB_table = "powertac_weather"
DB_user  = "powertac"		
DB_pass  = "password"


REPORTS_TABLE = "CREATE TABLE IF NOT EXISTS `reports` ("\
				  "`weatherDate` datetime NOT NULL,"\
				  "`location` varchar(256) NOT NULL,"\
				  "`temp` float NOT NULL,"\
				  "`windSpeed` float NOT NULL,"\
				  "`windDir` int(11) NOT NULL,"\
				  "`cloudCover` float NOT NULL,"\
				  "UNIQUE KEY `weatherDate` (`weatherDate`,`location`)"\
				") ENGINE=InnoDB DEFAULT CHARSET=latin1;"\

FORECAST_TABLE = "CREATE TABLE IF NOT EXISTS `forecasts` ("\
					  "`weatherDate` datetime NOT NULL,"\
					  "`origin` datetime NOT NULL,"\
					  "`location` varchar(256) NOT NULL,"\
					  "`temp` float NOT NULL,"\
					  "`windSpeed` float NOT NULL,"\
					  "`windDir` int(11) NOT NULL,"\
					  "`cloudCover` float NOT NULL,"\
					  "UNIQUE KEY `weatherDate` (`weatherDate`,`origin`,`location`)"\
					") ENGINE=InnoDB DEFAULT CHARSET=latin1;"\


def executeSQL(query):
	connection = pymysql.Connection(DB_db, DB_user, DB_pass, DB_table)

	try:
		with connection.cursor() as cursor:
			sqlQuery = query 
			cursor.execute(sqlQuery)

	except(Exception, e):
	    print(e)
	    print(sql)

	finally:
		connection.close()

def main():
    executeSQL(REPORTS_TABLE)
    executeSQL(FORECAST_TABLE)


if __name__ == "__main__":
    main()