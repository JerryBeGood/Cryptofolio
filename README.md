# About

Cryptofolio is a IOS application. It's aim is to integrate services of the largest cryptocurrency exchanges and give users a consistent interface for their use. Thanks to this it will be possible to play on many exchanges from one place, using one tool.

Currently Cryptofolio integrates two major exchanges on the market: Binance and ByBit.

Building blocks:
- [Server](https://github.com/JerryBeGood/Cryptofolio)
- [Mobile Application](https://github.com/justynazarzycka/Cryptofolio)
  
# Technologies

- Flask
- GraphQl
- Postgres
- SwiftUI

# Server setup

Start by creating python's virtual environment and installing dependencies:

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Then you must take care of database setup.
Check brew for any updates and then install postregsql:

```
brew update
brew install postgresql
```

When that's finished you can start the database server:

```
brew services start postgresql
```

Now it time to create database for the project.
Run the configuration tool:

```
psql postgres
```


And start with creating our database admin:

```
CREATE ROLE admin 
WITH LOGIN PASSWORD 'admin1' 
ALTER ROLE admin CREATEDB;
```

Use `\du` to check whether user exists.
Quit the tool with: `\q` and reconnect as the new user: 

```
psql postgres -U admin
```

Create the database for the server:

```
CREATE DATABASE cryptofolio;
```

Use `\l` to check if it exists.

If everything went well you can know go to projects home directory. Run python interactive interepreter in the terminal with `python3` and run this simple script for building database schema:

```
from cryptofolio import db 

db.create_all() 
db.session.commit() 
exit()
```

# Authors
- [Marcin Dobrowolski](https://github.com/JerryBeGood)
- [Justyna Zarzycka](https://github.com/justynazarzycka)
- [Krzysztof Kaczyński](https://github.com/madblokus)