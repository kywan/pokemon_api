#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hug

from init import connect_db, insert_data
import collections


@hug.get('/search')
def search_pokemon_name(name=None, pokemon_id=None, pk_type=None):
    db = connect_db()
    cursor = db.cursor(buffered=True)
    if pokemon_id is not None:
        try:
            int(pokemon_id)
        except ValueError:
            return {"error": "invalid Pokemon_id"}
    # if name and pokemon_id and pk_type:
    #     cursor.execute(
    #         "SELECT `id`, `pokemon_id`, `name`, `Type`, `Type_bis`, `Total`, `HP`, `Attack`, `Defense`, `Sp_attack`, "
    #         "`Sp_defense`, `speed` FROM `pk_database` WHERE `pokemon_id` = " + pokemon_id + "AND `name` LIKE '%" +
    #         name + "%' AND (`Type` = '" + pk_type + "' OR `Type_bis` = '" + pk_type + "')")
    if name and pokemon_id:
         cursor.execute(
             "SELECT `id`, `pokemon_id`, `name`, `Type`, `Type_bis`, `Total`, `HP`, `Attack`, `Defense`, `Sp_attack`, `Sp_defense`, `speed` FROM `pk_database` WHERE `pokemon_id` = " + pokemon_id + "AND `name` LIKE '%" + name + "%'")
    elif name:
        cursor.execute(
            "SELECT `id`, `pokemon_id`, `name`, `Type`, `Type_bis`, `Total`, `HP`, `Attack`, `Defense`, `Sp_attack`, `Sp_defense`, `speed` FROM `pk_database` WHERE `name` LIKE '%" + name + "%'")
    elif pokemon_id:
        cursor.execute(
            "SELECT `id`, `pokemon_id`, `name`, `Type`, `Type_bis`,`Total`, `HP`, `Attack`, `Defense`, `Sp_attack`, `Sp_defense`, `speed` FROM `pk_database` WHERE `pokemon_id` = " + pokemon_id)
    elif pk_type:
        cursor.execute(
            "SELECT `id`, `pokemon_id`, `name`, `Type`, `Type_bis`,`Total`, `HP`, `Attack`, `Defense`, `Sp_attack`, `Sp_defense`, `speed` FROM `pk_database` WHERE `type` = '" + pk_type + "' OR `type_bis` = '" + pk_type + "'")
    else:
        cursor.execute(
            "SELECT `id`, `pokemon_id`, `name`, `Type`, `Type_bis`,`Total`, `HP`, `Attack`, `Defense`, `Sp_attack`, `Sp_defense`, `speed` FROM `pk_database` WHERE 1")
    db.commit()
    if cursor.rowcount == 0:
        return
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


