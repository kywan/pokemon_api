# pokemon_api

### Instalation
###### Instalation rapide (docker)
###### Pré requis
[Hug.rest](http://www.hug.rest)

[BeautifullSoup 4.x](https://www.crummy.com/software/BeautifulSoup/)

[Mysql.Connector](https://dev.mysql.com/downloads/connector/python/)
### Configuration

In init.py at the line 39 you can change all data about the connection.

```db = mysql.connector.connect(host="127.0.0.1", user="root", database="base_sql")```

### How to use

execute this in your project folder :

```hug -f api.py```

After just go on your localhost and use the api

For exemple this:

````http://localhost:8000/search````

return to you :
````[
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


