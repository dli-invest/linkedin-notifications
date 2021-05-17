from linkedin_api import Linkedin
import requests
import dateparser
import re
from datetime import datetime, timedelta
import json
import os
import time
import sys
# Authenticate using any Linkedin account credentials
email = os.environ.get("LINKEDIN_EMAIL")
password = os.environ.get("LINKEDIN_PASSWORD")
webhook = os.environ.get("DISCORD_WEBHOOK")
if email is None or password is None:
    print("SOME MESSAGE GOES HERE")
    exit("Failed to get app credentials")
api = Linkedin(email, password)


def post_webhook_content(url: str, embeds: list):
    url = url
    data = {}
    # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data["embeds"] = embeds

    result = requests.post(
        url, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

def clean(str):
    # removes any text with # symbols
    # and urls 
    if str:
        clean_str = " ".join(filter(lambda x:x[0]!='#', str.split()))
        clean_str = re.sub(r'http\S+', '', clean_str)
        return clean_str
    else:
        return None

print("LOOKING FOR UPDATES")

def loop_for_company(company: str):
    print("CURRENT COMPANY")
    print(company)
    updates = api.get_company_updates(company, None, 10)
    # get income
    for update in updates:
        # get commentary object
        try:
            commentary = update["value"]["com.linkedin.voyager.feed.render.UpdateV2"]["commentary"]["text"]['text']
            annotation = update["value"]["com.linkedin.voyager.feed.render.UpdateV2"]["actor"]["subDescription"]["accessibilityText"]
            cleanText = clean(annotation)

            relativeDate = dateparser.parse(cleanText)
            now = datetime.now()
            if now-timedelta(hours=24*5) <= relativeDate <= now:
                actions = update["value"]["com.linkedin.voyager.feed.render.UpdateV2"]["updateMetadata"]["actions"]
                url = "https://www.linkedin.com/company/peakfintech/"
                for action in actions:
                    if action.get('url') != None:
                        url = action.get('url')
                        break
                embeds = [{
                    "title": f"{company} - {cleanText}",
                    "description": commentary,
                    "url": url
                }]
                post_webhook_content(webhook, embeds)
                time.sleep(2)
            else:
                break
        except Exception as e:
            print(e)

companies = ['datacm', 'arht-media-inc-', 'peakfintech']
company = sys.argv[0]
loop_for_company(company)
