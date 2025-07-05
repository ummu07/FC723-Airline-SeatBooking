#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 03:05:32 2025

@author: ummusalmahumarrani
"""

# database_setup.py

import sqlite3

def initialize_database():
    """
    Create a SQLite database file and customers table if it doesn't already exist.
    """
    conn = sqlite3.connect("FC723 - Application/airline_booking.db")
    cursor = conn.cursor()

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
