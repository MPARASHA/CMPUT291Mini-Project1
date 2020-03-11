

import sqlite3
import datetime

def post_sale(product_Id, datetime_obj, sale_description, sale_condition, sale_res_price):
    database = sqlite3.connect("database.db")
    databaseCursor = database.cursor()
    x = 100
    while True:
        queryInput = "SELECT count(1) from sales where sid = ?;"
        listSaleQuery = databaseCursor.execute(queryInput, chr(x))
        listSaleQuery = listSaleQuery.fetchone()
        if listSaleQuery[0] == 0:
            # insert into
            insert = "INSERT INTO sales VALUES (?, ?, ?,?,?,?,?);"
            #cgange it with the current user

            listInsert = (chr(x), "USER", product_Id, datetime_obj.date(), sale_description, sale_condition, sale_res_price)
            databaseCursor.execute(insert, listInsert)
            database.commit()
            break
        else:
            x += 1




def prompt_user():
    product_Id = input("Enter product ID: ")
    sale_end_date = ''
    sale_end_time = ''
    sale_description = ''
    sale_condition = ''
    while sale_end_date == '':
        sale_end_date = input("Enter end date YYYY/MM/DD: ")
        format_str = '%Y/%m/%d'  # The format
        datetime_obj = datetime.datetime.strptime(sale_end_date, format_str)

    while sale_description == '':
        sale_description = input("Enter sale description: ")

    while sale_condition == '':
        sale_condition = input("Enter sale condition: ")

    sale_res_price = input("Enter the reserved price: ")

    post_sale(product_Id, datetime_obj, sale_description, sale_condition, sale_res_price)










if __name__ == '__main__':
    print("hello")
    inputs = input("blsdsda: ")
    if inputs == "":
        print("it works")
    prompt_user()