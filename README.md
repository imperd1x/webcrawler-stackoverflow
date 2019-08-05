[![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square)](LICENSE.md)

# Webcrawler Stackoverflow
Python script to captures data from questions of stackoverflow and save the information in MySQL database. 

![alt text](https://raw.githubusercontent.com/cristianodpp/webcrawler-stackoverflow/master/234234242.png)

![alt text](https://raw.githubusercontent.com/cristianodpp/webcrawler-stackoverflow/master/918238372.png)

![alt text](https://github.com/cristianodpp/webcrawler-stackoverflow/blob/master/database_example.png)

## Requirements
- [Python 3](https://www.python.org/downloads/)
- [PyMySQL](https://pypi.org/project/PyMySQL/)
- [Unidecode](https://pypi.org/project/Unidecode/)
- [Requests](https://pypi.org/project/requests/)

## Install
```sh
$ brew install python3
```
```sh
$ pip3 install bs4
```
```sh
$ pip3 install pymysql
```
```sh
$ pip3 install unidecode
```
```sh
$ pip3 install requests
```

Create your database and insert the table
```mysql
CREATE TABLE `questions` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(355) DEFAULT NULL,
  `link` varchar(500) DEFAULT NULL,
  `answers` int(8) DEFAULT NULL,
  `views` int(9) DEFAULT NULL,
  `answered_accepted` tinyint(1) DEFAULT NULL,
  `description` text,
  `stackoverflow_id` int(12) DEFAULT NULL,
  `creation_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `stackoverflow_id` (`stackoverflow_id`)
) ENGINE=MyISAM AUTO_INCREMENT=446564 DEFAULT CHARSET=utf8;
```

Please change the strings inside file [/core/dbconnection.py] to connect database 
```python
self.db = pymysql.connect("localhost", "username", "password", "database")
```
