# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 22:39:50 2023

@author: Cooks
"""
import random
import sqlite3
from sqlite3 import Error
import concurrent.futures

people_db_file = "sqlite.db"
max_people = 500

def generate_people(count):
    #count = 0
    last_names = []
    first_names = []
    with open('LastNames.txt', 'r') as filehandle:
            last_names = [line.rstrip() for line in filehandle]
            
    with open('FirstNames.txt', 'r') as filehandle:
            first_names = [line.rstrip() for line in filehandle]
    names = []
    item1 = 0
    for x in range(count):
        item2 = first_names[random.randint(0,len(first_names)-1)]
        item3 = last_names[random.randint(0,len(last_names)-1)]
        my_tuple = (item1,item2,item3)
        names.append(my_tuple)
        item1 += 1
    return names  

def create_people_database(db_file, count):
    conn = sqlite3.connect(db_file)
    with conn:
        sql_create_people_table = """ CREATE TABLE IF NOT EXISTS people (
        id integer PRIMARY KEY,
        first_name text NOT NULL,
        last_name text NOT NULL); """
        cursor = conn.cursor()
        cursor.execute(sql_create_people_table)
        sql_truncate_people = "DELETE FROM people;"
        cursor.execute(sql_truncate_people)
        people = generate_people(count)
        sql_insert_person = "INSERT INTO people(id,first_name,last_name) VALUES(?,?,?);"
        for person in people:
            #print(person) # uncomment if you want to see the person object
            cursor.execute(sql_insert_person, person)
        #print(cursor.lastrowid) # uncomment if you want to see the row id 
        cursor.close()


class PersonDB():
    
    def __init__(self, db_file=''):
        self.db_file = db_file
        
    def __enter__(self):
        conn = sqlite3.connect(self.db_file)
        self.conn = conn
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.conn.close()
        
    def load_person(self, id):
        sql = "SELECT * FROM people WHERE id=?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (id,))
        records = cursor.fetchall()
        result = (-1,'','') # id = -1, first_name = '', last_name = ''
        if records is not None and len(records) > 0:
            result = records[0]
        cursor.close()
        return result
    
def test_PersonDB():
    with PersonDB(people_db_file) as db:
        print(db.load_person(10000)) # Should print the default
        print(db.load_person(122))
        print(db.load_person(300))

def load_person(id, db_file):
    with PersonDB(db_file) as db:
        return db.load_person(id)
    
def people_Futures():
    lst = []
    with concurrent.futures.ThreadPoolExecutor(10) as executor:
        futures = [executor.submit(load_person, ids, people_db_file) for ids in range(max_people)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            lst.append(result)
        print(lst)
if __name__ == "__main__":
    #people = generate_people(100)
    #print(people)
    #create_people_database(people_db_file, max_people)
    #test_PersonDB()
    people_Futures()



        