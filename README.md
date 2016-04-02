# DoFler v5

## Introduction

DoFler (short for Dashboard Of Fail) is a Web-Based front-end tying data from a wide variety of different network sniffing and analysis tools.  The WebUI is intended to be displayed on a projector at Hacking/Information Security conferences, however I have heard of numerous people running DoFler in their own home labs, PwnPads, etc.

## Some Notes on v5

DoFler version 5.x is a complete rewrite leveraging Node.js to attain a lot of the Asynchronous goals that I had initially set forth with Python's Tornado framework.  Unfortunately, while Tornado would have let me re-use a lot of the parser code, it was ending up to be kludgey and it made more sense to simply switch over to a language and framework that was better suited to the workload that I'm attempting to do.  This does mean that I abandoned the scapy work I was doing, but as is life.

One of the biggest things thats new with v5 is that the WebUI is now Bootstrap-enabled and makes heavy use of web-sockets.  The heavy web-socket use allows the UI to be more real-time and more responsive.  It will no longer feel like everything is "batched" into the UI, but instead will generally flow into the UI in a more organic way.

I decided to stick with a relational back-end (even though I was heavily considering heading back to Mongo) as it gives a lot more flexibility to the deployed architectures (e.g. you could deploy this on a Raspberry Pi).

As I'm relatively new to Node.JS and Javascript, I'm sure there are a lot of inefficiencies that need ironing out, but so far in my testing it's been working pretty solidly.

## Installation

The pre-reqs for DoFler vary depending on what parsers you want to enable.  The default parsers use the following tools:

* ngrep
* ettercap 
* tshark

There are optional parsers as well:

* Tenable's PVS (via API calls)
* driftnet (See recommended version below for driftnet)

In general installing the pre-requisite tools should be a simple matter of installing them through your package manager.  Here is the command for installing the primary tools on Ubuntu 

````
sudo apt-get install ngrep ettercap-text-only tshark
````

For the database backend, DoFler supports MySQL, Postgres, or just about anything else that the [Sequelize](http://docs.sequelizejs.com/en/latest/) library supports.  For the purposes of this guide, we will cover MariaDB on Ubuntu.

````
# Install the binaries
sudo apt-get install mariadb-client mariadb-server

# Run the initial conifguration 
mysql_secure_installation

# Create the database 
mysqladmin -uroot -p create dofler 

# Create the dofler user 
mysql -uroot -p
> GRANT ALL PRIVILEGES ON dofler.* TO 'dofler'@'localhost' IDENTIFIED BY 'NEW_PASSWORD';
> exit 
````


In regards to Node.JS itself, I recommend using NVM to install Node.JS as it allows you to keep multiple version if needed, and allows for downloading the latest stable versions as well.  There is an awesome walk-through for Ubuntu that Digital Ocean provides and it is located [HERE](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-an-ubuntu-14-04-server#how-to-install-using-nvm).

Once you have Node.JS installed and the pre-requisites, you simply need to download the repository and then run npm to install the needed libraries to get dofler into a runnable state.

````
cd /opt 
git clone https://github.com/SteveMcGrath/DoFler.git
cd dofler 
npm install ./
````

As we are using MySQL/MariaDB, we do have to install the appropriate Node.JS database interface library.  To do so, we will do this: 

````
npm install mysql 
````

Lastly, copy the example.json config file in the config folder and call the copy "production.json".  Change the Database.uri parameter to match what you have configured.  From here, your ready to start up the binary! 

````
export NODE_ENV=production
./server.js 
````

You should see a bunch of console output at this point.  the default port DoFler listens on is port 3000, so just connect your browser to http://SERVER_ADDRESS:3000 and you should be good to go!

### Installing Driftnet

Installing driftnet is a little more complicated.  While there are many variants, and some of them may be in your package manager's system repositories, the fork of driftnet that I have seen the most success with is a version that has PNG support added in.  To install this version, you will need to build it yourself from source.

````
sudo apt-get install libpng-dev libjpeg-dev libgif-dev libpcap-dev build-essential
sudo /usr/src 
git clone https://github.com/bldewolf/driftnet.git 
cd driftnet 
vi Makefile 
# You will want to look for the "-DNO_DISPLAY_WINDOW"
# cflag.  Uncomment this flag in the make file.
make 
cp driftnet /usr/local/bin;cp driftnet.1 /usr/local/share/man/man1
````

### Installing the Systemd service file

__Coming soon__