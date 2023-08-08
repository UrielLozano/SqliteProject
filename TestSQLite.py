# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 22:26:53 2023

@author: Cooks
"""

import sqlite3
from sqlite3 import Error
 
def create_connection():
    try:
        conn = sqlite3.connect(':memory:')
        print(f"You are running SQLite version {sqlite3.version}")
    except Error as e:
        print(e)
    finally:
        conn.close()
        
if __name__ == '__main__':
    create_connection()
