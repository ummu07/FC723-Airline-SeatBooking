#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 23:53:50 2025

@author: ummusalmahumarrani
"""
import sqlite3 # For intresting with the SQLite database 

# FC723 Airline Seat Booking System
# Part A: Starter version (no database yet)
# This program allows users to manage seat bookings on a Burka757 aircraft.

# ----------------------
# Seat Map  Initialization
# ----------------------

# Seat columns are labeled A-F, and there are 80 rows (1 to 80).
# F = Free, R = Reserved, X = Aisle, S = Storagee
seats = {} 


# Check that the seat alyout matches the project brief. CUrrently the rows do not
# match the ailse layout of the plane. CB
# Initialize seats with 'F', but insert 'X' and 'S' for specific columns/rows 
for col in ['A', 'B', 'C', 'D', 'E', 'F' ]:
    seats[col] = [] 
    for row in range(1, 81): 
        # Example: make rows 40-45 aisle (X) in column C and D 
        # Aisle seats: rows 40-45 in columns C and D 
        if col in ['C', 'D'] and 40 <= row <= 80:
            seats[col].append('X') 
        # Example: make rows 75-80 storage (S) in columns C and D 
        # Storage seats: rows 75-80 in columns D, E, F
        if col in ['C', 'D'] and 40 <= row <= 45: 
            seats[col].append('X')
        # Example: make rows 75-80 storage (S) in cloumns D, E, F
        elif col in ['D', 'E', 'F'] and 75 <= row <= 80:
            seats[col].append('S') 
        else:
            seats[col].append('F') 
            
# You should make a class with all of the functions associated to your menu as the
# methods of that class. Then you can instantiate the seat alyout as part of the attributes. CB

# You may also want to make use of user-defined modules. So the 'main' python file can contain
# the logic for running the program, while importing the functionality of the program
# from another file. Creating the database can also be performed by another module. CB
# Display main menu 
def show_menu():
    print("\n===== Apache Airline Seat Booking =====")
    print("1.Check availability of seat")
    print("2. Book a seat")
    print("3. Free a seat")
    print("4. Show booking status")
    print("5. Search for a booking (Extra Feature)")
    print("6. Exist")
    
    
# Check if a seat is available 
def check_seat(seat_id):
    col = seat_id[-1].upper() 
    try: 
        row = int(seat_id[:-1]) - 1 
        if col in seats and 0 <= row < 80: 
            status = seats[col][row] 
            print(f"Seat {seat_id} status: {status}") 
        else:
            print("Invalid seat number.")
    except:
        print("Invalid input format. Use format like 12A.") 
        

import random
import string 

# ----------------------------
# Temporary Booking Reference List
# ----------------------------
existing_refs = [] 


# ----------------------------
# Generate Unique Booking Reference 
# ----------------------------

def generate_booking_reference(existing_refs):
    """
    
    Generate a unique 8-character alphanumeric booking reference.    
    Checks against a list of existing reference to ensure uniqueness.
    
    """
    
    while True:
        # Generate a random 8- character string
        reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) 
        
        # Checks for uniqueness
        if reference not in existing_refs:
            return reference
        
        
# Book a seat
def book_seat(seat_id):
    col = seat_id[-1].upper()
    try:
        row = int(seat_id[:-1]) - 1 # Convert seat like "12A" to row 11, col A
        if col in seats and 0 <= row < 80:
            if seats[col][row] == 'F':
                # Step 1: Get customer details
                first_name = input("Enter passenger's first name:")
                last_name = input("Enter passenger's last name:")
                passport = input("Enter passport number:") 
                
                # Step 2: Generate booking reference
                booking_ref = generate_booking_reference(existing_refs)
                existing_refs.append(booking_ref)
                
                # Step 3: Store reference in the seat map
                seats[col][row] = booking_ref 
                
                # Step 4: Insert booking data into the database
                conn = sqlite3.connect("/Users/ummusalmahumarrani/Desktop/FC723_Project_P480954/FC723 - Application/airline_booking.db") 
                cursor = conn.cursor() 
                cursor.execute('''
                     INSERT INTO customers (booking_ref, first_name, last_name, passport, seat_row, seat_col)
                     VALUES (?, ?, ?, ?, ?, ?)
                ''',  (booking_ref, first_name, last_name, passport, row + 1, col))
                conn.commit()
                conn.close() 
                
                # Step 5: Display confirmation
                print(f"\nSeat {seat_id} successfully booked!")
                print("----- Booking Details ------")
                print(f"Name      :  {first_name} {last_name}")
                print(f"Passport   :  {passport}")
                print(f"Seat      :  {seat_id}")
                print(f"Reference :  {booking_ref}")
                print("----------------------------")
                
                
            elif seats[col][row] in ['R', 'X', 'S']:
                print(f"Seat {seat_id} is not a valid bookable seat.")
            else:
                print(f"Seat {seat_id} is already booked.")
        else:
                print("Invalid seat number.") 
    except Exception as e:
        print("An error occurred during booking:", e) 
        
# You have a lsit of existing references here, but you have a database to store this information
# isntead. Which do you use? CB

# Test the booking reference generator
existing_refs = ["X9YZ123A", "ABCD1234"]
new_ref = generate_booking_reference(existing_refs)
print(f"New booking reference: {new_ref}")
        
# Free a booked seat
def free_seat(seat_id):
    col = seat_id[-1].upper()
    try:
        row = int(seat_id[:-1]) - 1
        
        
        # Check if the seat is valid and booked
        if col in seats and 0 <= row < 80:
            current_value = seats[col][row]
            
            
            if current_value not in ['F', 'X', 'S']:
                # Step 1: Set seat back to 'F'
                seats[col][row] = 'F' 
                
                
                # Step 2: Delete from database using the booking reference 
                try:
                    conn = sqlite3.connect("/Users/ummusalmahumarrani/Desktop/FC723_Project_P480954/FC723 - Application/airline_booking.db")
                    cursor = conn.cursor() 
                    
                    
                    # Use the booking reference stored in the seat
                    cursor.execute("DELETE FROM customers WHERE booking_ref = ?", (current_value,))
                    conn.commit()
                    conn.close() 
                    
                    
                    print(f"Seat {seat_id} has been successfully freed and booking removed.")
                except Exception as db_error:
                    print("Database error during seat release:", db_error) 
            else:
                print(f"Seat {seat_id} is not currently booked.") 
        else:
            print("Invalid seat number.")
    except Exception as e:
        print("Input error:", e)
    
            
# Show full booking status
def show_status():
    print("\n "+" ".join([col for col in seats])) 
    for i in range(80):
        row_display = f"{i+1:02d} "
        for col in seats:
            row_display += seats[col][i] + " "
        print(row_display) 
        
        
# Extra Feature: Search Booking by Seat 
def search_booking(seat_id):
    col = seat_id[-1].upper() 
    try:
        row = int(seat_id[:-1]) - 1
        if col in seats and 0 <= row < 80:
            status = seats[col][row]
            if status == 'F':
                print(f"Seat {seat_id} is currently free.") 
            elif status == ['X', 'S']:
                print(f"Seat {seat_id} is not a bookable seat.") 
            else:
                # Any string other than F/X/S is a booking reference
                print(f"Seat {seat_id} is booked. (Reference: {status})")
        else:
            print("Invalid seat number.") 
    except:
        print("Invalid input format.") 
        
        
# Main program loop
while True:
    show_menu()
    choice = input("Enter your choice (1-6): ")
    
    
    if choice == '1':
        seat = input("Enter seat (e.g., 12A): ") 
        check_seat(seat)
    elif choice == '2':
        seat = input("Enter seat to book (e.g., 12A): ")
        book_seat(seat) 
    elif choice == '3':
        seat = input("Enter seat to free (e.g., 12A): ")
        free_seat(seat) 
    elif choice == '4':
        show_status()
    elif choice == '5':
        seat = input("Enter seat to search (e.g., 12A):")
        search_booking(seat)
    elif choice == '6':
        print("Exiting program. Goodbye!")
        break
    

# Again here, the database initialisation can be kept in a different file and instantiated
# when you create the booking system in you main py file. CB 
    
# --------------------------
# Create the SQLite database and customers table (if not exists) 
# --------------------------
def initialize_database():
    """
    Create a SQLite database file and customers table if it doesn't already exist.
    The table stores booking reference, passenger name, passport number, and seat info.
    """
    # Connect to SQLite database (creats file if it doesn't exist)
    conn = sqlite3.connect("airline_booking.db")
    cursor = conn.cursor()


    # Create the table with appropriate fields
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS customers(
                       booking_ref TEXT PRIMARY KEY,
                       first_name TEXT NOT NULL,
                       last_name TEXT NOT NULL,
                       passport TEXT NOT NULL,
                       seat_row INTEGER NOT NULL,
                       seat_col TEXT NOT NULL
                    ) 
                   ''') 
                   
                   
          # Commit the chnage and close connection 
    conn.commit()
    conn.close()
initialize_database() 