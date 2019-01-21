from requests import get, exceptions
from re import findall, compile, sub

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
    """
    It will not work for cases where there is (/'some text') as a plain text
    To fix in the future
    :param calendar_text:
    :return:
    """
    regex = compile(r'\(/\w+\)')
    usernames = regex.findall(calendar_text)
    usernames = set(usernames)
    return [x[2:-1] for x in usernames]


def filter_events(calendar_text, username):
    """
    Alternatively, icalendar library could be used here.
    In this case I do not need sophisticated calendar processing and regex is enough
    :param calendar_text: string
    :param username: string
    :return: string containing events
    """
    regex = compile(r"BEGIN:VEVENT[\S\s]+?END:VEVENT")
    match = regex.findall(calendar_text)
    filtered_events = [text for text in match if "(/"+username+")" in text]
    return '\n'.join(filtered_events)


def get_calendar_head(calendar_text):
    """
    I retrieve header to append it to returned calendar
    :param calendar_text: ics file as a string
    :return: header as a string
    """
    regex = compile('^[\s\S]*?(?=BEGIN:VEVENT)')
    match = regex.findall(calendar_text)
    return match[0]


def get_calendar_tail():
    """
    required in .ics file ending, without it file parsing doesn't work
    :return: string
    """
    return "\nEND:VCALENDAR"


def make_filtered_calendar(calendar_text, username):
    """
    Removes unmatching events from .ics-like string
    :param calendar_text: string
    :param username: events assigned to this user will remain
    :return: string
    """
    head = get_calendar_head(calendar_text)
    events = filter_events(calendar_text, username)
    tail = get_calendar_tail()
    return head + events + tail


def compress_calendar_url(calendar_url):
    """
    removes part of URL which is common for every Trello calendar
    Would not work if calendar path will change
    :param calendar_url: original calendar URL
    :return: compressed URL, string
    """
    calendar_url = calendar_url.replace(TRELLO_CAL_URL, '')
    return sub(r'\.(ics|ical)$', '', calendar_url)


def amplify_calendar_url(compressed_url):
    """
    adds part of URL which is common for every Trello calendar
    Would not work if calendar path will change
    :param compressed_url: string
    :return: string
    """
    return TRELLO_CAL_URL+compressed_url+EXTENSION

