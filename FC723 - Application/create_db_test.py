#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 23:59:53 2025

@author: ummusalmahumarrani
"""

import os

# Delete existing DB if it exists
if os.path.exists("airline_booking.db"):
    os.remove("airline_booking.db")
    print("Old database removed. A new one will be created.")


import sqlite3
import os

def initialize_database():
    # Define full path to the .db file
    db_path = "/Users/ummusalmahumarrani/Desktop/FC723_Project_P480954/FC723 - Application/airline_booking.db"

    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create customers table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            booking_ref TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            passport TEXT NOT NULL,
            seat_row INTEGER NOT NULL,
            seat_col TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

initialize_database()
