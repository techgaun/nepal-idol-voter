# -*- coding: utf-8 -*-

import asyncio
import requests
from bs4 import BeautifulSoup as BS

provider = "mailnesia.com"
email_title = "Nepal Idol Voting"
email_title = "Hi"


def do_vote(name, email, country, contestant_id, contestant_name):
    payload = dict(
        name=name, email=email, country=country, contestant_id=contestant_id)
    r = requests.post('http://ap1.tv/nepalIdol/api/emailVoting', data=payload)
    # print(r.text)
    if r.ok:
        response = r.json()
        assert response['status']
        if response['message'].startswith('Maximum voting limit'):
            return False
        assert contestant_name in response['message']
        return True
    return False


def verify_vote(email):
    print("Verifying all e-mails for {}".format(email))
    inbox_url = "http://mailnesia.com/mailbox/{}?newerthan=1309034087&noheadernofooter=1".format(
        email)
    inbox = requests.get(inbox_url)
    #  print(inbox.text)

    if inbox.ok:
        soup = BS(inbox.content, 'html.parser')
        emails = soup.select("tr.emailheader")
        idol_emails = [
            idol_email['id'] for idol_email in emails
            if email_title in idol_email.text
        ]

        for mail_id in idol_emails:
            mail_url = "http://mailnesia.com/mailbox/usa/{}?noheadernofooter=ajax".format(
                mail_id)
            mail = requests.get(mail_url)

            if mail.ok:
                mail_soup = BS(mail.content, 'html.parser')
                idol_email = mail_soup.select(
                    'a[href=^="http://ap1.tv/nepalIdol/verifyEmailVoting"]')
                if idol_email:
                    email_url = idol_email['href']
                    r_verify = requests.get(email_url)
                    if not r_verify.ok:
                        print("Verifying {} failed".format(email_url))
    else:
        print("Fetching inbox for {} failed".format(email))


async def run(name, country, contestant_id, contestant_name):
    name = name.lower()
    email = "{}@{}".format(name, provider)
    print("{} voting with email {} for {} : {}".format(
        name, email, contestant_name, contestant_id))
    while do_vote(name, email, country, contestant_id, contestant_name):
        print('E-mail sent for verification for {}'.format(email))
    else:
        print('E-mail limit reached for {}'.format(email))

    verify_vote(name)


async def run_all(word_file, country, contestant_id, contestant_name):
    with open(word_file) as f:
        names = f.read().splitlines()
        tasks = [
            asyncio.ensure_future(
                run(name, country, contestant_id, contestant_name))
            for name in names
        ]
        await asyncio.wait(tasks)


if __name__ == '__main__':
    word_file = "nepali-names.txt"
    contestant_id = 25
    country = 'US'
    contestant_name = 'Menuka'
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(
        run_all(word_file, country, contestant_id, contestant_name))
    ioloop.close()
