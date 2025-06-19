#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 23:53:50 2025

@author: ummusalmahumarrani
"""

# FC723 Airline Seat Booking System
# Part A: Starter version (no database yet)
# This program allows users to manage seat bookings on a Burka757 aircraft.

# ----------------------
# Seat Map  Initialization
# ----------------------

# Seat columns are labeled A-F, and there are 80 rows (1 to 80).
# F = Free, R = Reserved, X = Aisle, S = Storagee
seats = {} 


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
        

# Book a seat
def book_seat(seat_id):
    col = seat_id[-1].upper()
    try:
        row = int(seat_id[:-1]) - 1
        if col in seats and 0 <= row < 80:
            if seats[col][row] == 'F':
                seats[col][row] = 'R'
                print(f"Seat {seat_id} successfully booked.")
            elif seats[col][row] in ['R', 'X', 'S']:
                print(f"Seat {seat_id} is not available.")
            else:
                print("Invalid seat status.")
        else:
                print("Invalid seat number.") 
    except:
        print("Invalid input format.")   
        
        
# Free a booked seat
def free_seat(seat_id):
    col = seat_id[-1].upper()
    try:
        row = int(seat_id[:-1]) - 1
        if col in seats and 0 <= row < 80:
            if seats[col][row] == 'R':
                seats[col][row] = 'F'
                print(f"Seat {seat_id} has been freed.") 
            else:
                print(f"Seat {seat_id} is not currently booked.") 
        else: 
            print(f"Seat {seat_id} is not currently booked.") 
    except:
        print("Invalid input format.") 
        
        
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
            if status == 'R':
                print(f"Seat {seat_id} is booked. (Reserved by Passenger)") 
            elif status == 'F':
                print(f"Seat {seat_id} is currently free.") 
            elif status in ['X', 'S']:
                print(f"Seat {seat_id} is not a bookable seat.")
            else:
                print("Unknown seat status.")
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