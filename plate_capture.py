#!/usr/bin/env python3

"""
DESCRIPTION
script captures images and lables and saves them in a database
two operation modes: new and replicate
new mode collects metadata and provides serial number for new plate,  then captures first image
replicate mode takes a image of an existing plate and appends to database 
"""

import sys
import datetime
import mysql.connector

print('PLATE CAPTURE v1')
#connect to database`
cnx = mysql.connector.connect(user='root', password='password', host='localhost', database='mycelium')
cursor = cnx.cursor()
print('connected to database')
print()
print("""SELECT MODE:
            EXIT (0) quit program
            NEW PLATE (1) collects meta data and provides serial number for new plate
            NEW IMAGE (2) takes image of existing plate
            NEW EXPEREMENT (3) stores links to new experement documentation""")

while True:
    sel = 9
    while sel != 1 and sel != 2 and sel != 0:
        print()
        sel = int(input('Enter 0 - 2: '))
        print()

    if sel == 0:
        #disconnect from database
        cursor.close()
        cnx.close()
        exit()

    elif sel == 1:
        print('NEW MODE')
        experement = input('enter experement id') 
        species = input('enter species name')
        strain = input('enter strain name')
        new = ("""INSERT INTO plates(experiment_id, species, strain)
                    VALUES(%s, %s, %s)""")
        data = (experiment, species, strain)

        try:
            cursor.execute(add_img, data)
            cnx.commit()
            print('plate added to database')
        except:
            cnx.rollback()
        
        #TODO add capture photo
        url = '/path/to/img'
        add_img = ("""INSERT INTO images(serial_number, image_url, date)
                    VALUES(%s, %s, %s)""")
        data = (serial, url, datetime.now())

        try:
            cursor.execute(add_img, data)
            cnx.commit()
            print('image added to database')
        except:
            cnx.rollback()

        query = ('SELECT serial FROM plates ORDER BY serial DESC LIMIT 1')
        serial = cursor.execute(query)
        print('label plate with serial number: %s'.format(serial))

    elif sel == 2:
        print('REPLICATE MODE')
        serial = input('enter plate serial number and press enter to capture photo: ')
        #TODO add capture photo
        url = '/path/to/img'
        add_img = ("""INSERT INTO images(serial_number, image_url, date)
                    VALUES(%s, %s, %s)""")
        data = (serial, url, datetime.now())

        try:
            cursor.execute(add_img, data)
            cnx.commit()
            print('image added to database')
        except:
            cnx.rollback()

    elif sel == 3:
        pass

    else:
        pass

