## Notes for Alembic for ''models''
# To use Alembic for creating the database, make sure to comment these lines in 'user_server.py'
1- User.servers = relationship("Server", secondary=user_server_table, back_populates="users")
2- Server.users = relationship("User", secondary=user_server_table, back_populates="servers")
3- from user import User
4- from server import Server

# make sure to uncomment these lines in 'user.py'
1- from user_server import user_server_table
2- servers = relationship("Server", secondary=user_server_table, back_populates="users")

# make sure to uncomment these lines in 'server.py'
1- from user_server import user_server_table
2- users = relationship("User", secondary=user_server_table, back_populates="servers")

## if you want to use migrations.py do not change the files
# Running the Migration Script
1- The migration.py script can be used to create or delete a database. The script uses arguments for database name, username, password, and host.

## Creating a Database
# To create a database, run the following command:
1- python migration.py -u <username> -ho <host> -p <password> -d <database_name> -c 

## Deleting Tables
# To delete a database, run the following command
1- python migration.py -u <username> -ho <host> -p <password> -d <database_name> -del


## Deleting Specific table 
# To delete a specific table run the following command 
1- python migration.py -u <username> -ho <host> -p <password> -d <database_name> -dt <table_name>


## Creating Specific table 
# To create a specific table run the following command 
1- python migration.py -u <username> -ho <host> -p <password> -d <database_name> -ct <table_name>


## Get list of tables 
# To get the list of tables run the following command 
1- python migration.py -u <username> -ho <host> -p <password> -d <database_name> -lt


## Get list of tables and columns 
# To get the list of tables and all columns with their types run the follwing command 
1- python migration.py -u <username> -ho <host> -p <password> -d <database_name> -ltc 


## Get list of size of tables 
# To get the list of size of tables run the following command 
1- python migration.py -u <username> -ho <host> -p <password> -d <database_name> -s
2- python migration.py -u <username> -ho <host> -p <password> -d <database_name> -s <table_name>

Point : <table_name> means this __tablename__ in models 
Point : Replace <username>, <host>, <password>, and <database_name> with your actual PostgreSQL username, host, password, and the desired name for the database.