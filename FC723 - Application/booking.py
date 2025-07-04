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

    def book_seat(self, seat_id):
        pass  # To be implemented next

    def free_seat(self, seat_id):
        pass  # To be implemented

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