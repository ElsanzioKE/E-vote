-- Prepares a MySQL server for the tisher project.
CREATE DATABASE IF NOT EXISTS evote;
CREATE USER IF NOT EXISTS 'evote_dev'@'localhost' IDENTIFIED BY 'evote_pwd';
GRANT ALL PRIVILEGES ON evote . * TO 'evote_dev'@'localhost';
GRANT SELECT ON performance_schema . * TO 'evote_dev'@'localhost';
