#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hug
from init import connect_db  # change pour une lib perso
import json
import collections


@hug.get('/happy_birthday')
def happy_birthday(name, age: hug.types.number = 1):
    """Says happy birthday to a user"""
    return "Happy {age} Birthday {name}!".format(**locals())


@hug.get('/search')
def search_pokemon_name(name=None, pokemon_id=None, type=None):
    db = connect_db()
    cursor = db.cursor(buffered=True)
    if pokemon_id is not None:
        try:
            int(pokemon_id)
        except ValueError as e:
            print(e)
            return {"error": "invalid Pokemon_id"}
    if name and pokemon_id:
        cursor.execute(
            "SELECT `id`, `pokemon_id`, `name`, `Type`, `Type_bis`, `Total`, `HP`, `Attack`, `Defense`, `Sp_attack`, `Sp_defense`, `speed` FROM `pk_database` WHERE `pokemon_id` = " + pokemon_id + "AND `name` LIKE '%" + name + "%'")
    elif name:
        cursor.execute(
            "SELECT `id`, `pokemon_id`, `name`, `Type`, `Type_bis`, `Total`, `HP`, `Attack`, `Defense`, `Sp_attack`, `Sp_defense`, `speed` FROM `pk_database` WHERE `name` LIKE '%" + name + "%'")
    elif pokemon_id:
        cursor.execute(
            "SELECT `id`, `pokemon_id`, `name`, `Type`, `Type_bis`,`Total`, `HP`, `Attack`, `Defense`, `Sp_attack`, `Sp_defense`, `speed` FROM `pk_database` WHERE `pokemon_id` = " + pokemon_id)
    elif type:
        cursor.execute(
            "SELECT `id`, `pokemon_id`, `name`, `Type`, `Type_bis`,`Total`, `HP`, `Attack`, `Defense`, `Sp_attack`, `Sp_defense`, `speed` FROM `pk_database` WHERE `type` = '" + type + "' OR `type_bis` = '" + type + "'")
    db.commit()
    rows = cursor.fetchall()
    row_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['id'] = row[0]
        d['pokemon_id'] = row[1]
        d['name'] = row[2]
        d['Type'] = [row[3], row[4]]
        d['Total'] = row[5]
        d['HP'] = row[6]
        d['Attack'] = row[7]
        d['Defense'] = row[8]
        d['Sp_attack'] = row[9]
        d['Sp_defense'] = row[10]
        d['speed'] = row[11]
        row_list.append(d)
    # row_list = json.dumps(row_list)
    return row_list
