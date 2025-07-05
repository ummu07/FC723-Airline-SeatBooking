#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 15:24:09 2025

@author: ummusalmahumarrani
"""

from database_setup import initialize_database


# main.py
from booking import BookingSystem

if __name__ == "__main__":
    system = BookingSystem()
    system.run()
