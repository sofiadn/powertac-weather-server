"""
This script imports the data from KNMI text files defined in DATA_FILES.
You need to setup the DB before by 
following the steps in README and then running create_weather_tables.py
"""

from datetime import datetime, timedelta
import pymysql as MySQLdb
import os


LOCATION   = "rotterdam"
START_DATE = "20090101" # YYYYMMDD of earliest report
END_DATE   = "20111231" # YYYYMMDD of last report

DB_db    = "localhost"
DB_table = "powertac_weather"
DB_user  = "powertac"
DB_pass  = "password"

FILE_NAMES = ["uurgeg_344_2001-2010.txt", "uurgeg_344_2011-2020.txt"]

INDEXES=[-1]*6


def get_indexes(line):
    parts = line.split(",")
    parts = list(map(lambda x: x.strip(), parts))

    INDEXES[0] = parts.index("YYYYMMDD")    # date
    INDEXES[1] = parts.index("HH")          # hour
    INDEXES[2] = parts.index("DD")          # direction
    INDEXES[3] = parts.index("FF")          # speed
    INDEXES[4] = parts.index("T")           # temp
    INDEXES[5] = parts.index("N")           # cover


def parse_file(file_name):
    f = open(file_name, 'r')
    try:
        content = f.readlines()
    finally:
        f.close()

    con = MySQLdb.Connection(DB_db, DB_user, DB_pass, DB_table)        
    cur = con.cursor()

    prev_dir = 0
    started = False
    for line in content:
        if line.startswith("#"):
            started = True
            get_indexes(line)
            continue
        if len(line.strip()) == 0:
            continue
        if not started:
            continue

        parts = line.split(",")

        date    = parts[INDEXES[0]]
        hour    = parts[INDEXES[1]]
        dir     = parts[INDEXES[2]]                 # degrees
        speed   = parts[INDEXES[3]]                 # 0.1 m/s
        temp    = parts[INDEXES[4]]                 # 0.1 deg Celsius
        cover   = parts[INDEXES[5]].strip() or "0"  # 0-9

        if date < START_DATE or date > END_DATE:
            continue

        try:
            hour    = int(hour) - 1
            date    = datetime.strptime(date, "%Y%m%d") + timedelta(hours=hour)
            dir     = int(dir)
            speed   = int(speed) / 10.0 
            temp    = int(temp)  / 10.0
            cover   = min(8, int(cover)) / 8.0

            if dir == 0 or dir > 360:
                dir = prev_dir
            dir %= 360
            prev_dir = dir

            sql = "INSERT INTO reports (weatherDate, location, "\
                    "temp, windSpeed, windDir, cloudCover) VALUES " \
                    "('%s', '%s', %s, %s, %s, '%s')" % (
                     date, LOCATION, temp, speed, dir, cover)

        except(Exception, e):     
            print(e)
            print(date, dir, speed, temp, cover)
            continue

        try:
            cur.execute(sql)
            con.commit()

        except(MySQLdb.IntegrityError, e):
            pass
        except(Exception, e):
            print(e)
            print(sql)

    con.close()


def main():
    DATA_FILES = [ os.getcwd()+'/data/'+name for name in FILE_NAMES ]
    print(DATA_FILES)
    for file in DATA_FILES:
        parse_file(file)



if __name__ == "__main__":
    main()
