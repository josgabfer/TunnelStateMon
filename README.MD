# Tunnel State Monitor

The tunnelstatemon script sends email alerts when it detects a tunnel in error state.  
This is achieved by sending a GET request to https://docs.umbrella.com/umbrella-user-guide/docs/tunnels to get all the AD integration components (VAs, DCs and AD connectors) from the dashboard. After this, the script checks the status of all AD connectors in the dashboard and if it finds an AD connector in error state, it will send an email alert to the specified recipients.

## Installation

Use git to clone the repository files to your machine:

```bash
git clone https://github.com/josgabfer/ADConnMon.git

# Requirements:
Package            Version
------------------ -----------
certifi            2022.6.15.1
charset-normalizer 2.1.1
flatdict           4.0.1
idna               3.3
numpy              1.23.3
pandas             1.4.4
pip                22.2.2
python-dateutil    2.8.2
python-dotenv      0.21.0
pytz               2022.2.1
requests           2.28.1
setuptools         63.2.0
six                1.16.0
termcolor          2.0.1
urllib3            1.26.12
```

## Files

ADConnectorMonitor.py - this python file perform 3 tasks:  
    1) Send a GET request to https://api.umbrella.com/deployments/v2/tunnels to get a list of all the tunnels in the Umbrella dashboard.  
    2) Check the status of all tunnels.  
    3) Send email alerts if it detects a tunnel in error state.  

getToken.py - this python file will take care of generating a new authentication token if needed.

.env - this file is not included in the repository files since it needs to be created locally on the machine. The .env file is where we store the parameters that the ADConnectorMonitor.py file needs to work. Please follow the next instructions:  
```
1) Create the .env file in the same location where the ADConnectorMonitor.py is stored and copy & paste the following text and fill:  
    EMAIL_ADDRESS = ''  
    PASS = ''  
    RECIPIENTS = ''  
    KEY = ''  
    SECRET = ''  
```

```
2) Add the values between the '' for each parameter:  
    EMAIL_ADDRESS: the sender's email address  
    PASS: password created by the sender that authorizes applications send  
    RECIPIENTS: the recipient's email address that will receive the email alerts (If you plan on adding more than one recipient, please use a coma to separate each email address)  
    KEY: API Key obtained from the Umbrella dashboard (Make sure that the API Key you created has "Virtual Appliances" included in the Key scope)  
    SECRET: Key secret  
```

## Usage

Run the script manually:
```python
Windows: python TunnelStateMonitor.py
Mac: python3 TunnelStateMonitor.py
```

Run the script automatically:
Multiple tools can be used to automate the script execution, however, this is up to the user as we don't recommend any specific ways to achieve automation. Here is an example on how to use the Task Scheduler in windows to automate python script executions: https://www.jcchouinard.com/python-automation-using-task-scheduler/
