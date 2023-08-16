import discord
import mysql.connector
from mysql.connector import errorcode
import asyncio
from discord.ext import commands # import commands

mydb = mysql.connector.connect(
    host = "localhost" ,
    user = "root",
    password = "P3nguinsrule!2",
    database = "timbot",
    auth_plugin = "mysql_native_password"
)

cursor = mydb.cursor()


        
def addColumn(table_name: str, column_name: str, datatype: str): # adds a column to specified table
    print("ALTER TABLE " + str(table_name) + "ADD " + str(column_name) + " " + str(datatype) + " DEFAULT 0")
    cursor.execute("ALTER TABLE " + str(table_name) + " ADD " + str(column_name) + " " + str(datatype))

def delColumn(table_name: str, column_name: str): # deletes a column from specified table
    print("ALTER TABLE " + str(table_name) + " DROP " + str(column_name))
    cursor.execute("ALTER TABLE " + str(table_name) + " DROP " + str(column_name))

def getValue(table_name: str, column_name: str, user_id: int)-> int:
    cursor.execute("SELECT " + column_name + " FROM " + table_name + " WHERE client_id =" + str(user_id))
    result = cursor.fetchall() # gets the list [(int,)] from db
    
    if len(result) == 0: # if the value is NULL, the client has no data
        #print(str(user_id) + " has 0 " + column_name)
        insertIntoTable(table_name, column_name, user_id, 0) # add the user to whatever table you are checking
        return 0    
    elif result[0][0] == None: # if the value is None, the client has no data
        #print(str(user_id) + " has 0 " + column_name)
        #insertIntoTable(table_name, column_name, user_id, 0) # add the user to whatever table you are checking
        return 0
    else: # if the value exists
        #print(str(user_id) + " has " + str(result[0][0]) + " " + column_name)
        return(result[0][0]) # returns the int value stored in db
    
    
    
def insertIntoTable(table_name: str, column_name: str, user_id: int, value: int):
    
    # finds the column and value of the table
    cursor.execute("SELECT " + column_name + " FROM " + table_name + " WHERE client_id = " + str(user_id))
    result = cursor.fetchall()

    if len(result) == 0: # if the user is not in the database
        print("Adding " + str(user_id) + " to database..")
        cursor.execute("INSERT INTO " + table_name + "(client_id," + column_name + ")" + " VALUES(" + str(user_id) + "," + str(value) + ")")
        mydb.commit()
    else: # if the user is in the database
        print("Updating " + str(user_id) + "..")
        cursor.execute("UPDATE " + table_name + " SET " + column_name + "= " + str(value) + " WHERE client_id = " + str(user_id))
        mydb.commit()
    
def generateCrumbs(user_id: int,amount: int)-> None: # adds crumbs to users
    newAmount = getValue('user_crumbs', 'crumbs', user_id) + amount
    insertIntoTable('user_crumbs', 'crumbs', user_id, newAmount)

def subtractCrumbs(user_id: int, amount: int) -> None: # removes crumbs from users
    newAmount = getValue('user_crumbs', 'crumbs', user_id) - amount
    insertIntoTable('user_crumbs', 'crumbs', user_id, newAmount)
           

def wordleStreak(user_id: int, win: bool)-> None: # if win is True, add to wordlestreak
    cursor = mydb.cursor()
    cursor.execute("SELECT streak FROM wordle_streak WHERE client_id = " + str(user_id))
    result = cursor.fetchall()
    newStreak = getValue('wordle_streak', 'streak', user_id) + 1
    if win == True: # if player won
        insertIntoTable('wordle_streak', 'streak', user_id, newStreak)
    else:
        insertIntoTable('wordle_streak', 'streak', user_id, 0)



