# What is it?
DoFler (Dashboard of Fail + DOPPLER) is a fully automated dashboard
setup that can be easily distributed as needed.  A central dofler server
acts as the aggregation point and also serves up the HTML page that people 
can then view.

The HTML page is simple page that uses Javascript and CSS to format the
output so that it looks pleasing, and can auto-update.  The Javascript
pulls the most recent data from the JSON api in the backend.

![screenshot](http://f.cl.ly/items/071X1p3I1O0N1423073Z/Screen%20Shot%202013-03-14%20at%202.27.14%20PM.png)

# How do I use it?
Run code, drink, and be marry ;)

# How do I install it?
Installation can depend on how you would like to deploy dofler.  All
early testing was done using both the client and server on the same
host, however it was designed to split the two and have multiple
clients running.

## Requirements

* Python 2.6,2.7

__Client Only__

* Ettercap
* TShark (Part of Wireshark)
* Driftnet (Use the https://github.com/bldewolf/driftnet fork)

## Installation

* Install using pip or easy_install `pip install dofler doflersvc`
* Adjust the config file at /etc/dofler/dofler.conf & /etc/dofler/service.conf as needed.
* Start up the approprate services (_dofler-server_ and _dofler_)

## Installation Guides

* [fedora_guide][Fedora Installation Guide]
* [debian_guide][Debian Installation Guide]
* [osx_guide][Max OSX Installation Guide]
* [wintel_guide][Windows Installation Guide (Server-only)]

[fedora_guide]: https://github.com/SteveMcGrath/DoFler/blob/master/doc-data/fedora-install-guide.md
[debian_guide]: https://github.com/SteveMcGrath/DoFler/blob/master/doc-data/debian-install-guide.md
[osx_guide]: https://github.com/SteveMcGrath/DoFler/blob/master/doc-data/osx-install-guide.md
[wintel_guide]: https://github.com/SteveMcGrath/DoFler/blob/master/doc-data/wintel-install-guide.md


# ChangeLog

* 0.3.0
	* Complete Rewrite
	* Now uses MongoDB as the backend instead of MySQL/SQLAlchemy
	* Can now enable/disable certain views (images, stats, accounts) in WebUI
	* WebUI now has a "porn reset" function as part of the API
	* Dofler is now split into 2 packages, dofler and doflersvc
	* Removed any client-side time dependencies
* 0.2.0
	* Updated WebUI so that it uses UTC Time instead of Local Time.
	* Minor bugfixes
* 0.1.0
	* Initial Release


# API Documentation

The API is accepts requests using urlencoded formdata and will return
responses (if available) in a json dictionary format.  The client-side
supporting APIs are designed to be temporal in nature.  Because of this,
it is very important that the server uses NTP or some other way to keep
the time in sync with what the rest of the work uses.


## /login

__Required Inputs:__ sensor, auth, salt
__HTTP Methods:__ POST

### Info

Will use the information provided, coupled with the secret for the sensor
in the config file to indipendently validate the hash that the client sent.
If the hashes match, it will return an authentication cookie.

### Options

* __sensor:__ [string]: The Sensor Name.

* __auth:__ [string]: The MD5 Hash that we will be computing against.

* __salt:__ [string]: Some random data of some kind so that the auth hash
  isnt always the same.


## /post/account

__Required Inputs:__ username, password, info, proto, parser
__HTTP Methods:__ POST

### Info

Uploads a potentially new account to the API to be added to the database,
and then presented to users.  The account presented will be checked to see
if it already exists int he database; if there is no previous upload of the
account, then it will be added.

### Options

* __username:__ [string]: The username of the account.

* __password:__ [string]: The password of the account.  It is assumed that any 
  anonymization of the password is done client-side, so none will be done on the
  server-side.

* __info:__ [string]: Any information such as URL, Ip Address, etc. goes here.

* __proto:__ [string]: The Protocol name.

* __parser:__ [string]: The name of the parser that generated this event.  While
  not displayed, it may be useful for further analysis.


## /post/stats

__Required Inputs:__ jdata
__HTTP Methods:__ POST

### Info

Here is where we gather information about the types of traffic we see on the network.
The parser listens to all of the traffic with tshark, then responds with a JSON
dictionary containing everything it's seen since last checkin.

### Options

* __jdict:__ [JSON]: {'PROTO1': COUNT, 'PROTO2': COUNT}


## /post/image

__Required Inputs:__ filetype, file
__HTTP Methods:__ POST

### Info

Uploads an image to the API there is it parsed into the database.  As the database
is designed to only keep one copy of an image, it will first check to see if the
image is already int he DB based on the MD5Sum and will simply update the timestamp
if this is the case.  If the image does not exist, it will then add the image to the
database.

### Options

* __filetype:__ [string]: The file extension (e.g. png, jpg, gif)

* __file:__ [file]: The image file.


## /account_total

__Required Inputs:__ NONE
__HTTP Methods:__ GET

### Info

Returns the total number of accounts in the system.  This is intended to be displayed
in the footer of the account listing.


## /accounts/NUM

__Required Inputs:__ NUM
__HTTP Methods:__ GET

### Info

Returns a JSON dictionary of all of the accounts with a higher ID than what was
sent to the API.  For example, to get all of the accounts in the system, you would
call the api with '/api/accounts/0' to get all IDs greater than or equal to 0.

### Options

* __NUM:__ [integer]: The ID of the next account to get.


## /images/TIMESTAMP

__Required Inputs:__ TIMESTAMP
__HTTP Methods:__ GET

### Info

Returns a JSON dictionary of the MD5 hashes of all the images that are newer than
the timestamp sent.  The timestamp is basic UNIX time.

### Options

* __TIMESTAMP:__ [timestamp:integer]: The times in unix time that you would like to
  pull images from.  Any images with a timestamp newer than this will be returned.


## /image/HASH

__Required Inputs:__ HASH
__HTTP Methods:__ GET

### Info

Returns the Image file based on the Hash provided.

### Options

* __HASH:__ [string:md5 hash]: The MD5 hash fo the image.


## /stats

__Required Inputs:__ NONE
__HTTP Methods:__ GET

### Info

__INCOMPLETE__

Returns a JSON dictionary of the sums of the traffic statistics that were collected by the tshark_stats parser.