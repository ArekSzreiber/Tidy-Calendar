from requests import get, exceptions
from re import findall, compile, sub

TIDYCAL_URL = 'http://127.0.0.1:5000/'
TRELLO_CAL_URL = 'https://trello.com/calendar/'
EXTENSION = '.ics'

def load_calendar(url):
    """
    :param url: trello calendar url
    :return: calendar as a string
    """
    try:
        r = get(url)
    except exceptions.RequestException as e:
        print(e)
        return False
    return r.text


def extract_usernames(calendar_text):
    regex = compile(r'\(/\w+\)')
    usernames = regex.findall(calendar_text)
    usernames = set(usernames)
    return [x[2:-1] for x in usernames]


def filter_events(calendar_text, username):
    regex = compile(r"BEGIN:VEVENT[\S\s]+?END:VEVENT")
    match = regex.findall(calendar_text)
    filtered_events = [text for text in match if "(/"+username+")" in text]
    return '\n'.join(filtered_events)


def get_calendar_head(calendar_text):
    regex = compile('^[\s\S]*?(?=BEGIN:VEVENT)')
    match = regex.findall(calendar_text)
    return match[0]


def get_calendar_tail():
    return "\nEND:VCALENDAR"


def filter_calendar(calendar_text, username):
    head = get_calendar_head(calendar_text)
    events = filter_events(calendar_text, username)
    tail = get_calendar_tail()
    return head + events + tail


def compose_query_url(calendar_url, username):
    """
    TODO: to ma być adres mojej stronki z query parametrami GET
    Skleja w sensowny sposób url do mojego serwera, które użytkownik wklei do
    kalendarza google
    :param calendar_url: url kalendarza z trello
    :param username: trello username
    :return: url with query parameters to my server
input:
https://trello.com/calendar/5b7d6f65755e404dfcc59bdb/5b83f1f958983c8d48ce32aa/4415599e33db400f7f6d7dc3ffecb1b5.ics
aszreiber
uotput:
http://127.0.0.1:5000/5b7d6f65755e404dfcc59bdb/5b83f1f958983c8d48ce32aa/4415599e33db400f7f6d7dc3ffecb1b5-aszreiber
czyli:
wypierdol https://trello.com/calendar/ oraz .ics (lub .ical) z url
i doklej username, a '-' jest separatorem
    """
    #calendar_url = sub(TRELLO_CAL_URL, '', calendar_url)
    calendar_url = calendar_url.replace(TRELLO_CAL_URL, '')
    calendar_url = sub(r'\.(ics|ical)$', '', calendar_url)
    return TIDYCAL_URL+calendar_url+'-'+username

def decompose_query_url(url):
    """
    rozkłada url na adres url kalendarza i username
    :param url:
    :return: lista [url_kalendarza, trello_username]
    """
    pass







if __name__ == '__main__':
    url = "https://trello.com/calendar/5b7d6f65755e404dfcc59bdb/5b83f1f958983c8d48ce32aa/4415599e33db400f7f6d7dc3ffecb1b5.ics"
    username = "aszreiber"

    print(compose_query_url(url, username))
