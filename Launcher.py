import sqlite3
import time
import hashlib
from os import system, name 
import getpass
import re
import traceback
import random
import string


connection = None
cursor = None
LoggedUser = None
LoggedUserName = None

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

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

def saleFunctions(sale):
    global connection, cursor, LoggedUser, LoggedUserName
    clear()
    cursor.execute('''  SELECT s.lister, s.descr, s.edate, s.cond, MAX(b.amount), COUNT(r.reviewee) AS Num_Rev, AVG(r.rating)
                        FROM sales s, bids b, reviews r
                        WHERE b.sid = s.sid AND s.lister = r.reviewee AND lower(s.sid) = :usale
                        GROUP BY s.lister, s.descr, s.edate, s.cond
                        
                        UNION

                        SELECT s.lister, s.descr, s.edate, s.cond, s.rprice, COUNT(r.reviewee), AVG(r.rating)
                        FROM sales s, bids b, reviews r
                        WHERE lower(s.sid) = :usale AND b.sid = s.sid AND s.lister = r.reviewee AND s.sid NOT IN (SELECT b.sid FROM bids b)
                        GROUP BY s.lister, s.descr, s.edate, s.cond;
                        
                        ''', {"usale":sale})
    rows = cursor.fetchall()
    print("SALE DESCRIPTION:\n")
    # Print the table
    print()
    print()

    print("   ", end = "")
    for key in rows[0].keys():
        print(key, end = "\t\t")

    print()

    for i in range(1, len(rows) + 1):
        print(str(i) + ") " , end = "")
        for item in rows[i-1]:
            print(item, end = "\t\t")
        print()

    print()
    print()

    print("PRODUCT DESCRIPTION:\n")

    cursor.execute('''  SELECT p.pid, p.descr, COUNT(DISTINCT pr.rid) AS Num_Rev, AVG(pr.rating)
                        FROM products p,  previews pr, sales s
                        WHERE pr.pid = p.pid AND s.pid = p.pid AND s.sid = :usale
                        GROUP BY p.pid, p.descr;
                        ''',{"usale":sale})

    rows = cursor.fetchall()
    
    if(not(rows)):
        print("Product hasn't been reviewed yet!\n")
    else:
        # Print the table
        print()
        print()

        print("   ", end = "")
        for key in rows[0].keys():
            print(key, end = "\t\t")

        print()

        for i in range(1, len(rows) + 1):
            print(str(i) + ") " , end = "")
            for item in rows[i-1]:
                print(item, end = "\t\t")
            print()

        print()
        print()

    uchoice = input("Please select one of the following options:\n 1) Place a bid \n 2) List Sales of Seller \n 3) List all reviews of the seller \n 4) Go back ")
    if(uchoice == '4'):
        return
    elif(uchoice == '1'):
        cursor.execute("SELECT MAX(amount) FROM bids WHERE sid = :usale;", {"usale":sale})
        row = cursor.fetchone()
        print(row[0])
        while(True):
            amount = input("Enter bid ammount: ")
            try:
                amount = float(amount)
            except ValueError:
                print("Invalid Input!")
                continue

            if(amount > row[0]):
                break
            else:
                print("Bid amount can't be less than the current maximum bid!\n")
            
        while(True):
            bid = randomString(20)
            cursor.execute("SELECT bid FROM bids WHERE bid = :ubid;", {"ubid": bid})
            rows = cursor.fetchall()

            if(not(rows)):
                cursor.execute("INSERT INTO bids VALUES (:ubid, :ubidder, :usid, datetime('now'), :uamount);", {"ubid": bid, "ubidder": LoggedUser, "usid": sale, "uamount":amount})
                connection.commit()
                break
            else:
                continue

    elif(uchoice == '2'):
        cursor.execute("SELECT lister FROM sales WHERE sid = :usale;",{"usale": sale})
        row = cursor.fetchone()
        lister = row[0]

        cursor.execute('''  SELECT  s.sid, s.descr, MAX(b.amount), cast((julianday(s.edate)-julianday('now')) as int) AS Days, cast(((julianday(s.edate)-julianday('now')) * 24 - cast((julianday(s.edate)-julianday('now')) as int) *24) as int) AS Hours, cast(( ((julianday(s.edate)-julianday('now'))*1440) - (cast((julianday(s.edate)-julianday('now')) as int)*1440) - (cast(((julianday(s.edate)-julianday('now')) * 24 - cast((julianday(s.edate)-julianday('now')) as int) *24) as int) * 60) ) as int) AS Minutes
                                FROM sales s, bids b
                                WHERE s.lister = :ulister AND s.sid = b.sid AND s.edate > datetime('now') 
                                GROUP BY s.sid, s.descr
                                

                                UNION

                                SELECT s.sid, s.descr, s.rprice, cast((julianday(s.edate)-julianday('now')) as int) AS Days, cast(((julianday(s.edate)-julianday('now')) * 24 - cast((julianday(s.edate)-julianday('now')) as int) *24) as int) AS Hours, cast(( ((julianday(s.edate)-julianday('now'))*1440) - (cast((julianday(s.edate)-julianday('now')) as int)*1440) - (cast(((julianday(s.edate)-julianday('now')) * 24 - cast((julianday(s.edate)-julianday('now')) as int) *24) as int) * 60) ) as int) AS Minutes
                                FROM sales s
                                WHERE s.lister = :ulister AND s.sid NOT IN (SELECT b.sid FROM bids b)
                                GROUP BY s.sid, s.descr

                                ORDER BY Days, Hours, Minutes;
                                 ''',{"ulister":lister})
        rows = cursor.fetchall()

          

        # Print the table
        print()
        print()

        print("   ", end = "")
        for key in rows[0].keys():
            print(key, end = "\t\t")

        print()

        for i in range(1, len(rows) + 1):
            print(str(i) + ") " , end = "")
            for item in rows[i-1]:
                print(item, end = "\t\t")
            print()

        print()
        print()
        while(True):
            uchoice = input("Select a Sale or enter 'b' to go back... ")

            if(uchoice == 'b' or uchoice == 'B'):
                break
            try:
                uchoice = int(uchoice)
            except ValueError:
                print("Not a number!")
                continue
            if(uchoice > 0 and uchoice < len(rows) + 1):
                selectedSale = rows[uchoice - 1][0]
                saleFunctions(selectedSale)
            else:
                print("\nInvalid Response!\n")

    elif(uchoice == '3'):
        cursor.execute("SELECT lister FROM sales WHERE sid = :usale;",{"usale": sale})
        row = cursor.fetchone()
        lister = row[0]
        cursor.execute("SELECT * FROM reviews WHERE reviewee = :ulister; ", {"ulister": lister})

        rows = cursor.fetchall()

        # Print the table
        print()
        print()

        print("   ", end = "")
        for key in rows[0].keys():
            print(key, end = "\t\t")

        print()

        for i in range(1, len(rows) + 1):
            print(str(i) + ") " , end = "")
            for item in rows[i-1]:
                print(item, end = "\t\t")
            print()

        print()
        print()




