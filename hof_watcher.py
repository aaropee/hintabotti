# Imports

import os
import requests
# Webscraper
from bs4 import BeautifulSoup
# Time - functions
from datetime import datetime
from threading import Timer
# Bot token and id
from dotenv import load_dotenv
load_dotenv()

# Establish time 
x = datetime.today()
y = x.replace(day = x.day+1, hour = 9, minute = 0, second = 0)
delta_t = y-x
secs = delta_t.seconds+1

token = os.getenv('TOKEN')
chat_id = os.getenv('CHAT_ID')
# Product page
url = 'https://www.thomann.de/fi/tc_electronic_hall_of_fame_2.htm'
telegram_api_send_message = f'https://api.telegram.org/bot{token}/sendMessage'
# Set the target price
my_price = 100

def main():
    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'html.parser')
    # Pull the name and price of the product from the site
    title = soup.find(itemprop="name").get_text().strip()
    price = soup.find(class_ = "prod-pricebox-price").get_text().strip()[0:3]  # format the 
    
    # Define the content of the Telegram - message
    data = {
        'chat_id': chat_id,
        'text': f'*${price}*\n[{title}]({url})',
        'parse_mode': 'Markdown'
    }

    # compare the list-price to the target
    if price > str(my_price):
        print("The price is still too high")
    else:
        source = requests.post(telegram_api_send_message, data=data)

# Run the program once every day at desired time
t = Timer(secs, main)

# Start the timer, which runs the main - method
if __name__ == '__main__':
    t.start()