# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 12:23:31 2023

@author: Madssar
"""
import libManSystem
import LibDatabase
from datetime import datetime, timedelta

class User():
    def __init__(self,name,userType,uid,cd): #cd means class or dept
        self.name = name
        self.userType = userType
        self.uid = uid
        self.cd = cd
            
        
    def menu(self):
             print(f"""\nMenu for {self.userType}
 1. Borrow book
 2. Return book
 3. Search book
 4. List borrowed books
 5. Pay Fine
 q. Logout
 """)
         
             c = input("\nSelect Option (1-4|q): ")
             choice = {"1" :self.borrow,
                   "2" :self.returnBook,
                   "3" :self.search,
                   "4" :self.listOfBorrowedBook,
                   "5" :self.payFine,
                   "q" :"q"}.get(c,"invalid")        
             if choice == "q":
                 print('Exiting...')
                 libManSystem.LibManSystem()
             elif choice != "invalid":
                 choice()
             else:
                 print("Choose a valid option...\n")
                 User.menu(self)
                 
   
    def borrow(self):
          '''This method is take the isbn from user and get the book from sqlite database to 
          borrow the book. If book quantity = 0 then it will reserve the book for user 
          and if 
          there is no book available against that isbn then it will return book not found'''
          
          #get current date
          current_date = datetime.now().date()
          #add 10 days delta to date
          due_date = current_date + timedelta(days=10)
          current_date = str(current_date)
          due_date = str(due_date)
          try:
              isbn = int(input("Please enter the ISBN:"))
              #fbTitle is found book title
              bol,fbTitle = LibDatabase.libDb.borrowBook(self.uid,self.name,isbn)
              if bol is True:
                  bookToAdd = fbTitle[0][0] #getting title from tuple
                  if self.userType == "student":
                      #creating table if not exist
                      LibDatabase.libDb.studentTable()
                      #inserting borrowed book into student table
                      LibDatabase.libDb.insertBorrowedBook(self.uid, self.name, self.userType, self.cd, bookToAdd, isbn, current_date, due_date)
                      User.menu(self)
                  elif self.userType == "staff":
                      LibDatabase.libDb.staffTable()
                      LibDatabase.libDb.insertBorrowedBook(self.uid, self.name, self.userType, self.cd, bookToAdd, isbn, current_date, due_date)
                      User.menu(self)
              elif bol == 'reserve':
                  print("\nBook reserved successfully\n")
                  User.menu(self)
          except IndexError:
               print("\nBook not found")
               User.menu(self)
          except Exception as e:
              print("\nadd valid ISBN",e)
              User.menu(self)
               
    def returnBook(self):
        '''Take the isbn from user and remove that book from student 
        and add back into books table'''
        try:
            isbn = input("Enter the isbn:")
            LibDatabase.libDb.return_book(isbn,self.userType)
            User.menu(self)
        except Exception as e:
            print("Something wrong happend",e)
            User.menu(self)
    
    def search(self):
          '''This method allow users to search the book by different methods'''
          print("""How do you want to search
                         1. by title
                         2. by author
                         3. by language
                         4. by publication date
                         5. Main Menu""")
          try:
              option = int(input("Enter your choice:"))
              searchString = input("Enter your search string:")
              if option == 1:
                  fbooks = LibDatabase.libDb.search("title", searchString)
              elif option == 2:
                  fbooks = LibDatabase.libDb.search("author", searchString)
              elif option == 3:
                  fbooks = LibDatabase.libDb.search("language", searchString)
              elif option == 4:
                  fbooks = LibDatabase.libDb.search("publication_date", searchString)
              elif option == 5:
                  User.menu(self)
              else:
                  print("Enter a valid choice")
                  User.search(self)
                    
              for v in fbooks:
                  #printing books with width and left allignment
                  print(f"\n{v[0]:<10}{v[1]:<10}{v[2]:<10}{v[3]:<10}{v[4]}\n")
              
              print('''1. Search Menu
2. Main Menu''')
              choice = int(input('Enter your choice:'))
              if choice == 1:
                  User.search(self)
              elif choice == 2:
                  User.menu(self)
                  
          except ValueError:
             print('Please enter valid value')
             User.search(self)
          except Exception as e:
             print('Something wrong happend',e)
             User.search(self)
    
    def listOfBorrowedBook(self):
        '''This method will display all the books user lended'''
        try:
            LibDatabase.libDb.listOFBorrowedBooks(self.uid, self.name, self.userType)
            print('\n1. Main Menu')
            choice = int(input('Enter your choice:'))
            if choice == 1:
                User.menu(self)
        except ValueError:
            print('Please enter valid value')
            User.menu(self)
        except Exception as e:
            print('Something wrong happend',e)
            User.menu(self)
        
    def payFine(self):
        '''This method allow user to pay the fine if available'''
        try:
            isbn = input("Enter the isbn of book:")
            LibDatabase.libDb.payFine(isbn,self.uid,self.userType)
            print('\t1. Main Menu')
            choice = int(input('Enter your choice:'))
            if choice == 1:
                User.menu(self)
        except ValueError:
            print('Please enter valid value')
            User.menu(self)
        except Exception as e:
            print('Something wrong happend',e)
            User.menu(self)
        
        