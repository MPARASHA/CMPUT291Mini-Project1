import sqlite3
import time
import hashlib
from os import system, name 
import getpass

connection = None
cursor = None
LoggedUser = None
LoggedUserName = None

def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()
    return

def define_tables():
    global connection, cursor
    
    tables =  open("/home/manzi/Desktop/CMPUT291Mini-Project1/prj-tables.sql","r")
    contents = tables.read()
    
    cursor.executescript(contents)
    connection.commit()

    return

def insert_data():
    global connection, cursor
    
    # TODO fill in test data
    datafile = open("/home/manzi/Desktop/CMPUT291Mini-Project1/test_data.sql","r")
    contents = datafile.read()
    cursor.executescript(contents)
    connection.commit()
    return

def ListProducts():
    global connection, cursor, LoggedUser, LoggedUserName
    cursor.execute(''' SELECT pid, descr''')

def SearchSales():
    global connection, cursor, LoggedUser, LoggedUserName
    pass

def PostSale():
    global connection, cursor, LoggedUser, LoggedUserName
    pass

def SearchUser():
    global connection, cursor, LoggedUser, LoggedUserName
    pass

def systemFunctionalities():
    global connection, cursor, LoggedUser, LoggedUserName
    clear()
    while(True):
        userchoice = input("Welcome %s, Select one of the following options:\n 1) Log Out \n 2) List Products \n 3) Search for sales \n 4) Post a Sale \n 5) Search for Users   " % LoggedUserName)
        if(userchoice ==  '1'):
            LoggedUser =  None
            LoggedUserName = None
            return
        elif(userchoice ==  '2'):
            ListProducts()
        elif(userchoice == '3'):
            SearchSales()
        elif(userchoice == '4'):
            PostSale()
        elif(userchoice == '5'):
            SearchUser()
        else:
            print("\nInvalid Input\n")

def Login():
    global connection, cursor, LoggedUser, LoggedUserName
    clear()
    while(True):
        email = input("Enter email: ")
        pwd = getpass.getpass("Enter Password: ")

        cursor.execute("SELECT email,pwd FROM users WHERE email = :uemail AND pwd = :upwd;",{"uemail": email, "upwd": pwd})
        rows = cursor.fetchall()
        connection.commit()

        if(not rows):
            print("Email or Password Invalid\n")
        else:
            LoggedUser = email
            LoggedUserName = name
            systemFunctionalities()
            return

def Register():
    global connection, cursor, LoggedUser, LoggedUserName
    clear()
    while(True):
        email = input("Enter email: ")
       

        cursor.execute("SELECT email, pwd FROM users WHERE email = :uemail;",{"uemail": email})
        rows = cursor.fetchall()
        connection.commit()

        if(rows):
            print("User already exists\n")
        else:

            pwd = getpass.getpass("Enter Password: ")
            name = input("Enter Name: ")
            city =  input("Enter City: ")
            gender = input("Enter gender(M/F): ")

            cursor.execute("INSERT INTO users VALUES (:uemail, :uname, :upwd, :ucity, :ugender); ", {"uemail": email, "uname": name, "upwd": pwd, "ucity": city, "ugender": gender })
            
            connection.commit()
            LoggedUser =  email
            LoggedUserName = name

            systemFunctionalities()
            return


    
def UI():
    clear()
    while(True):
        userchoice = input("Welcome, please select one of the following options:\n1) Enter 1 to Login\n2) Enter 2 to Register\n3) Enter 3 to exit the program  ")
        if(userchoice == '1'):
            Login()
            clear()
            
        elif(userchoice == '2'):
            Register()
            clear()

        elif(userchoice == '3'):
            return

        else:
            print('Invalid Choice\n\n')
    
def main():
    global connection, cursor

    path="./project1.db"
    connect(path)

    define_tables()
    insert_data()
    UI()

    connection.commit()
    connection.close()
    return

if __name__ == "__main__":
    main()