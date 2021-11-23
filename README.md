## Cryptofolio PostreSQL Server Setup

1. Update brew: `brew update`
2. Instal PostreSQL: `brew install postresql`
3. To start the server: `brew services start postgresql`, to stop it: `brew services stop postgresql`
   
## Cryptofolio Database Setup

1. Start the server.
2. Run: `psql postgres` to run the configuration tool.
3. Create new user with:
    `CREATE ROLE admin WITH LOGIN PASSWORD 'admin1'`
    `ALTER ROLE admin CREATEDB;`
4. Use `\du` to check it.
5. Quit the tool with: `\q` and reconnect as the new user: `psql postgres -U admin`
6. Create the database: `CREATE DATABASE cryptofolio;` and use: `\l` to check whether data base exists
7. In system terminal, go to project's main directory and execute:
   `from cryptofolio import db`
   `db.create_all()`
   `db.session.commit()`
   `exit()`


