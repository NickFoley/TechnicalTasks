# TechnicalTasks
 - This repository contains the 3 technical tasks requested. 
 - Each task is contained within its own directory.
 - Every task has a md file containing assumptions that were made in absence of required information. 
 - All tasks were completed with Python 3.9.1 
 - All Tasks have an image call OutputScreenshot, which is a screenshot showing the task being successfully executed.
## Task 1 
 ```
Task 1 - Write a script in Python that prints the numbers from 1 to 75.
But for multiples of four print "Mission" instead of the number and for the multiples of five print "Control".
For numbers which are multiples of both four and seven print "Mission Control".
 ```
 - Task 1 has no dependencies and can be run with:
```buildoutcfg
python task1.py
```
## Task 2
 ```
Task 2 - Data handling and basic visualisation test:
Download json GOES 16 proton data from services.swpc.noaa.gov
https://services.swpc.noaa.gov/json/goes/primary/differential-protons-1-day.json
Put into Pandas Dataframe
Plot a 20 minute moving average against the raw inputs for p1
 ```
- Task 2 has dependencies and a requirements.txt file has been produced.
- A requirements.txt file has been made define required dependencies. A venv can be setup and configured with:
```buildoutcfg
python -m venv task2
task2\Scripts\activate.bat
python -m pip install -r requirementlss.txt
```
- Task 2 can then be run with
```buildoutcfg
python task2.py
```
## Task 3
 ```
Task 3 - Create a single RESTful endpoint in Flask for delivering spwx data:
Download https://services.swpc.noaa.gov/json/rtsw/rtsw_mag_1m.json to form a SQLite3 table.
Have the endpoint use query strings to allow you to select a time period of up to an hour. Where the data is grouped into periods of 5 minute averages and returned via json.
 ```
- Task 3 has dependencies and a requirements.txt file has been produced.
- A requirements.txt file has been made define required dependencies. A venv can be setup and configured with:
```buildoutcfg
python -m venv task3
task3\Scripts\activate.bat
python -m pip install -r requirementlss.txt
```
- Task 3 can then be run with
```buildoutcfg
python task3.py
```