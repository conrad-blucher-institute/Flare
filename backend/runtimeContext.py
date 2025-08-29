# -*- coding: utf-8 -*-
# flareRunner.py
#----------------------------------
# Created By : Anointiyae Beasley
#----------------------------------
""" This script initializes thread-local storage for managing data that 
should remain isolated across multiple threads.
 """ 
#----------------------------------
# 
#
#Imports
import threading
thread_storage = threading.local()