# Installing Dofler on Fedora/CentOS

This document is a step-by-step walkthrough for installing a full dofler setup for a Fedora-based system.  These directions should also work with minimal modification on any CentOS or RHEL host.

All of these commands assume that you are running as root.


## Client/Parser Installation

1. Update the System to Current: `yum -y update`
2. Install the Development Tools: `yum -y groupinstall "Development Tools"`
3. Install the needed dependencies: `yum -y install git ettercap wireshark libpng-devel libjpeg-devel giflib-devel libpcap-devel python-devel`
4. Goto the system src directory: `cd /usr/src`
5. Download the patched driftnet source: `git clone https://github.com/bldewolf/driftnet.git`
6. Goto the driftnet source directory: `cd driftnet`
7. Modify the Makefile to not display a window.  This means uncommenting the -DNO_DISPLAY_WINDOW cflag ammentment. `vi Makefile`
8. Build driftnet: `make`
9. Install Driftnet: `cp driftnet /usr/local/bin;cp driftnet.1 /usr/local/share/man/man1`
10. Install Distribute (needed for pip): `curl http://python-distribute.org/distribute_setup.py | python`
11. Install Pip: `curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python`
12. Install dofler and dependencies: `pip install dofler`
13. Adjust configuration settings as needed: `vi /etc/dofler/dofler.conf`

## Service/WebUI Installation

1. Update the System to Current: `yum -y update`
2. Install the Development Tools: `yum -y groupinstall "Development Tools"`
3. Install the EPEL Repo: `rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm`
4. Install the 10Ren Repo: `curl -o /etc/yum.repos.d/10gen.repo https://gist.github.com/reggi/4956419/raw/47f0b07f2220ac126aabd0a110f3a2b7b43529a3/10gen.repo`
5. Install the needed dependencies: `yum -y install mongo-10gen mongo-10gen-server python-devel libxslt libxslt-devel atlas atlas-devel`
6. Startup Mongo: `service mongod start`
7. Install Distribute (needed for pip): `curl http://python-distribute.org/distribute_setup.py | python`
8. Install Pip: `curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python`
9. Install numpy: `pip install numpy`
9. Install dofler and dependencies: `pip install dofler scipy`
10. Adjust configuration settings as needed: `vi /etc/dofler/service.conf`