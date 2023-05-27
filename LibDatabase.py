# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 12:22:58 2023

@author: Madssar
"""

import sqlite3
import datetime

class LibDatabase:
    def __init__(self):
        #conn = sqlite3.connect(':memory:')
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()

    def booksTable(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS  books(
                isbn integer PRIMARY KEY,
                title text,
                author text,
                language text,
                publication_date text,
                available integer
                )""")
    def studentTable(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS  student(
                userid integer,
                name text,
                class text,
                borrowedBooks text,
                isbn text,
                borrowDate text,
                dueDate text,
                returnDate text,
                fine integer
                )""")
    def staffTable(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS  staff(
                userid integer,
                name text,
                dept text,
                borrowedBooks text,
                isbn text,
                borrowDate text,
                dueDate text,
                returnDate text,
                fine integer
                )""")
 
    def insertBook(self, isbn, title, author, language, publication_date, available):
        try:
            with self.conn:
                insert = """INSERT INTO books
                          (isbn, title, author, language, publication_date, available) 
                          VALUES (?, ?, ?, ?, ?, ?);"""
                data_tuple = (isbn, title, author,language, publication_date, available)
                self.c.execute(insert, data_tuple)
                #self.c.execute("INSERT INTO books(isbn,title,author,available) values(?, ?, ?, ?)",(isbn,title,author,available))
                print("\nBook added successfully")
                self.conn.commit()
        except:
            print("Something wrong happend")
                
    def insertBorrowedBook(self,uid,name,userType,uclass,borrowedBook,isbn,borrowedDate,dueDate):    
        try:
            with self.conn:
                tableName = "student" if userType == "student" else "staff"
                deptOrClass = "class" if userType == "student" else "dept"
                insert = f"""INSERT INTO {tableName}
                          (userid, name, {deptOrClass}, borrowedBooks, isbn, borrowDate, dueDate, returnDate, fine) 
                          VALUES (?, ?, ?, ?, ?, ?, ?,NULL,NULL);"""
                data_tuple = (uid, name, uclass, borrowedBook, isbn, borrowedDate, dueDate)
                self.c.execute(insert, data_tuple)
                print("\nBook Borrowed successfully")
                self.conn.commit()
        except Exception as e:
            print("Something wrong happend here",e)
            
    def search(self,opt,s): #opt = option e.g search by title or author, s = string you want to search e.g 'Harry'
        s = '%'+s+'%'
        cmd = f'SELECT * FROM books WHERE {opt} LIKE :s'
        if opt in ['title','author','language','publication_date']:
            self.c.execute(cmd, {'s':s})
        else: 
            print("Book Not Found")
        return self.c.fetchall()
        
    def borrowBook(self,uid,name,isbn):
        try:
            self.c.execute("SELECT TITLE FROM BOOKS WHERE ISBN = ? AND AVAILABLE = 0",(isbn,))
            title = self.c.fetchone()
            
            if title is not None:
                title = title[0]
                self.c.execute("""CREATE TABLE IF NOT EXISTS  reservedBooks(
                    userid integer,
                    name text,
                    isbn text,
                    title text
                    )""")
                self.c.execute("INSERT INTO reservedBooks (userid, name, isbn, title) VALUES (?, ?, ?, ?)",(uid, name, isbn, title))
                self.conn.commit()
                return 'reserve',''
            else:
                self.c.execute("SELECT TITLE FROM BOOKS WHERE ISBN = ? AND AVAILABLE != 0",(isbn,))
                book = self.c.fetchall()
                #execute command do not rise any exception because it sends empty result even nothing found so i am using if else to overcome this issue
                if book:
                    # Execute an SQL query to decrement the available value by 1
                    self.c.execute("UPDATE books SET available = available - 1 WHERE isbn = ?", (isbn,))
                    return True, book
                else:
                    print("Book not found")
                    return False,''
        except Exception as e:
            print("Something wrong happend",e)
            return False,''

                      
    def return_book(self,isbn,userType):
        #get current date
        current_date = datetime.date.today()
        current_date = str(current_date)
        try:
            with self.conn:
                self.c.execute("UPDATE books SET available = available + 1 WHERE isbn = ?", (isbn,))
                tableName = "student" if userType == "student" else "staff"
                self.c.execute(f"Update {tableName} set returnDate = ?",(current_date,))
                print("\nBook returned successfully")
                return True
        except Exception as e:
            print('Please try again',e)
            
    def remove_book(self,title,author):
        try:
            with self.conn: 
                self.c.execute("SELECT * FROM books WHERE title=? AND author=?", (title,author))
                result = self.c.fetchone()
                if result:
                    self.c.execute("DELETE from books where title = ? AND author = ?",(title,author))
                    self.conn.commit()
                    print("\nBook Removed successfully")
                else:
                    print("\nBook not found")
        except:
            print("\nSomething wrong happend")
    
    def showReport(self,table):
        try:
            self.c.execute(f'PRAGMA table_info({table})')
            columns = self.c.fetchall()
            column_names = [column[1] for column in columns]
            #Remove brackets using join() and convert values to strings
            column_names_str = ', '.join(column_names)
            print(column_names_str)
            self.c.execute(f"select * from {table}")
            rows = self.c.fetchall()
            for row in rows:
                print(', '.join(str(value) for value in row))  # Remove brackets using join() and convert values to strings
        except Exception as e:
            print(e)
    
    def fine(self):
        try:
            current_datetime = datetime.datetime.now()
            current_date = current_datetime.date()
            self.c.execute("SELECT name,dueDate from student")
            studentRows = self.c.fetchall()
            self.c.execute("select name,dueDate from staff")
            staffRows = self.c.fetchall()
            
            for row in studentRows:
                studentName = row[0]
                dueDate = row[1]
                #converting dueDate string to date object
                dueDate = datetime.datetime.strptime(dueDate, "%Y-%m-%d").date()
                if current_date > dueDate:
                    # Calculate the fine amount based on table name (students or staff)
                    fine_amount = 10
                    # Update the respective table with the fine amount
                    self.c.execute("UPDATE student SET fine = ?", (fine_amount,))
                    self.conn.commit()
                    print(f"Fine of {fine_amount} pounds imposed on student {studentName}")
                else:
                    return False
                
            for row in staffRows:
                staffName = row[0]
                dueDate = row[1]
                #converting dueDate string to date object
                dueDate = datetime.datetime.strptime(dueDate, "%Y-%m-%d").date()
                if current_date > dueDate:
                    # Calculate the fine amount based on table name (students or staff)
                    
                    fine_amount = 5
            
                    # Update the respective table with the fine amount
                    self.c.execute("UPDATE staff SET fine = ?", (fine_amount,))
                    self.conn.commit()
                    print(f"Fine of {fine_amount} pounds imposed on staff {staffName}")
                else:
                    return False
        except Exception as e:
            print(e)
        
                
    def payFine(self,isbn,uid,userType):
        try:
            tableName = "student" if userType == "student" else "staff"
            fine_amount = 10 if userType == "student" else 5
            self.c.execute(f"select fine from {tableName} where isbn = {isbn} AND userid = {uid}")
            fine = self.c.fetchone()
            fine=fine[0]
            if fine != None:
                done = fine - fine_amount
                self.c.execute(f"update {tableName} set fine = {done}")
                self.conn.commit()
            else:
                print('\nYou do not have any fine\n')
        except Exception as e:
            print("Failure",e)
    
    def listOFBorrowedBooks(self,uid,name,userType):
        try:
            tableName = 'student' if userType == 'student' else 'staff'
            self.c.execute(f'PRAGMA table_info({tableName})')
            columns = self.c.fetchall()
            column_names = [column[1] for column in columns]
            #Remove brackets using join() and convert values to strings
            column_names_str = ', '.join(column_names)
            print(column_names_str)
            self.c.execute(f'select * from {tableName} where userid = ? AND name = ?',(uid,name,))
            rows = self.c.fetchall()
            for row in rows:
                print(', '.join(str(value) for value in row))  # Remove brackets using join() and convert values to strings
        except Exception as e:
            print(e)
            
libDb = LibDatabase()
#libDb.fine()
#libDb.showTables()
#libDb.showValues()
#libDb.studentTable()
#libDb.showStudentValues()
#libDb.deleteTable("books")
#libDb.showTables()
#libDb.showStaffValues()
#libDb.fine()
#libDb.payFine(12,1,"student")