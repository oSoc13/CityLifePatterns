#!/usr/bin/python
# -*- coding: utf-8 -*-
import functions
########################################


countedSpotsArray = functions.getAllCountedSpots()
functions.clearNextSpotsTable()

for spot in countedSpotsArray:
    spotArray = functions.getNextSpots( spot )
    
    requiredZeros = 6 - len(spotArray)
    while (requiredZeros > 0):
        spotArray.append(0)
        requiredZeros -= 1

    functions.repopulateNextSpotList( spotArray )

