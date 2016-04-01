This is the node.js rewrite.  its entirely new code in a new language, and I'm learning what works and what doesnt all over again.

This code is currently in a very incomplete state and is not considered stable.

Current Status:

* [WORKING] NGrep 
* [WORKING] TShark
* [IN-PROG] Driftnet
* [TODO] Dsniff
* [TODO] ettercap
* [TODO] Web Dashboard (websockets?)

Design Goals List

* Use WebSockets to handle page updates instead of an API.
* The Accounts data should be a revolving list of 5-10 items, rotating in a new one every second or so.
* The server should handle interacting with the PVS sensor to pull the vuln data for the top 5 hosts.  This should be handled via an API call as there is a lot of wiring that needs to be done to make this work and the page visualization will be refreshed every time with new data.
* Stats should be updates via API, as the protocols could change.
* the main page should present a mobile-friendly format