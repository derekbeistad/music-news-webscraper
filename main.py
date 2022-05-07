import requests
from bs4 import BeautifulSoup
import os
from twilio.rest import Client

# Constants
NEWS_LINK = 'https://www.indieisnotagenre.com/news/'
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
FROM_NUMBER = 'number'
TO_NUMBER = 'number'

# Setup
client = Client(account_sid, auth_token)
content = requests.get(NEWS_LINK)
soup = BeautifulSoup(content.text, 'html.parser')

# Gathering Data
articles = soup.find_all(name='h2', class_='entry-title', attrs={'itemprop': 'headline'})

# Parsing Through Data
titles = []
links = []
for article in articles:
    titles.append(article.string)
    links.append(article.find(name='a')['href'])

# Create CSV
with open("top-indie-music-news.csv", mode='a') as file:
    entry = "Top Indie Music News Today From 'Indie Is Not a Genre'.\n\n"
    for title, link in zip(titles, links):
        new_entry = f"Title: {title}\n{link}\n\n"
        entry += new_entry
    file.write(entry)

# Twilio SMS Alert
# # Create Message
# body_text = ''
# for n in range(len(titles[:6])):
#     body_text += f"Title: {titles[n]}\n{links[n]}\n\n"
# message = client.messages \
#                 .create(
#                     body=f"Top news today from 'Indie Is Not A Genre'.\n\n{body_text}",
#                     from_=FROM_NUMBER,
#                     to=TO_NUMBER
#                 )