def ListProductsMoreFeatures(pid, productName):
    global connection, cursor, LoggedUser, LoggedUserName
    while(True):
        clear()
        userchoice = input(" Product Selected: %s\n Select one of the following options:\n 1) Write a review for this product \n 2) List all reviews for this product \n 3) List all active sales associated to this product\n 4) Go back to Product Listing " % productName)
        if(userchoice == '1'):
            while(True):
                reviewText = input("\nType a review: \n")
                if(reviewText == ""):
                    print("Review Can't be empty!")
                    continue
                else:
                    break

            while(True):
                rating = input("Enter a rating from 1 to 5 inclusive: ")
                try:
                    rating = float(rating)
                except ValueError:
                    print("\nThat's not a number!\n")
                    continue
                if(rating < 1 or rating >5):
                    print("Invalid Rating!")
                    continue
                else:
                    break

            cursor.execute("SELECT MAX(rid) FROM previews;")
            row = cursor.fetchone()
            rid = None

            while(True):
                rid = row[0] + 1
                cursor.execute("SELECT rid FROM previews WHERE rid = :urid;", {"urid": rid})
                rows = cursor.fetchall()

                if(not(rows)):
                    break
                else:
                    continue
            
            cursor.execute("INSERT INTO previews VALUES (:urid, :upid, :ureviewer, :urating, :urtext, datetime('now'));", {"urid": rid, "upid": pid, "ureviewer": LoggedUser, "urating": rating, "urtext": reviewText})    
            connection.commit()
            

            
        elif(userchoice == '2'):
            pid = pid.lower()
            cursor.execute("SELECT rid, reviewer, rtext, rdate FROM previews WHERE lower(pid) = :upid;", {"upid": pid})
            rows = cursor.fetchall()

            # Print the table
            print()
            print()

            
            print("   ", end = "")
            for key in rows[0].keys():
                print(key, end = "\t\t")

            print()

            for i in range(1, len(rows) + 1):
                print(str(i) + ") " , end = "")
                for item in rows[i-1]:
                    print(item, end = "\t\t")
                print()

            print()
            print()

            a = input("Press 'Enter' to go back...")

            if(a):
                pass


        elif(userchoice == '3'):
            pid = pid.lower()
            cursor.execute('''  SELECT  s.sid, s.descr, MAX(b.amount), cast((julianday(s.edate)-julianday('now')) as int) AS Days, cast(((julianday(s.edate)-julianday('now')) * 24 - cast((julianday(s.edate)-julianday('now')) as int) *24) as int) AS Hours, cast(( ((julianday(s.edate)-julianday('now'))*1440) - (cast((julianday(s.edate)-julianday('now')) as int)*1440) - (cast(((julianday(s.edate)-julianday('now')) * 24 - cast((julianday(s.edate)-julianday('now')) as int) *24) as int) * 60) ) as int) AS Minutes
                                FROM sales s, bids b
                                WHERE lower(s.pid) = :pid AND s.sid = b.sid AND s.edate > datetime('now') 
                                GROUP BY s.sid, s.descr
                                

                                UNION

                                SELECT s.sid, s.descr, s.rprice, cast((julianday(s.edate)-julianday('now')) as int) AS Days, cast(((julianday(s.edate)-julianday('now')) * 24 - cast((julianday(s.edate)-julianday('now')) as int) *24) as int) AS Hours, cast(( ((julianday(s.edate)-julianday('now'))*1440) - (cast((julianday(s.edate)-julianday('now')) as int)*1440) - (cast(((julianday(s.edate)-julianday('now')) * 24 - cast((julianday(s.edate)-julianday('now')) as int) *24) as int) * 60) ) as int) AS Minutes
                                FROM sales s
                                WHERE lower(s.pid) = :pid AND s.sid NOT IN (SELECT b.sid FROM bids b)
                                GROUP BY s.sid, s.descr

                                ORDER BY Days, Hours, Minutes;
                                 ''',{"pid":pid})

            rows = cursor.fetchall()

          

            # Print the table
            print()
            print()

            
            print("   ", end = "")
            for key in rows[0].keys():
                print(key, end = "\t\t")

            print()

            for i in range(1, len(rows) + 1):
                print(str(i) + ") " , end = "")
                for item in rows[i-1]:
                    print(item, end = "\t\t")
                print()

            print()
            print()
            while(True):
                uchoice = input("Select a Sale or enter 'b' to go back... ")

                if(uchoice == 'b' or uchoice == 'B'):
                    return
                try:
                    uchoice = int(uchoice)
                except ValueError:
                    print("Not a number!")
                    continue
                if(uchoice > 0 and uchoice < len(rows) + 1):
                    selectedSale = rows[uchoice - 1][0]
                    saleFunctions(selectedSale)


        elif(userchoice == '4'):
            return
        else:
            print("Invalid Input!")
            

