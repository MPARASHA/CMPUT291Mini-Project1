

import sqlite3
import re

global printedQuery;
global selectedSale;
global database;


def printQuery(rows):
	print("getting print");
	#rows = toPrint.fetchall();
	print(rows);

def Question2():
	global printedQuery;
	global database;
	print("hi I am here");
	stringToMatch = 'xbox';
	database = sqlite3.connect('./database.db');
	databaseCursor = database.cursor();
	databaseCursor.execute("SELECT s.sid from sales as s, products as p where s.descr = :stringToMatch or (s.pid = p.pid and p.descr = :stringToMatch)", {"stringToMatch":
			stringToMatch});
	rows = databaseCursor.fetchall();
	printQuery(rows);


def print2and(query1):
	print("sdsd");

def printInputForSale():
	print("Please select from the following option");
	print("To bid, type bid xxx for example bid 100");
	print("To list all active sales for the seller type sales");
	print("To list all the reivew for seller type reivews");

def makeBid(bidAmount):
	print("in bids")
	global selectedSale;
	databaseCursor = database.cursor();
	print("40")
	queryInput = "SELECT * from bids where sid = ?;"
	listSaleQuery = databaseCursor.execute("queryInput", selectedSale[0]);
	print("43");
	listSaleQuery = listSaleQuery.fetchall();
	print("come here");
	for x in listSaleQuery:
		if x[4] >= bidAmount:
			cFlag = True;
			break;
	if (cFlag):
		print("Bid amount less than maximum");
		inputForSale();
	else:
		x = 0;
		while (True):
			queryInput = "SELECT count(1) from bids where bid = ?;"
			listSaleQuery = databaseCursor.execute(queryInput, chr(x));
			listSaleQuery = listSaleQuery.fetchone();
			if (listSaleQuery[0] == 0):
				#insert into
				insert = "INSERT INTO bids VALUES (?, ?, ?,?,?)"
				listInsert = (chr(x), "place", selectedSale[0], bidAmount);
				databaseCursor.execute(insert, listInsert);
				break;
			else:
				x += 1;






def listSales():
	global selectedSale;
	databaseCursor = database.cursor();
	queryInput = "SELECT * from sales where lister = ?;"
	listSaleQuery = databaseCursor.execute(queryInput, selectedSale[1]);
	listSaleQuery = listSaleQuery.fetchall();
	printQuery(listSaleQuery);



def listReivews():
	global selectedSale;
	databaseCursor = database.cursor();
	queryInput = "SELECT * from reivews where reviewee = ?;"
	listSaleQuery = databaseCursor.execute(queryInput, selectedSale[1]);
	listSaleQuery = listSaleQuery.fetchall();
	printQuery(listSaleQuery);





def inputForSale():
	printInputForSale();
	inputCommand = input("Please enter the command: ").split();
	inputCommand[0].lower();
	try:
		if inputCommand[0] == "bid":
			makeBid(float(inputCommand[1]));
		elif inputCommand[0] == "sales":
			listSales();
		elif inputCommand[0] == "reivews":
			listReivews();
		else:
			print("Error please try again:");
			inputForSale();
	except:
		print("Error please try again: bad one");
		inputForSale();

def selectSale(index):
	global printedQuery;
	global selectedSale;
	
	for x in range(index):
		selectedSale = printedQuery.fetchone();
	inputForSale();

def start():
	theInput = input("Please enter a command: ").split();
	#theInput.split(" ");
	print(theInput[0]);
	if (theInput[0] == "option"):
		try:
			index = int(theInput[1]);
		except:
			start();
		selectSale (index);
		print("whats uo");



if __name__ == '__main__':
	
	#one = "insert into sales values ('S01', 'ibev@gmail.com', 'G01', '2020-02-01', 'xbox', 'Brand new', 50);"
	#two = "insert into sales values ('S02', 'ibev@gmail.com', 'M02', '2020-02-01', 'xbox', 'Brand new', 5);"
	#database = sqlite3.connect('./database.db');
	#databaseCursor = database.cursor();
	#databaseCursor.execute(one);
	#database.commit();

	Question2();
	start();



