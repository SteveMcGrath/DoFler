# How to Use DoFler

DoFler is an automated "Wall of Ewes" clone that leverages the output from
multiple tools to drive the content provided on the WebUI.  As the WebUI is
driven by a back-end API, it's possible to feed and pull data using 3rd party
applications as well.  The end result is that DoFler becomes a central
aggregation point for all of the data you want to display on the screen.
While DoFler was originally written for use at conferences, mostly for
entertainment purposes, it has since expanded beyond it's original intention
and branched out into other uses as well.

Running DoFler in most cases involves a single box with 2 network cards.  One
of the cards is listening on an IP and displaying the WebUI while the other is
sniffing to a span or a tap on the network in order to pull the information.
More complex (multi-sensor) scenarios are definitely possible, and DoFler is 
designed with bigger installations in mind as well.

# Getting Started

Once DoFler is started up, you will see a mostly blank screen.  Click on the
Gear Icon in the upper-right corner to enter the settings & config section.
From here you can login to the WebUI to gain access to all of the configuration
options within the DoFler sensor.  The default account information is:

* __Username:__ admin
* __Password:__ password

It's highly recommended to [change this][users] as soon as you initially login 
to the console.  While the admin account cannot be removed, you can change the
password from the users menu.  Further you can add whatever users you want
into the system as well.  All users sare the same "admin" level of access
as users are generally used for pushing content from remote sensors.  It's
also worth noting that if you change the admin password, that you also update
the server account password so that the local parsers can properly communicate
to the API.

# Starting up the Parsers

Go ahead and click the [Parser Settings][parsers] and make sure everything
look correct.  Somethings worth pointing out is that by default, DoFler will
not start up any of the parsers when it is loaded.  If you want the parsers to
autostart then enable that setting.  Further as Dofler is reliant on the
output of other applications, sometimes the default settings will not work
with the application version installed.  TShark in particular is notorious for
this.  In TShark's case specifically, if you do not see any HTTP POSTs to the
API (url: /post/stat) after 60 seconds of starting up the parser, then you may
need to adjust the settings.  Here are some common commands for various
installations, versions, and packaged versions:

_NOTE: These commands all use rungbuffers, and may not be desirable_

* __Debian Testing :__ `tshark -T psml -PS -l -i {IF} -b filesize:100000 -b files:3 -w /tmp/tshark-stats.pcap`
* __CentOS/RHEL 6 :__ `tshark -T psml -i {IF} -S -b filesize:100000 -b files:3 -w /tmp/tshark-stats.pcap`
* __Ubuntu 12.04 :__ `tshark -T psml -Sli {IF} -b filesize:100000 -b files:3 -w /tmp/tshark-stats.pcap`

Lastly, make sure you set the listening interface to the proper promiscuous
interface.  The default (eth1) may not match what your monitoring.

Once your happy with the values you are seeing, go ahead and switch over to
the [Services Settings][services] and turn on the parsers.  They should now
be running and looking at the appropriate interface.  If you don't see any
information within a few minutes, then you may need to re-evaluate the parser
settings.

# Finishing Up

DoFler is still under heavy development, however please let us know if you
happen to come across any bugs, or if there are any other issues that you
have discovered.  Further, if you wish to help with development, we are always
looking for people to help out with things like the WebUI, backend parsers,
etc.  Contact Steven McGrath if you want to help:

* __Twitter :__ [@SteveMcGrath][twitter]
* __IRC :__ [Steve in #burbsec on FreeNode][irc]
* __Email :__ steve (at) chigeek.com
* __Devblog :__ [http://chigeek.com/tag/dofler.html]()
* __Code Repository :__ [http://chigeek.com/tag/dofler.html]()
* __Issue Tracker :__ [http://chigeek.com/tag/dofler.html]()

[parsers]: /ui/settings/parsers
[users]: /ui/settings/users
[services]: /ui/settings/services
[twitter]: https://twitter.com/stevemcgrath
[irc]: irc://irc.freenode.net/burbsec