def ListProducts():
    global connection, cursor, LoggedUser, LoggedUserName

    # Needed to get column names
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(''' SELECT p.pid AS PID, p.descr AS DESCR, COUNT(DISTINCT rid) AS NumREV, AVG(rating) AS AVG_RAT, COUNT(DISTINCT sid)AS NUM_SALES
                       FROM products p, sales s, previews pr
                       WHERE p.pid = s.pid AND edate > datetime('now')
                       GROUP BY p.pid, p.descr
                       ORDER BY COUNT(sid) DESC; ''')

    rows = cursor.fetchall()
    

    while(True):
        clear()
        # Print the table
        print()
        print()

        
        print("   ", end = "")
        for key in rows[0].keys():
            print(key, end = "\t\t")

        print()

        for i in range(1, len(rows) + 1):
            print(str(i) + ") " , end = "")
            for item in rows[i-1]:
                print(item, end = "\t\t")
            print()

        print()
        print()
        userchoice = input("Enter a number from the table above to select the respected product or Enter 'b' to go back:  ")
        if(userchoice == 'b' or userchoice == 'B'):
            return
        try:
            userchoice = int(userchoice)
        except ValueError:
            print("\nThat's not an int!\n")
            continue
        if(userchoice > 0 and userchoice < len(rows) + 1):
            ListProductsMoreFeatures(rows[userchoice - 1][0], rows[userchoice - 1][1])
        else:
            print("\nInvalid Choice!\n")


