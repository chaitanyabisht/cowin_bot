import json
import requests
import datetime
import os

def telegram(telegram_token,chat_id,message):
    url=f'https://api.telegram.org/bot{telegram_token}/sendMessage'
    payload={"chat_id":chat_id,"text": message}
    telegram_data=requests.post(url=url,json=payload)
    return telegram_data.json()


def api(pincode,date):
    url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={date}'
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43'}
    
    response = dict(requests.get(url,headers = headers).json())

    lst = []

    centers_lst = response['centers']
    
    nothingfound = True

    for center in centers_lst:
        flag = False
        message = ''
        for session in center['sessions']:
            if (session['min_age_limit'] >= 18 and session['available_capacity'] >= 0):

                if (flag == False):
                    #print(f'Center ID: {center["center_id"]}')
                    #print(f'Center Name: {center["name"]}')

                    message += f'Center ID: {center["center_id"]}\n'
                    message += f'Center Name: {center["name"]}\n'

                    flag = True
                    nothingfound = False

                    #print()
                    message += '\n'
                
                #print(f'    Date: {session["date"]}')
                #print(f'    Vaccine: {session["vaccine"]}')
                #print(f'    Available Capacity: {session["available_capacity"]}')

                message += f'    Date: {session["date"]}\n'
                message += f'    Vaccine: {session["vaccine"]}\n'
                message += f'    Available Capacity: {session["available_capacity"]}\n'

        if (flag == True):
            lst.append(message)
        
    if (nothingfound == True):
        lst.append(-1)

    return lst


    
def lambda_handler(event, context):
    x = datetime.datetime.now()
    date = str(x.day) + '-' + str(x.month) + '-' + str(x.year)

    lst = (api(110075,date))

    if (lst[0] != -1):

        token = os.getenv('BOT_TOKEN')
        chat_id = os.getenv('CHAT_ID')
        for message in lst:
            telegram(token,chat_id,message)
    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
