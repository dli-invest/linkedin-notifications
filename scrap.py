from linkedin_api import Linkedin
import requests
import dateparser
import re
from datetime import datetime, timedelta
import json
import os
# Authenticate using any Linkedin account credentials
email = os.environ.get("LINKEDIN_EMAIL")
password = os.environ.get("LINKEDIN_PASSWORD")
webhook = os.environ.get("DISCORD_WEBHOOK")
if email is None or password is None:
    exit("Failed to get app credentials")
api = Linkedin(email, password)


def post_webhook_content(url: str, content: str):
    url = url
    data = {}
    # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data["content"] = content

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


for company in ['datacm', 'arht-media-inc-', 'peakfintech']:
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
            if now-timedelta(hours=24*3) <= relativeDate <= now:
                print(relativeDate)
                print(cleanText)
                post_webhook_content(webhook, cleanText)
            else:
                break
        except Exception as e:
            print(e)