def SearchSales():
    global connection, cursor, LoggedUser, LoggedUserName
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    clear()
    saleOrder = {}
    keywords = []
    userchoice =  input("Enter keywords separated by one space each OR enter 'b' to go back... ")

    if(userchoice == 'b' or userchoice == 'B'):
        return
    else:
        keywords = userchoice.split(" ")


    for word in keywords:
       # print("hi")
        wordl = word.lower()
        wordl = "%"+wordl+"%"
        cursor.execute("SELECT DISTINCT s.sid FROM sales s, products p WHERE lower(s.descr) LIKE :uword OR (lower(p.descr) LIKE :uword AND s.pid = p.pid);",{"uword": wordl} )
        rows = cursor.fetchall()
        
            
        for row in rows:
            if row[0] in saleOrder:
                saleOrder[row[0]] += 1
            else:
                saleOrder[row[0]] = 1

    sortedSales = sorted(saleOrder.items(), key = lambda x: x[1], reverse = True)
    print(sortedSales)
    rows = []
    for s in sortedSales:
        cursor.execute('''      SELECT  s.sid, s.descr, MAX(b.amount), cast((julianday(s.edate)-julianday('now')) as int) AS Days, cast(((julianday(s.edate)-julianday('now')) * 24 - cast((julianday(s.edate)-julianday('now')) as int) *24) as int) AS Hours, cast(( ((julianday(s.edate)-julianday('now'))*1440) - (cast((julianday(s.edate)-julianday('now')) as int)*1440) - (cast(((julianday(s.edate)-julianday('now')) * 24 - cast((julianday(s.edate)-julianday('now')) as int) *24) as int) * 60) ) as int) AS Minutes
                                FROM sales s, bids b
                                WHERE s.sid = :usid AND s.sid = b.sid AND s.edate > datetime('now') 
                                GROUP BY s.sid, s.descr
                                

                                UNION

                                SELECT s.sid, s.descr, s.rprice, cast((julianday(s.edate)-julianday('now')) as int) AS Days, cast(((julianday(s.edate)-julianday('now')) * 24 - cast((julianday(s.edate)-julianday('now')) as int) *24) as int) AS Hours, cast(( ((julianday(s.edate)-julianday('now'))*1440) - (cast((julianday(s.edate)-julianday('now')) as int)*1440) - (cast(((julianday(s.edate)-julianday('now')) * 24 - cast((julianday(s.edate)-julianday('now')) as int) *24) as int) * 60) ) as int) AS Minutes
                                FROM sales s
                                WHERE s.sid = :usid AND s.sid NOT IN (SELECT b.sid FROM bids b)
                                GROUP BY s.sid, s.descr

                                ORDER BY Days, Hours, Minutes;
                                 ''',{"usid": s[0]})

        while(True):
            row = cursor.fetchone()
            if(not(row)):
                break
            else:
                rows.append(row)

          

    # Print the table
    print()
    print()

            
    print("   ", end = "")
    for key in rows[0].keys():
        print(key, end = "\t\t")

    print()

    for i in range(1, len(rows) + 1):
        print(str(i) + ") " , end = "")
        for item in rows[i-1]:
            print(item, end = "\t\t")
        print()

    print()
    print()
    while(True):
        uchoice = input("Select a Sale or enter 'b' to go back... ")

        if(uchoice == 'b' or uchoice == 'B'):
            return
        try:
            uchoice = int(uchoice)
        except ValueError:
            print("Not a number!")
            continue
        if(uchoice > 0 and uchoice < len(rows) + 1):
            selectedSale = rows[uchoice - 1][0]
            saleFunctions(selectedSale)


