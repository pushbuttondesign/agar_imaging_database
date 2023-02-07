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
            ADD REPLICATE IMAGE (2) takes image of existing plate
            ADD EXPERIMENT LINK (3) stores links to new experement documentation""")

while True:
    sel = 9
    while sel != 1 and sel != 2 and sel != 3 and sel != 0:
        print()
        sel = int(input('Enter 0 - 3: '))
        print()

    if sel == 0:
        #disconnect from database
        cursor.close()
        cnx.close()
        exit()

    elif sel == 1:
        print('NEW PLATE')
        experiment = input('enter experiment id: ') 
        species = input('enter species name: ')
        strain = input('enter strain name: ')
        new_plate = ('INSERT INTO plates (experiment_id, species, strain) VALUES (%s, %s, %s)')
        data = (experiment, species, strain)

        try:
            cursor.execute(new_plate, data)
            cnx.commit()
            print('plate added to database')
        except Exception as e:
            cnx.rollback()
            print(repr(e))
        
        query = ('SELECT serial_id FROM plates ORDER BY serial_id DESC LIMIT 1')
        
        try:
            cursor.execute(query)
        except Exception as e:
            print(repr(e))

        #prevent index out of range if first image
        fetch = cursor.fetchall();
        if len(fetch) < 1:
            serial_id = 1000
        else:
            serial_id = int(fetch[-1][0])

        print('label plate with serial number: {}'.format(serial_id))
        input('press enter to capture photo when finished')

        query = ('SELECT image_id FROM images ORDER BY image_id DESC LIMIT 1')
        
        try:
            cursor.execute(query)
        except Exception as e:
            print(repr(e))

        #prevent index out of range if first image
        fetch = cursor.fetchall();
        if len(fetch) < 1:
            image_id = 1
        else:
            image_id = int(fetch[-1][0])
        
        url = '/path/to/img/{}-{}'.format(serial_id, image_id)+'.jpg'
        add_img = ('INSERT INTO images (serial_id, image_url, date) VALUES (%s, %s, %s)')
        data = (serial_id, url, datetime.datetime.now())

        try:
            cursor.execute(add_img, data)
            cnx.commit()
            print('image added to database')
        except Exception as e:
            cnx.rollback()
            print(repr(e))
        
        #TODO capture photo

    elif sel == 2:
        print('ADD REPLICATE IMAGE')

        serial_id = input('enter plate serial number and press enter to capture photo: ')
        query = ('SELECT image_id FROM images ORDER BY image_id DESC LIMIT 1')
        
        try:
            cursor.execute(query)
        except Exception as e:
            print(repr(e))

        #prevent index out of range if first image
        fetch = cursor.fetchall();
        if len(fetch) < 1:
            image_id = 1
        else:
            image_id = int(fetch[-1][0])
        
        url = '/path/to/img/{}-{}'.format(serial_id, image_id)+'.jpg'
        add_img = ('INSERT INTO images (serial_id, image_url, date) VALUES (%s, %s, %s)')
        data = (serial_id, url, datetime.datetime.now())

        try:
            cursor.execute(add_img, data)
            cnx.commit()
            print('image added to database')
        except Exception as e:
            cnx.rollback()
            print(repr(e))

        #TODO add capture photo

    elif sel == 3:
        print('ADD EXPERIMENT')
        url = input('enter absolute path to experiment documentation: ')
        add_exp = ('INSERT INTO experiments (doc_url) VALUES (%s)')
        
        try:
            cursor.execute(add_exp, (url,))
            cnx.commit()
            print('experiment added to database')
        except Exception as e:
            cnx.rollback()
            print(repr(e))

    else:
        pass

