# Webcrawler Stackoverflow
Python Script to get all questions from this website.

Implemented MySQL connection to insert on table.

CREATE TABLE `questions` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(355) DEFAULT NULL,
  `description` text,
  `link` varchar(500) DEFAULT NULL,
  `answers` int(8) DEFAULT NULL,
  `views` int(9) DEFAULT NULL,
  `answered_accepted` tinyint(1) DEFAULT NULL,
  `stackoverflow_id` int(12) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `stackoverflow_id` (`stackoverflow_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1801 DEFAULT CHARSET=utf8;


![alt text](https://raw.githubusercontent.com/cristianodpp/webcrawler-stackoverflow/master/234234242.png)

![alt text](https://raw.githubusercontent.com/cristianodpp/webcrawler-stackoverflow/master/918238372.png)

[![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square)](LICENSE.md)

This project uses [BeautifulSoup 4.4.0](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) 

## Requirements

    - python3 
    - bs4 

## Install

    $ brew install python3

    $ pip3 install bs4


