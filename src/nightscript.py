#!/usr/bin/python
#
# This is the night script that is responsible for building the database.
#
# Takes 1 argument to specify in which mode to run:
#
#   1) 'rebuild': Rebuild the database from scratch. This will
#       - truncate the 'whatsnext' table in the 'vikingpatterns' database
#       - rebuild it using all checkins since 2012-03-13 04:00:00
#
#       Rebuilding mimicks the update mode in that it processes checkins per day.
#
#   2) 'update': Update the database with checkins since the last run. This will
#       - Update it using all checkins since the date specified in file 'lastrun'
#
# NOTES:
#   - All dates are expected to be in this format: %Y-%m-%d %H:%M:%S, with leading zeros!
#   - The file 'lastrun' is expected to be in same directory as this file.
#   - 'lastrun' file should only contain (without quotes): "Night script was last run on: 2012-03-17 04:00:00",
#     with the date specified when it was last run. This will be updated each time the script runs in update mode.
#   - Output generated in 'rebuild' mode can be controlled in file
#     modules/DatabaseBuilder.py in function 'buildFromScratch()'
#
# Currently, the MySQL database looks like this:
#
#   Database: vikingpatterns
#   table: whatsnext
#    +--------------------+-------------+------+-----+---------+----------------+
#   | Field              | Type        | Null | Key | Default | Extra          |
#   +--------------------+-------------+------+-----+---------+----------------+
#   | id                 | bigint(20)  | NO   | PRI | NULL    | auto_increment |
#   | spotId             | int(11)     | NO   |     | NULL    |                |
#   | nextSpotId         | int(11)     | NO   |     | NULL    |                |
#   | totalCount         | bigint(20)  | NO   |     | NULL    |                |
#   | spotCreationDate   | varchar(25) | NO   |     | NULL    |                |
#   | lastOccurrence     | varchar(25) | NO   |     | NULL    |                |
#   | variance           | bigint(20)  | NO   |     | NULL    |                |
#   | averageTimeSpent   | bigint(20)  | NO   |     | NULL    |                |
#   | MspotAge           | float       | NO   |     | NULL    |                |
#   | MtimeSpent         | float       | NO   |     | NULL    |                |
#   | weightedPopularity | float       | NO   |     | NULL    |                |
#   +--------------------+-------------+------+-----+---------+----------------+
#
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
#
###################################
import sys
sys.path.insert(0, './modules')
import DatabaseBuilder
from DatabaseBuilder import *
import os.path
###################################

baseDir = os.path.dirname(os.path.abspath(__file__))
dbBuilder = DatabaseBuilder()

args = sys.argv
nrArgs = len(args)

if nrArgs > 1:
    dbBuilder = DatabaseBuilder()
    if args[1] == 'rebuild':
        print 'You are about to truncate the entire database, continue? Y/N'
        char = sys.stdin.read(1)
        if char == 'Y':
            dbBuilder.buildFromScratch()
        if char == 'N':
            print 'Terminating...'
    if args[1] == 'update':
        dbBuilder.updateSinceLastRun(baseDir)
else:
    print 'No arguments given. Usage:'
    print 'python nightscript.py rebuild (rebuilds database from scratch)'
    print 'python nightscript.py update  (adds checkins since last run specified in \'lastrun\' file)'



