#!/usr/bin/python
# -*- coding: utf-8 -*-
import functions
########################################


countedSpotsArray = functions.getAllCountedSpots()

for spot in countedSpotsArray:
    spotArray = functions.getNextSpots( spot )
    print spotArray
    
    requiredZeros = 6 - len(spotArray)
    while (requiredZeros > 0):
        spotArray.append(0)
        requiredZeros -= 1

    print spotArray
    functions.mostCheckedNextSpotList( spotArray )

