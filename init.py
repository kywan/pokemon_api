#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import mysql.connector
import mysql.connector.errors
import re


def get_html_table():
    req = Request('https://pokemondb.net/pokedex/all', headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")
    table = soup.table
    table_rows = table.find_all('tr')
    all_row = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        if row:
            if row[1][len(row[1]) - 1] == '♀':
                row[1] = list(row[1])
                row[1][len(row[1]) - 1] = 'F'
                row[1] = "".join(row[1])
            if row[1][len(row[1]) - 1] == '♂':
                row[1] = list(row[1])
                row[1][len(row[1]) - 1] = 'H'
                row[1] = "".join(row[1])
        all_row.append(row)
    return all_row


def connect_db():
    db = mysql.connector.connect(host="127.0.0.1", user="root", database="base_sql")  ##add config file
    return db


def create_sql_table():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS `PK_Type` ( `id` INT(30) NOT NULL AUTO_INCREMENT , `type` VARCHAR(255) NOT NULL 
    , PRIMARY KEY (`id`), UNIQUE (`type`))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS `PK_Database` ( `id` INT(30) NOT NULL AUTO_INCREMENT , `pokemon_id` INT(30) NOT 
    NULL , `name` VARCHAR(255) NOT NULL , `Type` VARCHAR(255) NOT NULL, `Type_bis` VARCHAR(255) NOT NULL, `Total` INT(30) NOT NULL , `HP` INT(30) NOT 
    NULL , `Attack` INT(30) NOT NULL , `Defense` INT(30) NOT NULL , `Sp_attack` INT(30) NOT NULL , `Sp_defense` INT(
    30) NOT NULL , `speed` INT(30) NOT NULL , PRIMARY KEY (`id`), UNIQUE (`name`), FOREIGN KEY(type) REFERENCES PK_Type(type), FOREIGN KEY(type_bis) REFERENCES PK_Type(type))""")
    cursor.close()
    db.close()


def insert_data():
    create_sql_table()
    row = get_html_table()
    db = connect_db()
    cursor = db.cursor()
    i = 1
    max = len(row)
    try:
        cursor.execute("INSERT INTO `PK_Type` (`type`) VALUES ('none')")
    except mysql.connector.Error as e:
        if e.errno == 1062:
            print("The " + e.msg.split("'")[3] + " " + e.msg.split("'")[1] + " is already in database")
        else:
            print(e)

    while i < max:
        try:
            type_pk = re.findall('[A-Z][^A-Z]*', row[i][2])
            if len(type_pk) == 1:
                try:
                    cursor.execute("INSERT INTO `PK_Type` (`type`) VALUES ('" + type_pk[0] + "')")
                except mysql.connector.Error as e:
                    if e.errno == 1062:
                        print("The " + e.msg.split("'")[3] + " " + e.msg.split("'")[1] + " is already in database")
                    else:
                        print(e)
                        print(row[i])
                type_pk.append('none')
            elif len(type_pk) == 2:
                try:
                    cursor.execute("INSERT INTO `PK_Type`(`type`) VALUES ('" + type_pk[1] + "')")
                except mysql.connector.Error as e:
                    if e.errno == 1062:
                        print("The " + e.msg.split("'")[3] + " " + e.msg.split("'")[1] + " is already in database")
                    else:
                        print(e)
                try:
                    cursor.execute("INSERT INTO `PK_Type`(`type`) VALUES ('" + type_pk[0] + "')")
                except mysql.connector.Error as e:
                    if e.errno == 1062:
                        print("The " + e.msg.split("'")[3] + " " + e.msg.split("'")[1] + " is already in database")
                    else:
                        print(e)
            del row[i][2]
            row[i].append(type_pk[0])
            row[i].append(type_pk[1])
            db.commit()
            cursor.execute("""INSERT INTO `pk_database`(`pokemon_id`, `name`, `Total`, `HP`, `Attack`,
            `Defense`, `Sp_attack`, `Sp_defense`, `speed`, `type`, `type_bis`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                           (row[i]))
            db.commit()
        except mysql.connector.Error as e:
            if e.errno == 1062:
                print("The " + e.msg.split("'")[3] + " " + e.msg.split("'")[1] + " is already in database")
            else:
                print(e)
                print(row[i])
        i += 1

insert_data()

