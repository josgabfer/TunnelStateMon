import smtplib
from email.message import EmailMessage
from dotenv import dotenv_values, find_dotenv
from getToken import generate_auth_string
import requests
import json
from requests.models import HTTPError
from termcolor import colored


config = dotenv_values(".env")

EMAIL_ADDRESS = config['EMAIL_ADDRESS']
PASS = config['PASS']
RECIPIENTS = config['RECIPIENTS']
count = 0

def send_email(body):
    """This function will send an alert to the desired recipients"""
    msg = EmailMessage()
    msg['Subject'] = 'AD Connector Error Found!'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENTS
    msg.set_content("\r\n".join(body))

    msg.add_alternative("""
    <!DOCTYPE >
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AD Connector Monitor</title>
    </head>
    <body>
        <h1>Detected Tunnels Down</h1>
        <p>The following tunnel(s) are currently DOWN or UNESTABLISHED: <br/>""" + "\r\n".join(body) + """ <br/> Please check your Umbrella dashboard.</p>

        <style type="text/css">
            body{
                margin: 0;
                background-color: #cccccc;
            }
        </style>
        
    </body>
    </html>
    """, subtype='html')

    
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(EMAIL_ADDRESS,PASS)
        print('login success')
        smtp.send_message(msg)
        print("Email has been sent to: ", RECIPIENTS)

def get_request(): 
    """This function will send a GET request to get a list of all AD integration components"""
    try:
        config = dotenv_values(find_dotenv())
        token = config.get('TOKEN')
        if (token == None):
            token = (generate_auth_string())
        print(token)
        url = "https://api.umbrella.com/deployments/v2/tunnels"
        params = {
            "includeState": "True"
        }
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "includeState": "True"
        }
        response = requests.get(url, params=params, headers=headers)
        if (response.status_code == 401 or response.status_code == 403):
            token = generate_auth_string()
            return get_request()
        elif (response.status_code == 200):
            print(colored("Get request successfully executed!", "green"))
            print("\n")
            if (response != None):
                tunnel_json = response.json()
                return tunnel_json
            else:
                return 'Error'

    except HTTPError as httperr:
        print(colored(f'HTPP error occured: {httperr}','red'))

    except Exception as e:
        print(colored(f'HTPP error occured: {e}','red')) 



def alert():
    """This function will search for all the AD connectors in error state to call the send email function"""
    tunnels = get_request()
    body = []
    count = 0
    for tunnel in tunnels:
        if(tunnel['meta']):
            if (tunnel['meta']['state']['status'] == 'DOWN'):
                message = tunnel['name'] +  ': '  + tunnel['meta']['state']['status'] +'<br/>'
                body.append(message)
                count+=1
        else:
            message = tunnel['name'] + ': ' + 'Unestablished' + '<br/>'
            body.append(message)
    if(count !=  0):
        send_email(body)
    else:
        print('Tunnels are Up and running')

if __name__ == '__main__':
    alert()