def PostSale():
    global connection, cursor, LoggedUser, LoggedUserName
    clear()

    pid = input("You can press 'b' to go back anytime...\n\nEnter product ID:  ")
    if(pid == 'b' or pid == 'B'):
        return
    
    # New Random Unique SID
    sid = None
    while(True):
        sid = randomString(4)
        cursor.execute("SELECT sid from sales WHERE sid = :usid", {"usid": sid})
        rows = cursor.fetchall()
        if(rows):
            continue
        else:
            break
    salets = None
    while(True):
        salets = input("Enter sale end date and time: ")
        if(salets == 'b' or salets == 'B'):
            return
        cursor.execute("SELECT :usalets > datetime('now')",{"usalets":salets})
        row = cursor.fetchone()
        if(row[0] == 0):
            print("Sale end date can't be in the Past!")
            continue
        else:
            break

    sdescr = input("Enter sale description: ")
    scond = input("Enter sale condition: ")
    srp = input("Enter sale reserve price: ")

    if(pid == ""):
        pid = None
    if(srp == ""):
        srp == None

    cursor.execute("INSERT INTO sales VALUES (:usid, :ulister, :upid, :uedate, :udescr, :ucond, :urp);", {"usid": sid, "ulister":LoggedUser, "upid":pid, "uedate":salets, "udescr": sdescr, "ucond": scond, "urp": srp })
    connection.commit()

def userFunctions(email):
    global connection, cursor, LoggedUser, LoggedUserName
    clear()
    print("Selected User is %s\n" % email)
    while(True):
        uc = input("Please select one of the following options:\n1) Write a review\n2) List all active listings for this user\n3) List all reviews of this user\n4) To go back: \n")
        if(uc == '4'):
            return
        elif(uc == '1'):
            rtext = None
            rating = None

            while(True):
                rtext = input("Enter Your Review: ")
                if(rtext == ""):
                    print("Review can't be blank!\n")
                    continue
                else:
                    break
            while(True):
                    rating = input("Enter a rating from 1 to 5 inclusive: ")
                    try:
                        rating = float(rating)
                    except ValueError:
                        print("\nThat's not a number!\n")
                        continue
                    if(rating < 1 or rating >5):
                        print("Invalid Rating!")
                        continue
                    else:
                        break
            cursor.execute("INSERT INTO reviews VALUES (:urev1, :urev2, :urat, :urtext, datetime('now'));", {"urev1": LoggedUser, "urev2": email, "urat": rating, "urtext": rtext})
            connection.commit()
        
        elif(uc == '2'):
            email = email.lower()
            cursor.execute('''      SELECT  s.sid, s.descr, MAX(b.amount), cast((julianday(s.edate)-julianday('now')) as int) AS Days, cast(((julianday(s.edate)-julianday('now')) * 24 - cast((julianday(s.edate)-julianday('now')) as int) *24) as int) AS Hours, cast(( ((julianday(s.edate)-julianday('now'))*1440) - (cast((julianday(s.edate)-julianday('now')) as int)*1440) - (cast(((julianday(s.edate)-julianday('now')) * 24 - cast((julianday(s.edate)-julianday('now')) as int) *24) as int) * 60) ) as int) AS Minutes
                                    FROM sales s, bids b
                                    WHERE lower(s.lister) = :ulister AND s.sid = b.sid AND s.edate > datetime('now') 
                                    GROUP BY s.sid, s.descr
                                    

                                    UNION

                                    SELECT s.sid, s.descr, s.rprice, cast((julianday(s.edate)-julianday('now')) as int) AS Days, cast(((julianday(s.edate)-julianday('now')) * 24 - cast((julianday(s.edate)-julianday('now')) as int) *24) as int) AS Hours, cast(( ((julianday(s.edate)-julianday('now'))*1440) - (cast((julianday(s.edate)-julianday('now')) as int)*1440) - (cast(((julianday(s.edate)-julianday('now')) * 24 - cast((julianday(s.edate)-julianday('now')) as int) *24) as int) * 60) ) as int) AS Minutes
                                    FROM sales s
                                    WHERE lower(s.lister) = :ulister AND s.sid NOT IN (SELECT b.sid FROM bids b)
                                    GROUP BY s.sid, s.descr

                                    ORDER BY Days, Hours, Minutes;
                                    ''',{"ulister":email})
            rows = cursor.fetchall()

            

            # Print the table
            print()
            print()

            print("   ", end = "")
            for key in rows[0].keys():
                print(key, end = "\t\t")

            print()

            for i in range(1, len(rows) + 1):
                print(str(i) + ") " , end = "")
                for item in rows[i-1]:
                    print(item, end = "\t\t")
                print()

            print()
            print()
            while(True):
                uchoice = input("Select a Sale or enter 'b' to go back... ")

                if(uchoice == 'b' or uchoice == 'B'):
                    break
                try:
                    uchoice = int(uchoice)
                except ValueError:
                    print("Not a number!")
                    continue
                if(uchoice > 0 and uchoice < len(rows) + 1):
                    selectedSale = rows[uchoice - 1][0]
                    saleFunctions(selectedSale)
                else:
                    print("\nInvalid Response!\n")
        
        elif(uc == '3'):
            cursor.execute("SELECT * FROM reviews WHERE reviewee = :ulister; ", {"ulister": email})

            rows = cursor.fetchall()

            # Print the table
            print()
            print()

            print("   ", end = "")
            for key in rows[0].keys():
                print(key, end = "\t\t")

            print()

            for i in range(1, len(rows) + 1):
                print(str(i) + ") " , end = "")
                for item in rows[i-1]:
                    print(item, end = "\t\t")
                print()

            print()
            print()


