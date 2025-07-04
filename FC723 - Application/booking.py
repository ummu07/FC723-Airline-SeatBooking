#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 14:58:46 2025

@author: ummusalmahumarrani
"""

import sqlite3
import random
import string

class BookingSystem:
    def __init__(self):
        # Initialize seat layout and database
        self.seats = {}
        self.initialize_seat_map()

    def initialize_seat_map(self):
        # Set up seat layout for columns A-F and rows 1–80
        for col in ['A', 'B', 'C', 'D', 'E', 'F']:
            self.seats[col] = []
            for row in range(1, 81):
                if col in ['C', 'D'] and 40 <= row <= 45:
                    self.seats[col].append('X')  # Aisle
                elif col in ['D', 'E', 'F'] and 75 <= row <= 80:
                    self.seats[col].append('S')  # Storage
                else:
                    self.seats[col].append('F')  # Free

    def show_menu(self):
        print("\n===== Apache Airline Seat Booking =====")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking status")
        print("5. Search for a booking (Extra Feature)")
        print("6. Exit")

    def check_seat(self, seat_id):
        """
        Checks if a seat is available or booked.
        """
        col = seat_id[-1].upper()
        try:
            row = int(seat_id[:-1]) - 1
            if col in self.seats and 0 <= row < 80:
                status = self.seats[col][row]
                print(f"Seat {seat_id} status: {status}")
            else:
                print("Invalid seat number.")
        except Exception:
            print("Invalid input format. Use format like 12A.")


    def show_status(self):
        pass  # To be implemented

    def search_booking(self, seat_id):
        pass  # To be implemented

    def run(self):
        while True:
            self.show_menu()
            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                seat = input("Enter seat (e.g., 12A): ")
                self.check_seat(seat)
            elif choice == '2':
                seat = input("Enter seat to book (e.g., 12A): ")
                self.book_seat(seat)
            elif choice == '3':
                seat = input("Enter seat to free (e.g., 12A): ")
                self.free_seat(seat)
            elif choice == '4':
                self.show_status()
            elif choice == '5':
                seat = input("Enter seat to search (e.g., 12A): ")
                self.search_booking(seat)
            elif choice == '6':
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid choice. Please select between 1 and 6.") 
                
                
    def generate_booking_reference(self):
        """
        Generates a unique 8-character alphanumeric reference. Ensures it's not already in the DB.
        """
        while True:
            ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            try:
                conn = sqlite3.connect("/Users/ummusalmahumarrani/Desktop/FC723_Project_P480954/FC723 - Application/airline_booking.db")
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM customers WHERE booking_ref = ?", (ref,))
                result = cursor.fetchone()
                conn.close()
                if not result:
                    return ref
            except:
                return ref  # fallback: return ref if DB check fails

                
    def book_seat(self, seat_id):
        """
        Books a seat if it is free. Collects passenger details, generates a booking reference,
        updates the seat map, and inserts the data into the SQLite database.
        """
        col = seat_id[-1].upper()
        try:
            row = int(seat_id[:-1]) - 1
            if col in self.seats and 0 <= row < 80:
                current_status = self.seats[col][row]
                if current_status == 'F':
                    # Get passenger details
                    first_name = input("Enter passenger's first name: ")
                    last_name = input("Enter passenger's last name: ")
                    passport = input("Enter passport number: ")
    
                    # Generate a unique 8-character booking reference
                    booking_ref = self.generate_booking_reference()
    
                    # Update seat map with booking ref
                    self.seats[col][row] = booking_ref
    
                    # Insert booking into database
                    try:
                        conn = sqlite3.connect("/Users/ummusalmahumarrani/Desktop/FC723_Project_P480954/FC723 - Application/airline_booking.db")
                        cursor = conn.cursor()
                        cursor.execute('''
                            INSERT INTO customers (booking_ref, first_name, last_name, passport, seat_row, seat_col)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (booking_ref, first_name, last_name, passport, row + 1, col))
                        conn.commit()
                        conn.close()
    
                        # Display confirmation
                        print(f"\nSeat {seat_id} successfully booked!")
                        print("----- Booking Details ------")
                        print(f"Name      :  {first_name} {last_name}")
                        print(f"Passport  :  {passport}")
                        print(f"Seat      :  {seat_id}")
                        print(f"Reference :  {booking_ref}")
                        print("----------------------------")
                    except Exception as db_err:
                        print("Database error:", db_err)
                elif current_status in ['X', 'S']:
                    print(f"Seat {seat_id} is not a valid bookable seat.")
                else:
                    print(f"Seat {seat_id} is already booked.")
            else:
                print("Invalid seat number.")
        except Exception as e:
            print("Invalid input format:", e)


    def free_seat(self, seat_id):
        """
        Frees a booked seat and removes the corresponding booking from the database.
        """
        col = seat_id[-1].upper()
        try:
            row = int(seat_id[:-1]) - 1
    
            if col in self.seats and 0 <= row < 80:
                current_value = self.seats[col][row]
    
                # Only proceed if the seat contains a booking reference (not F, X, or S)
                if current_value not in ['F', 'X', 'S']:
                    # Free the seat in the seat map
                    self.seats[col][row] = 'F'
    
                    # Remove from the database using the booking reference
                    try:
                        conn = sqlite3.connect("/Users/ummusalmahumarrani/Desktop/FC723_Project_P480954/FC723 - Application/airline_booking.db")
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM customers WHERE booking_ref = ?", (current_value,))
                        conn.commit()
                        conn.close()
    
                        print(f"Seat {seat_id} has been successfully freed and booking removed.")
                    except Exception as db_err:
                        print("Database error while freeing seat:", db_err)
                else:
                    print(f"Seat {seat_id} is not currently booked.")
            else:
                print("Invalid seat number.")
        except Exception as e:
            print("Error:", e) 