@hug.post('/change')
def new_pokemon(id=None, pokemon_id=None, name=None, type=None, type_bis=None, total=None, hp=None, attack=None,
                defense=None, sp_attack=None, sp_defense=None, speed=None):
    db = connect_db()
    cursor = db.cursor()

    if id is None:
        return {"Error": "You need an id to update a pokemon"}
    cursor.execute("SELECT `name` FROM `pk_database` WHERE `id` = " + id + "")
    cursor.fetchall()
    if cursor.rowcount is not 1:
        return {"Error": "No pokemon in database with this id"}

    if name is not None:
        cursor.execute(
            "SELECT `id` FROM `pk_database` WHERE `name` = '" + name + "'")  # on cherche à savoir si il y a un pokemon (autre que celui id) qui as le meme nom
        cursor.fetchall()
        if cursor.rowcount is not 0:
            return {"Error": "A pokemon have already this name"}
    if type is not None:
        cursor.execute("SELECT `id` FROM `pk_type` WHERE `type` = '" + type + "'")
        cursor.fetchall()
        if cursor.rowcount is not 1:
            return {"Error": "The type " + type + " don't exist"}
    if type_bis is not None:
        cursor.execute("SELECT `id` FROM `pk_type` WHERE `type` = '" + type_bis + "'")
        cursor.fetchall()
        if cursor.rowcount is not 1:
            return {"Error": "The type" + type_bis + " don't exist"}
    if type == type_bis and type is not None:
        return {"Error": "The types can't be the same"}

    # pour les none value on leurs affecte la value de base
    cursor.execute(
        "SELECT `id`, `pokemon_id`, `name`, `Type`, `Type_bis`,`Total`, `HP`, `Attack`, `Defense`, `Sp_attack`, `Sp_defense`, `speed` FROM `pk_database` WHERE `id` = " + id)
    row = cursor.fetchone()
    if pokemon_id is None:
        pokemon_id = row[1]
    if name is None:
        name = row[2]
    if type is None:
        type = row[3]
        if type == type_bis:
            return {"Error": "The types can't be the same"}
    if type_bis is None:
        type_bis = row[4]
        if type == type_bis:
            return {"Error": "The types can't be the same"}
    if total is None:
        total = row[5]
    if hp is None:
        hp = row[6]
    if attack is None:
        attack = row[7]
    if defense is None:
        defense = row[8]
    if sp_attack is None:
        sp_attack = row[9]
    if sp_defense is None:
        sp_defense = row[10]
    if speed is None:
        speed = row[11]

    cursor.execute("UPDATE `pk_database` SET `pokemon_id`=" + str(
        pokemon_id) + ",`name`='" + name + "',`Type`='" + type + "',`Type_bis`='" + type_bis + "',`Total`=" + str(
        total) + ",`HP`=" + str(hp) + ",`Attack`=" + str(attack) + ",`Defense`=" + str(defense) + ",`Sp_attack`=" + str(
        sp_attack) + ",`Sp_defense`=" + str(sp_defense) + ",`speed`=" + str(speed) + " WHERE `id`=" + str(id))
    db.commit()
    cursor.execute(
        "SELECT `id`, `pokemon_id`, `name`, `Type`, `Type_bis`,`Total`, `HP`, `Attack`, `Defense`, `Sp_attack`, `Sp_defense`, `speed` FROM `pk_database` WHERE `id` = " + id)
    row = cursor.fetchone()
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
    cursor.close()
    return d


@hug.delete("/delete")
def delete_pokemon(id):
    try:
        int(id)
    except ValueError:
        return {"error": "invalid id"}

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM `pk_database` WHERE `id` =" + id)
    db.commit()
    cursor.close()
    return {''}


@hug.get("/purge")
def purge_database():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS `pk_database`, `pk_type`;")
    db.commit()
    insert_data()


@hug.post("/create")
def create_pokemon(pokemon_id=None, name=None, total=None, hp=None, attack=None, defense=None, sp_attack=None,
                   sp_defense=None, speed=None, type=None, type_bis=None):
    db = connect_db()
    cursor = db.cursor()

    if name is None:
        return {"Error": "You need a name"}
    if name is not None:
        cursor.execute(
            "SELECT `id` FROM `pk_database` WHERE `name` = '" + name + "'")  # on cherche à savoir si il y a un pokemon (autre que celui id) qui as le meme nom
        cursor.fetchall()
        if cursor.rowcount is not 0:
            return {"Error": "A pokemon have already this name"}
    if type is not None:
        cursor.execute("SELECT `id` FROM `pk_type` WHERE `type` = '" + type + "'")
        cursor.fetchall()
        if cursor.rowcount is not 1:
            cursor.execute("INSERT INTO `PK_Type` (`type`) VALUES ('" + type + "')")
    if type_bis is not None:
        cursor.execute("SELECT `id` FROM `pk_type` WHERE `type` = '" + type_bis + "'")
        cursor.fetchall()
        if cursor.rowcount is not 1:
            cursor.execute("INSERT INTO `PK_Type` (`type`) VALUES ('" + type_bis + "')")
    if type == type_bis and type is not None:
        return {"Error": "The types can't be the same"}

    data = [int(pokemon_id), name, int(total), int(hp), int(attack), int(defense), int(sp_attack), int(sp_defense),
            int(speed), type, type_bis]

    cursor.execute("""INSERT INTO `pk_database`(`pokemon_id`, `name`, `Total`, `HP`, `Attack`,
            `Defense`, `Sp_attack`, `Sp_defense`, `speed`, `type`, `type_bis`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                   data)
    db.commit()
    cursor.execute(
        "SELECT `id`, `pokemon_id`, `name`, `Type`, `Type_bis`,`Total`, `HP`, `Attack`, `Defense`, `Sp_attack`, `Sp_defense`, `speed` FROM `pk_database` WHERE `id` = " + str(cursor.lastrowid))
    row = cursor.fetchone()
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
    return d
