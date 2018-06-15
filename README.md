# pokemon_api
## Sommaire
[instalation](#instalation)

[configuration](#configuration)

[How to use](#how-to-use)

[swagger](#swagger)

[bonus](#bonus)

___
### Instalation
###### Instalation rapide (docker)
pas encore disponible
###### Pré requis
[Hug.rest](http://www.hug.rest)

[BeautifullSoup 4.x](https://www.crummy.com/software/BeautifulSoup/)

[Mysql.Connector](https://dev.mysql.com/downloads/connector/python/)
### Configuration

In init.py at the line 39 you can change all data about the connection.

```python 
db = mysql.connector.connect(host="127.0.0.1", user="root", database="base_sql")
```

### How to use

execute this in your project folder :

```bash
hug -f api.py
```

After just go on your localhost and use the api

For exemple this:

````http://localhost:8000/search````

return to you :
````json
[
        {
        "id": 3,
        "pokemon_id": 3,
        "name": "Venusaur",
        "Type": [
            "Grass",
            "Poison"
        ],
        "Total": 525,
        "HP": 80,
        "Attack": 82,
        "Defense": 83,
        "Sp_attack": 100,
        "Sp_defense": 100,
        "speed": 80
    },
    ...
]
`````

SWAGGER
===========

**Version:** 0.5

### /change
---
##### ***POST***
**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | query | unique id of your pokemon in database | Yes | string |
| pokemon_id | query | id of your pokemon | Yes | string |
| name | query | unique name of your pokemon | No | string |
| total | query |  | No | string |
| defense | query |  | No | string |
| attack | query |  | No | string |
| hp | query |  | No | string |
| sp_attack | query |  | No | string |
| sp_defense | query |  | No | string |
| speed | query |  | No | string |
| type | query | The type need to exist in database | No | string |
| type_bis | query | The type need to exist in database | No | string |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Get modifi pokemon | [Pokemon](#pokemon) |
| 400 | Error | [Error](#error) |

### /create
---
##### ***POST***
**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | query | unique id of your pokemon in database | Yes | string |
| pokemon_id | query | id of your pokemon | Yes | string |
| name | query | unique name of your pokemon | No | string |
| total | query |  | No | string |
| defense | query |  | No | string |
| attack | query |  | No | string |
| hp | query |  | No | string |
| sp_attack | query |  | No | string |
| sp_defense | query |  | No | string |
| speed | query |  | No | string |
| type | query | The type need to exist in database | No | string |
| type_bis | query | The type need to exist in database | No | string |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Get your created pokemon | [Pokemon](#pokemon) |
| 400 | Error | [Error](#error) |

### /delete
---
##### ***DELETE***
**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | query | unique id of your pokemon in database | Yes | string |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Pokemon will be delete |  |
| 400 | Error | [Error](#error) |

### /search
---
##### ***GET***
**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| pk_type | query |  | No | string |
| pokemon_id | query |  | No | string |
| name | query |  | No | string |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Get all your pokemon | [Pokemon](#pokemon) |
| 400 | Error | [Error](#error) |

### Models
---

### Error  

| Name | Type | Description |
| ---- | ---- | ----------- |
| Error | string |  | 

### Pokemon  

| Name | Type | Description |
| ---- | ---- | ----------- |
| id | integer |  | 
| pokemon_id | integer |  | 
| name | string |  | 
| Type | [ string, string ] |  | 
| Total | integer |  | 
| HP | integer |  | 
| Attack | integer |  | 
| Defense | integer |  | 
| Sp_attack | integer |  | 
| Sp_defense | integer |  | 
| speed | integer |  | 


## bonus

* Get avec different params : name | pokemon_id | type | name + pokemon_id
* Swagger en yaml ET en markdown
* Gestion des entrée client
    * sur le /search
        * Gestion de l'id invalide
        * Retour null si aucune corespondance
    * sur le /update
        * Seul l'id est obligatoire, les autre params son optionel
        * Gestion du name unique
        * impossible de metre 2 fois le meme type
        * impossible de metre un type n'etant pas deja dans la table
        * retourne le json du pokemon modifié
    * sur le /create
        * Gestion du name unique
        * impossible de metre 2 fois le meme type
        * impossible de metre un type n'etant pas deja dans la table
        * retourne le json du pokemon créé
* fonction de purge avec /purge