# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 12:20:32 2023

@author: Madssar
"""
#import LibDatabase

import json
import Librarian
import User

class LibManSystem:

    def __init__(self):
        LibManSystem.homepage()
        
    def homepage():
        while True:
            print("""
                    Homepage
                    1. Login
                    2. Register
                    3. Exit
                    """)
            try:
                homeChoice = int(input("Enter your choice: "))
                if homeChoice == 1:
                    LibManSystem.login()
                    break
                elif homeChoice == 2:
                    LibManSystem.register()
                    break
                elif homeChoice == 3:
                    print("Exiting...")
                    break
                else:
                    print("Please enter a valid Number")
            except ValueError:
                print("Please enter a valid choice")
                                              
    def authenticate(username,password):
        '''Getting username and password from login method and authenticate the user from login.json file'''
        
        with open('login.json', 'r') as f:
            data = json.load(f)

        # Check if the username and password match in the "students" list
        for student in data['students']:
            if student['username'] == username and student['password'] == password:
                return True, student["userType"], student["id"], student["class"]
        
        # Check if the username and password match in the "staff" list
        for staff in data['staff']:
            if staff['username'] == username and staff['password'] == password:
                return True, staff["userType"], staff["id"], staff["department"] 
        
        # Check if the username and password match in the "librarian" list
        for librarian in data['librarian']:
            if librarian['username'] == username and librarian['password'] == password:
                return True, librarian["userType"], librarian["id"], librarian["username"]
        
        # If no match is found, return False
        return False, "", "", ""
    
           
    def login():
        
            '''Take username and password as input and authnticate user using authenticate method and redirect user to their respective menu'''
            
            print("Welcome to BCU Lib System")
            username = input("Enter username: ")
            password = input("Enter your password: ")
            #u,v,i,s  u = bolean v = userType i = id and s = class/department
            u,v,i,s = LibManSystem.authenticate(username, password)
            if u:
                if v == "student":
                    stdObj = User.User(username, v, i, s)
                    stdObj.menu()
                elif v == "staff":
                    staffobj = User.User(username, v, i, s)
                    staffobj.menu()
                elif v == "librarian":
                    librarianObj = Librarian.Librarian(username, i)
                    librarianObj.menu()
            else:
                print("\ninccorect username or password\n")
                LibManSystem.homepage()
            
    
    def register():
        '''Take inputs from user and save data into json file'''
        try:
            print("Welcome to registration area")
            userid = int(input("Enter your id: "))
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            
            print("""
                    User-Types
                    1. Student
                    2. Staff
                    3. Librarian""")
        
            choice = int(input("\nSelect Option from available usertypes: "))
    
            # creating dictonary to populate data according to user-type
            users = {"students": [], "staff": [], "librarian": []}
        
            if choice == 1:
                studentClass = input("Enter your class name:")
                try:
                    with open("login.json", "r") as infile:
                       users = json.load(infile)
                    #creating new dictonary to populate data entered by user   
                    new_student = {"id": userid, "username": username, "password": password, "class":studentClass, "userType":"student"}
                    #appending newly created new_student dictonary into users dictonary
                    users["students"].append(new_student)
                    
                    #now newly entered data is available in users dictonary so writing it into json file
                    with open("login.json", "w") as fd:
                        json.dump(users, fd)
                        print("\nYou're successfully registered\n")
                        fd.close()
                        LibManSystem.homepage()
                except FileNotFoundError:
                    users["students"] = [{"id": userid, "username": username, "password": password, "class":studentClass, "userType":"student"}]
                    with open("login.json", "w") as fd:
                        json.dump(users, fd)
                        print("\nYou're successfully registered\n")
                        fd.close()
                        LibManSystem.homepage()
        
            elif choice == 2:
                staffDept = input("Enter your department:")
                try:
                    with open("login.json", "r") as infile:
                       users = json.load(infile)
                    new_staff = {"id": userid, "username": username, "password": password, "department":staffDept, "userType":"staff"}
                    users["staff"].append(new_staff)
        
                    with open("login.json", "w") as fd:
                        json.dump(users, fd)
                        print("\nYou're successfully registered\n")
                        fd.close()
                        LibManSystem.homepage()
        
                except FileNotFoundError:
                    users["staff"] = [{"id": userid,
                                      "username": username, "password": password, "department":staffDept, "userType":"staff"}]
                    with open("login.json", "w") as fd:
                        json.dump(users, fd)
                        print("\nYou're successfully registered\n")
                        fd.close()
                        LibManSystem.homepage()
        
            elif choice == 3:
                try:
                    with open("login.json", "r") as infile:
                       users = json.load(infile)
                    librarian = {"id": userid,
                                 "username": username, "password": password, "userType":"librarian"}
                    users["librarian"].append(librarian)
                    with open("login.json", "w") as fd:
                        json.dump(users, fd)
                        print("\nYou're successfully registered\n")
                        fd.close()
                        LibManSystem.homepage()
                except FileNotFoundError:
                    users["librarian"] = [{"id": userid,
                                          "username": username, "password": password, "userType":"librarian"}]
                    with open("login.json", "w") as fd:
                        json.dump(users, fd)
                        print("\nYou're successfully registered\n")
                        fd.close()
                        LibManSystem.homepage()
            else:
                print("Please enter a valid number\n")
                LibManSystem.homepage()
        except:
            print("Enter a valid value")
            LibManSystem.homepage()
            
        

bcu =  LibManSystem()