def SearchUser():
    global connection, cursor, LoggedUser, LoggedUserName
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    clear()
    keyword = input("Enter a keyword for user-search or enter 'b' to go back: ")
    if(keyword == 'b' or keyword == 'B'):
        return
    keyl = keyword.lower()
    keyl = "%"+keyl+"%"

    cursor.execute('''  SELECT email, name, city 
                        FROM users
                        WHERE lower(email) LIKE :kword OR lower(name) LIKE :kword;
    ''', {"kword": keyl})

    rows = cursor.fetchall()

    
    
    while(True):
        # Print the table
        print()
        print()

                
        print("   ", end = "")
        for key in rows[0].keys():
            print(key, end = "\t\t")

        print()

        for i in range(1, len(rows) + 1):
            print(str(i) + ") " , end = "")
            for item in rows[i-1]:
                print(item, end = "\t\t")
            print()

        print()
        print()

        uc = input("Select one of the users or enter 'b' to go back: ")
        if(uc == 'b' or uc == 'B'):
            return
        try:
            uc = int(uc)
        except ValueError:
            print("Invalid Response!")
            continue
        if(uc > 0 and uc < len(rows) + 1):
            selectedUser = rows[uc - 1][0]
            userFunctions(selectedUser)
        else:
            print("\nInvalid Response!\n")
    


def systemFunctionalities():
    global connection, cursor, LoggedUser, LoggedUserName
    clear()
    while(True):
        userchoice = input("Welcome %s, Select one of the following options:\n 1) Log Out \n 2) List Products \n 3) Search for sales \n 4) Post a Sale \n 5) Search for Users   " % LoggedUserName)
        if(userchoice ==  '1'):
            LoggedUser =  None
            LoggedUserName = None
            return
        elif(userchoice == '2'):
            ListProducts()
        elif(userchoice == '3'):
            SearchSales()
        elif(userchoice == '4'):
            PostSale()
        elif(userchoice == '5'):
            SearchUser()
        else:
            print("\nInvalid Input!\n")

def Login():
    global connection, cursor, LoggedUser, LoggedUserName
    clear()
    while(True):
        email = input("Enter email: ")
        email = email.lower()

        # SQL injection checking
        pwd = getpass.getpass("Enter Password: ")
        if(re.match("^[A-Za-z0-9_]*$", pwd)):
            cursor.execute("SELECT email,pwd FROM users WHERE email = :uemail AND pwd = :upwd;",{"uemail": email, "upwd": pwd})
        else:
            print("\nPassword can only contain alphabets, numbers and underscore!\n")
            continue
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
        email = email.lower()

        cursor.execute("SELECT email, pwd FROM users WHERE lower(email) = :uemail;",{"uemail": email})
        rows = cursor.fetchall()   
        connection.commit()

        if(rows):
            print("User already exists!\n")
        else:
            while(True):
                pwd = getpass.getpass("Enter Password: ")
                if(not(re.match("^[A-Za-z0-9_]*$", pwd))):
                    print("\nPassword can only contain alphabets, numbers and underscore!\n")
                    continue
                else:
                    break
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
            print('Invalid Choice!\n\n')
        
    
def main():
    global connection, cursor

    path="./project1.db"
    connect(path)

    # ERROR checking for sqlite
    
    define_tables()
    insert_data()
    UI()

    connection.commit()
    connection.close()
    return

if __name__ == "__main__":
    main()