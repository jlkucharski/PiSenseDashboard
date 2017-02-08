# PI Sense dashboard
The dashboard presents the data gathered using PI sense for Raspberry Pi. The project can be split into two main pieces:
1. Data gathering job - python script running in cron (or as infinite python script) that gathers the data and saves it into csv files under data/
2. Data presentation/dashboard - SPA using angularjs and c3js on front end and python with flask on the back end.


## File structure
- data/* - test data 
- dashboard/* - dashboard files
- run_weather.sh - bash script that triggers weather.py (used by cron)
- weather.py - measures the temperature, humidity and pressure and saves it to *.csv files in data