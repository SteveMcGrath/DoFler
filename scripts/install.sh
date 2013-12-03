#!/bin/bash
# DoFler Installation Script
# ----------------------------------
# This is an installation script to automate installing everything needed for
# dofler to function.  This includes some things like an upstart script to
# automatically startup the daemon.

DISTRO=$(lsb_release -is)

echo -e "\n\n"
echo -e "DoFler Installation Script for Linux"
echo -e "-------------------------------------"
echo -e "\nBefore we begin, we need to ask you a few questions to help with the"
echo -e "installation."
echo -e "\n"
echo -en "Will this installation be network accessible? (y/n) [Default: n]: "
read NETWORK 
echo -e "\n\nPress Enter to start the install, or CNTRL+C to exit."
read cont

# Check to see if we are running as root.  If not, when most of this script wont
# work, so just throw an error and bomb out.
if [ $UID -ne 0 ];then
	echo "ERROR: Please run this script as the root user."
	exit
fi

# First thing we need to do is update the OS, then install all of the
# dependencies...
if [ "$DISTRO" -eq "Ubuntu" ];then
	apt-get update
	apt-get -y upgrade
	apt-get -y install pkg-config libpng12-dev libjpeg-dev libgif-dev git-core\
					   libpcap-dev python-dev ettercap-text-only sqlite3 tshark\
					   build-essential
elif [ "$DISTRO" -eq "CentOS" || "$DISTRO" -eq "Fedora" ];then
	yum -y update
	yum -y groupinstall 'Development Tools'
	yum -y install git ettercap wireshark libpng-devel libjpeg-devel\
				   giflib-devel libpcap-devel python-devel wget
fi

# Now for python's pip (Package Installer for Python)
wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python
wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py -O - | python

# Next we will need to pull down and build driftnet from scratch. We want a
# version that has png support, which isnt in any of the mainline repositories.
cd /usr/src 
git clone https://github.com/bldewolf/driftnet.git
cd driftnet
sed -i "/#CFLAGS += -DNO_DISPLAY_WINDOW/ s/#//" Makefile
make
cp driftnet /usr/local/bin/

# And now that we have everything we need, lets install dofler itself. Because
# we installed pip, we will use that to pull everything down.
pip install dofler 

if [ "$DISTRO" -neq "Ubuntu" ];then
	echo "NOTE: I havent coded automating past getting the code installed for"
	echo "      any operating system aside from Ubuntu.  Most of the rest of"
	echo "      this script could technically apply to CentOS 6, however in"
	echo "      an effort to get the code and installer out quickly, this was"
	echo "      forgone for the moment.  If you would like to contribute to the"
	echo "      installer script, please feel free on the github site below:"
	echo ""
	echo "      https://github.com/SteveMcGrath/DoFler"
	exit
fi

# Next up, the upstart script.
cat <<EOF > /etc/init/dofler.conf
description "Dofler"
author "steve@chigeek.com"

respawn
respawn limit 15 5

start on runlevel [2345]
stop on runlevel [016]

exec /usr/bin/dofler run
EOF

# 

initctl reload-configuration

# Now we need to start it up to create the databases, config files, etc.
initctl start dofler

# If dofler's WebUI is supposed to be network accessible then we will need to
# stop it and reconfigure it.  Currently there isn't a cli command to address
# the sqlite settings DB, so we will have to handle it manually.
if [ "$NETWORK" -eq "y" || "$NETWORK" -eq "Y" ];then
	sqlite3 /var/lib/dofler/settings.db "update settings set value='0.0.0.0' where name='api_host'"
	initctl restart dofler