CREATE DATABASE "inzynieria-srodowiska";
CREATE USER django WITH ENCRYPTED PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE "inzynieria-srodowiska" TO django;