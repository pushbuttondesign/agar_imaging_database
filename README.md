# agar_imaging_database
A MySQL database for storing images of agar plates with a python front end for taking and labelling images
Additionally includes scripts for backing up the database weekly and documentation for setup & usage in a local laboratory environment

## Hardware required
- Computer running Ubuntu LTS with:
	- 1x 500GB HDD for OS in ext4
	- 1x 2TB HDD for database in ZFS
	- 1x 2TB HDD for database backup in ext4
- Logitech C270 USB webcam

## MySQL server setup
```
$sudo apt-get update
$sudo apt-get install mysql-server
$sudo service mysql start
```

## Python MySQL connector setup
```
$sudo apt-get install python3
$sudo python3 -m pip install --upgrade pip
$sudo pip3 install mysql-connector-python
```

## Set credentials
```
$mysql
$mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
$mysql> exit
$mysql_secure_installation
$mysql -u root -p password
```
TODO: create new user accounts & lockdown security


## Create database
```
$mysql> CREATE DATABASE mycelium;
$mysql> USE mycelium;
$mysql> SHOW DATABASES;
$mysql> CREATE TABLE plates (serial_id INT unsigned AUTO_INCREMENT, experiment_id INT unsigned NOT NULL, species TINYTEXT NOT NULL, strain TINYTEXT NOT NULL, PRIMARY KEY (serial_id));
$mysql> CREATE TABLE images (image_id INT unsigned AUTO_INCREMENT, serial_id INT unsigned NOT NULL, image_url VARCHAR(250) NOT NULL, date DATETIME(0) NOT NULL, PRIMARY KEY (image_id));
$mysql> CREATE TABLE experiments (experiment_id INT unsigned AUTO_INCREMENT, doc_url VARCHAR(250) NOT NULL, PRIMARY KEY (experiment_id));
$mysql> ALTER TABLE plates AUTO_INCREMENT = 1000;
$mysql> ALTER TABLE images AUTO_INCREMENT = 1;
$mysql> ALTER TABLE experiments AUTO_INCREMENT = 100;
$mysql> SHOW TABLES;
$mysql> EXIT;
```

## Setup Monthly Backups
```
$gh repo clone pushbuttondesign/agar_imaging_database
$cd agar_imaging_database
$mysql> select @datadir
$mysql> EXIT;
$apt-get install cron
$crontab ./crontab
```

## Data entry
```
$sudo chmod +x ./plate_capture.py
$./plate_capture.py
```

## Database querying
- [GUI](https://www.mysql.com/products/workbench/)
- [CMD](https://dev.mysql.com/doc/mysql-getting-started/en/)
- Querying computers must have local access, remote access to database is turned off
- It is suggested to add new users for each person accessing the database, increase backups if required
