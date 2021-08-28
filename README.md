# TechnicalTasks
 - This repository contains the 3 technical tasks requested. 
 - Each task is contained within its own directory.
 - Every task has a md file containing assumptions that were made in absence of required information. 
 - All tasks were completed with Python 3.9.1 
 - All Tasks have an image called OutputScreenshot, which is a screenshot showing the task being successfully executed.
## Task 1 
 ```
Task 1 - Write a script in Python that prints the numbers from 1 to 75.
But for multiples of four print "Mission" instead of the number and for the multiples of five print "Control".
For numbers which are multiples of both four and seven print "Mission Control".
 ```
#### Running Task 1
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
#### Task 2 dependencies
- Task 2 has dependencies, as defined in the requirements.txt.
- A venv can be setup and configured with:
```buildoutcfg
python -m venv task2
task2\Scripts\activate.bat
python -m pip install -r requirements.txt
```
#### Running Task 2
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
#### Task 3 dependencies
- Task 3 has dependencies, as defined in the requirements.txt
- A venv can be setup and configured with:
```buildoutcfg
python -m venv task3
task3\Scripts\activate.bat
python -m pip install -r requirements.txt
```
#### Running Task 3
- Task 3 can then be run with
```buildoutcfg
python task3.py
```
#### Testing Task 3
- Run the task3 application/webserver.
- Using a browser or curl/wget query the endpoint and pass the start and end datetime_:
  ```http://127.0.0.1:5000/spwcdata/start_datetime/end_datetime```
- Replace the start and end datetime with a current/valid datetime and ensure the format "%Y-%m-%dT%H:%M:%S"
- For example:
   ```http://127.0.0.1:5000/spwcdata/2021-08-27T11:30:00/2021-08-27T12:15:00```
- The queried data should be returned in valid, pretty printed JSON format.