# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 12:24:37 2023

@author: Madssar
"""
import LibDatabase
import libManSystem
class Librarian():
    def __init__(self,name,uid):
        self.name = name
        self.uid = uid
        
    def menu(self):
        print(f"""
              Welcome {self.name}
              1. addBook
              2. Remove Book
              3. addFine 
              4. Show Report
              5. Logout""")
        
        try:
            choice = int(input("Enter your choice:"))
            if choice == 1:
                Librarian.addBook(self)
            elif choice == 2:
                Librarian.removeBook(self)
            elif choice == 3:
                Librarian.addFine(self)
            elif choice == 4:
                Librarian.getReport(self)
            elif choice == 5:
                Librarian.logout()
            else:
                print("\nChoose valid number\n")
                Librarian.menu(self)
        except ValueError:
            print('\nEnter valid choice\n')
            Librarian.menu(self)
        except Exception as e:
            print('\nSomething wrong happend',e)
            Librarian.menu(self)
        
            
    def addBook(self):
        '''This method allow librarian to add new book into database'''
        try:
            isbn = int(input("Enter isbn:"))
            title = input("Enter title:")
            author = input("Enter author:")
            language = input("Enter language:") 
            publication_date = input("Enter publication date(yyyy-mm-dd):")
            available = int(input("Enter copies available:"))
            LibDatabase.libDb.booksTable()
            LibDatabase.libDb.insertBook(isbn, title, author, language, publication_date, available)
            Librarian.menu(self)
        except ValueError:
            print('\nPlease Enter valid values\n')
            Librarian.menu(self)
        except Exception as e:
            print('Something wrong happend',e)
            Librarian.menu(self)
        
       
    def removeBook(self):
        '''this method allow librarian to remove book from database'''
        title = input("Enter title:")
        author = input("Enter author:")
        LibDatabase.libDb.remove_book(title, author)
        Librarian.menu(self)
           
    def addFine(self):
        '''This method automatically impose fine to all users if currentDate > dueDate'''
        try:
            bol = LibDatabase.libDb.fine()
            if bol is False:
                print('\nNo fine imposed\n')
            print('1. Main Menu')
            choice = int(input('Enter your choice:'))
            if choice == 1:
                Librarian.menu(self)
        except ValueError:
            print('Please enter valid choice\n')
            Librarian.menu(self)
        except Exception as e:
            print(e)
    
    def getReport(self):
        '''This method allow the librarian to view the report like which user borrowed which book and dates'''
        try:
            print("""What do you want to see
                  1. Student Report
                  2. Staff Report""")
            choice = int(input("Enter your choice:"))
            if choice == 1:
                table = "student" 
            elif choice == 2:
                table = "staff"
            LibDatabase.libDb.showReport(table)
            print('\n1. Main Menu')
            choice = int(input('Enter your choice:'))
            if choice == 1:
                Librarian.menu(self)
        except ValueError:
            print('Please enter valid choice\n')
            Librarian.menu(self)
        except Exception as e:
            print(e)
            
    def logout():
        libManSystem.LibManSystem.homepage()
