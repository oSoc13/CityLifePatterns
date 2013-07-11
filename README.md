CityLifePatterns
================

#General
This repository is the basis of a new feature for the CityLife / Vikingspots API build for VikingCo during open Summer of code.

##Backend
This repository contains all scripts to include a feature which returns relevant VikingSpots based upon your last checkin.
It does so by making tuples (checkin, next checking) and counting the amount of times that occures.

((checkin, next checkin), count)

Another script can be used (but isn't at the moment) to grab the 5 highest counts for each checkin.
The API can grab the x highest counts for a checkin of choise, or it can use the table created by the second script to just get 5 of them really fast.

Future development will enable the API to use weights as well as counts. The weight algorithmn needs to be tweaked in order to make it really relevant.
This however will not be handled during oSoc13 due to a lack of time.

#Frontend
Though the primary goal was the backend, we took the time actually do something with it.
in src/extension you will find an unpacked chrome extension that will enable you to add our feature to the CityLife WebApp that can be found at:
https://web.citylifeapp.com
(warning: the extension doesn't use https for the time being)

The extension will add a button to every SpotDetail which allows the user to see "what's up next". 
Clicking this button will make the api return the probable next spots out of the API.

To make sure we don't break the flow of the webapp, we've choosen to pull some hackerish tricks:
  * we can't know when the ajax request ends, so we use a timeout (for now) to include the buttons on the pages
  * we can't trigger the new page animation from the extension, so we make it go to an error page and substitute the content of that page
  * In the future we'd like to change the static timeout to a loop

##Legal
open Summer of code is an initiative of OKFN Belgium. All code written inside this repository is owned by OKFN Belgium.

Author rights go to:
 * Linsey Raymaekers
 * Wouter Vandenneucker

#Technology
From the CityLife API until the extension we've got an "n tier"-architecture.
Every tier uses different technologies to ensure speed and stability. 
We'll list those technologies so you have an idea why some choises where made

  * The CityLife data is stored using Redis "key value storage"
  * The CityLife API is written in Python and uses Django as a framework
  * Our "Nightly batch script" is written in Python as well.
  * The data from the batch script is stored in a mySQL database because of it's convience. Though converting it to redis might be a good idea in the future
  * Our API is build with Python and Django

On the frontend side of things, we've got:
  * A webapp using both CoffeeScript, Zepto and Backbone
  * Our extension uses JQuery and Chrome.extension api's

#Repo BuildUp
The repo consists of 3 main folders:
 * Wireframes
 * Src
 * tools

##Tools
The tools section is the least interesting one, it just contains the scripts we used to convert the Redis databasedump to a json file.
Converting it to a json made sure we didn't need to run Redis all the time (our notebooks can't handle it).

##Wireframes
The wireframes are flowcharts of our code. The in and outs as described above, just more easy to understand than my rambling.

##Src
  * This contains everything of importance the code/modules folder contains all functions and settings needed to make the scripts work
  * Frontend contains our API frontend (using Django). 
  * extension contains an unpacked chrome extension which enables the API functions in the webapp

#Usage
Will be added later
