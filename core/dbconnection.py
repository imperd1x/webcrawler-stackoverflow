#!/usr/bin/python3

import pymysql
import json
from unidecode import unidecode 

class database:

    def __init__(self):
        print("Connecting database...")

        # Open database connection
        self.db = pymysql.connect("localhost", "username", "password", "database")
        print("Success!")
        
    def insertBulkList(self, bulkList):
        cursor = self.db.cursor()
        sql = """
        INSERT IGNORE INTO questions (title, link, answers, views, answered_accepted, stackoverflow_id) 
        VALUES (%(question)s, %(link)s, %(answers)s, %(views)s, %(answered_accepted)s, %(stackoverflow_id)s)
        """
        json_object = json.loads(unidecode(bulkList))
        insert_item = []
        
        for item in json_object:
            insert_item.append({
                "question": item['question'],
                "link": item['link'],
                "answers": item['answers'],
                "views": item['views'],
                "answered_accepted": item['answered_accepted'],
                "stackoverflow_id": item['id']
            })
        
        try:
            cursor.executemany(sql, insert_item)
            self.db.commit()
            print(65*"*")
            print("|", cursor.rowcount, "records inserted.")
            print("\n")
        finally:
            cursor.close()
