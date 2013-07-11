#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as mdb
import sys
from dbconfig import *

con = object()

def queryDB( str ):
    try:
        con = mdb.connect(host, user, passw, db)
        cur = con.cursor()
        cur.execute(str)
        returnedResults = cur.fetchall()
        return returnedResults
            
    except mdb.Error, e:
        return "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
        
    finally:    
        if con:    
            con.close()
            
def queryDBSingleResponse( str ):
    try:
        con = mdb.connect(host, user, passw, db)
        cur = con.cursor()
        cur.execute(str)
        returnedResults = cur.fetchone()
        return returnedResults
            
    except mdb.Error, e:
        return "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
        
    finally:    
        if con:    
            con.close()


def writeDB ( str ):
    con = mdb.connect(host, user, passw, db)
    cur = con.cursor()
    try:
       cur.execute( str )
       con.commit()
    except:
       con.rollback()
    con.close()
