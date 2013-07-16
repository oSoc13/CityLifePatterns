#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as mdb
import sys
from dbconfig import *

con = object()
cur = object()

def openConnection():
    global con 
    con = mdb.connect(host, user, passw, db)


def closeConnection():
    con.close()

def queryDB( str ):
    global con
    try:
        cur = con.cursor()
        cur.execute(str)
        returnedResults = cur.fetchall()
        return returnedResults
            
    except mdb.Error, e:
        return "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
        
            
def queryDBSingleResponse( str ):
    global con
    try:
        cur = con.cursor()
        cur.execute(str)
        returnedResults = cur.fetchone()
        return returnedResults
            
    except mdb.Error, e:
        return "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

def writeDB ( str ):
    global con
    try:
       cur = con.cursor()
       cur.execute( str )
       con.commit()
    except:
       con.rollback()
