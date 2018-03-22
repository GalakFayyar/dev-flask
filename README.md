Python Flask API Project
===================
Basic architecture for Flask Projects

# Requirements
Python > 3.4
Pew
Pip

# Install notes
Get the project locally :
```
git clone https://github.com/GalakFayyar/dev-flask.git
```
Once in the local project folder, it is advised to create a new virtual environment using `pew` command :
```
pew new ENVIRONMENT_NAME -p python3.5 -r requirements.txt
```
Use the new envrionment as subshell :
```
pew workon ENVIRONMENT_NAME
python server.py
```
or directly execute command in virual environment :
```
pew in ENVIRONMENT_NAME python server.py
```
Test the API response by getting 200 status and "yo" content on the url :
http://localhost:9091/api-dev/heartbeat

## Notes
Do not forget to install `pythonX.X-dev` (with X.X is the version name). The dev package is required to properly use and install the dependencies with `pip` (python package manager). 
