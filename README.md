# PeopleForce Timesheet Logger
Log the timesheet for a particular month automatically


### 1. Install Python3
```shell
brew install python
```
##### 2. Create a virtual env inside the project
```shell
virtualenv venv -p /usr/bin/python3
```
##### 3. Activate the virtual env
```shell
source venv/bin/activate
```
##### 4. Install packages from [requirements.txt](requirements.txt)
```shell
python3 -m pip install -r requirements.txt
``` 

Selenium uses **Safari** as a browser for automation, and you should enable the **Developer Tools** and **Allow Remote Automation**
- Open safari
    - Go to Preferences
    - Switch to Advanced tab
    - Enable **Show Develop menu in bar**
- Go to **Develop** tab in the header navbar
  - Click on **Allow Remote Automation**