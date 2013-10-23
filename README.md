# What is it?
DoFler (Dashboard of Fail + DOPPLER) is a fully automated dashboard
setup that can be easily distributed as needed.  A central dofler server
acts as the aggregation point and also serves up the HTML page that people 
can then view.

The HTML page is simple page that uses Javascript and CSS to format the
output so that it looks pleasing, and can auto-update.  The Javascript
pulls the most recent data from the JSON api in the backend.

![screenshot](https://raw.github.com/SteveMcGrath/DoFler/master/doc-data/screenshot1-0.4.0.152.png)

# How do I use it?
Run code, drink, and be marry ;)

# How do I install it?
Installation can depend on how you would like to deploy dofler.  All
early testing was done using both the client and server on the same
host, however it was designed to split the two and have multiple
clients running.

## Requirements

* Python 2.6,2.7
* Ettercap
* TShark (Part of Wireshark)
* Driftnet (Use the https://github.com/bldewolf/driftnet fork)

## Installation

* Install using pip or easy_install `pip install dofler`
* Start up the approprate services (_dofler_)

## Install Scripts

* [is_linux][Linux Installation Script] (CentOS, Fedora, Ubuntu)

[is_linux]: https://raw.github.com/SteveMcGrath/DoFler/master/scripts/install.sh

## Installation Guides

* [mysql_guide][Configuring to talk to a MySQL Database]
* [network_guide][Configuring a Distributed Client/Server Installation]
* [fedora_guide][Fedora Installation Guide] ** Old Guide

[network_guide]: https://raw.github.com/SteveMcGrath/DoFler/master/doc-data/network-guide.md
[mysql_guide]: https://raw.github.com/SteveMcGrath/DoFler/master/doc-data/mysql-guide.md
[fedora_guide]: https://raw.github.com/SteveMcGrath/DoFler/master/doc-data/fedora-install-guide.md

# ToDo

* Finish User Management Section of WebUI
* Write CLI app to manage settings from the commandline

# ChangeLog

* 0.4.0
    * Complete Rewrite (Again)
    * Merged in DoflerLite Codebase
    * Switched back to SQLAlchemy for portability reasons
    * Settings now stored in seperate SQLiteDB
    * Ability to use SQLite, MySQL, etc. for the main database.
    * A interactive WebUI for adjusting settings and parsers has been added.
    * DoFler re-merged into 1 package for client and server.
    * Removed need for SciPy for Protocol Statistics (Using Flot JS library instead)
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