from os import getenv


dbname = 'postgres'
user = 'postgres'
password = getenv('PG_PASSWORD')
host = 'localhost'
port = '5432'
