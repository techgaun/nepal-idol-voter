# -*- coding: utf-8 -*-

import asyncio
import requests


def do_vote(name, email, country, contestant_id, contestant_name):
    payload = dict(
        name=name, email=email, country=country, contestant_id=contestant_id)
    r = requests.post('http://ap1.tv/nepalIdol/api/emailVoting', data=payload)
    print(r.text)
    if r.ok:
        response = r.json()
        assert response['status']
        if response['message'].startswith('Maximum voting limit'):
            return False
        assert contestant_name in response['message']
        return True
    return False


async def run(name, email, country, contestant_id, contestant_name):
    print("{} voting with email {} for {} : {}".format(
        name, email, contestant_name, contestant_id))
    if do_vote(name, email, country, contestant_id, contestant_name):
        print('E-mail sent for verification')
    else:
        print('E-mail limit reached')


async def run_all(word_file, country, contestant_id, contestant_name):
    with open(word_file) as f:
        names = f.read().splitlines()
        tasks = [
            asyncio.ensure_future(
                run(name,
                    name.lower() + '@yopmail.com', country, contestant_id,
                    contestant_name)) for name in names
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
