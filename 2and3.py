import sqlite3


global printedQuery
global selectedSale
global database


def sortSecond(val):
    return val[1]


def printQuery(rows, sorting):

    sorting.sort(key=sortSecond, reverse=True)
    for x in sorting:
        print(rows[x[0]])

def count_occurrences(word, sentence):
    return sentence.lower().split().count(word)


def Question2(stringToMatch):
    global printedQuery
    global database

    database = sqlite3.connect("database.db")
    databaseCursor = database.cursor()
    queryInput = """SELECT * from sales left join products on sales.pid = products.pid"""
    databaseCursor.execute(queryInput)
    queries = databaseCursor.fetchall()
    printedQuery = []
    for query in queries:
        if (stringToMatch in query[4]) or (stringToMatch in query[8]):
            printedQuery.append(query)
    index = 0
    sorting = []
    for x in printedQuery:
        index += 1
        if x[4] == None:
            count = count_occurrences(stringToMatch, x[8])
            sorting.append((index - 1, count))
        elif x[8] == None:
            count = count_occurrences(stringToMatch, x[4])
            sorting.append((index - 1, count))
        else:
            count = count_occurrences(stringToMatch, x[4] + " " + x[8])
            sorting.append((index - 1, count))
        print(count)

    printQuery(printedQuery, sorting)


def printInputForSale():
    print("Please select from the following option")
    print("To bid, type bid xxx for example bid 100")
    print("To list all active sales for the seller type sales")
    print("To list all the reivew for seller type reivews")


def makeBid(bidAmount):

    global selectedSale
    databaseCursor = database.cursor()

    queryInput = "SELECT * from bids where sid LIKE :num;"
    databaseCursor.execute(queryInput, {"num": selectedSale[0]})
    print(selectedSale)
    listSaleQuery = databaseCursor.fetchall()

    cFlag = False
    for x in listSaleQuery:
        if x[4] >= bidAmount:
            cFlag = True
            break
    if (cFlag):
        print("Bid amount less than maximum")
        inputForSale()
    else:
        x = 100
        while True:
            queryInput = "SELECT count(1) from bids where bid = ?;"
            listSaleQuery = databaseCursor.execute(queryInput, chr(x))
            listSaleQuery = listSaleQuery.fetchone()
            if listSaleQuery[0] == 0:
                # insert into
                insert = "INSERT INTO bids VALUES (?, ?, ?,?,?);"
                listInsert = (chr(x), "place", selectedSale[0], 1584576000000, bidAmount)
                databaseCursor.execute(insert, listInsert)
                database.commit()
                break
            else:
                x += 1


def listSales():
    global selectedSale
    databaseCursor = database.cursor()
    queryInput = "SELECT * from sales where lister = :num;"
    listSaleQuery = databaseCursor.execute(queryInput, {"num":selectedSale[1]})
    listSaleQuery = listSaleQuery.fetchall()
    for x in listSaleQuery:
        print(x)


def listReivews():
    global selectedSale
    databaseCursor = database.cursor()
    queryInput = "SELECT * from reviews where reviewee = :num;"
    listSaleQuery = databaseCursor.execute(queryInput, {"num":selectedSale[1]})
    listSaleQuery = listSaleQuery.fetchall()
    for x in listSaleQuery:
        print(x)



def inputForSale():
    printInputForSale()
    inputCommand = input("Please enter the command: ").split()
    inputCommand[0].lower()

    if inputCommand[0] == "bid":
        makeBid(float(inputCommand[1]))
    elif inputCommand[0] == "sales":
        listSales()
    elif inputCommand[0] == "reviews":
        listReivews()
    else:
        print("Error please try again:")
        inputForSale()



def selectSale(index):
    global printedQuery
    global selectedSale
    if index > len(printedQuery):
        return
    for x in range(index):
        selectedSale = printedQuery[x]
    inputForSale()


def question3():
    theInput = input("To select a sale please type option ### (ex. option 2): ").split()

    print(theInput[0])
    if (theInput[0] == "option"):
        try:
            index = int(theInput[1])
        except:
            question3()
        selectSale(index)


if __name__ == '__main__':

    inputs = input("Enter the description of the sale you want to see (for now please type xbox): ").lower()
    Question2(inputs)
    question3()
