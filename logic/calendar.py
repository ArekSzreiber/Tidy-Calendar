from requests import get, exceptions
from icalendar import Calendar, Event
from re import findall, compile

CALENDAR_FILE_NAME = "raw_calendar.ics"



def save_from_url(url, output_file_name):
    """
    Saves trello calendar to local file
    :param url: trello calendar url
    :param output_file_name:
    :return: None
    """
    try:
        r = get(url)
    except exceptions.RequestException as e:
        print(e)
        return False

    with open(output_file_name, 'w')as ics_file:
        ics_file.write(r.text)
    return True

def load_calendar_file(calendar_file_name):
    with open(calendar_file_name, "r") as calendar_file:
        return calendar_file.read()


def filter_calendar(trello_username, calendar_file_name):
    source_calendar_text = load_calendar_file(calendar_file_name)
    regex = compile('^[\s\S]*?(?=BEGIN:VEVENT)')
    match = regex.findall(source_calendar_text)
    filtered_calendar = match[0]

    regex = compile(r"BEGIN:VEVENT[\S\s]+?END:VEVENT")
    match = regex.findall(source_calendar_text)
    filtered_events = [text for text in match if "(/"+trello_username+")" in text]
    filtered_calendar += '\n'.join(filtered_events) + "\nEND:VCALENDAR"
    return filtered_calendar



def extract_usernames(calendar_file_name):
    calendar_text = load_calendar_file(calendar_file_name)
    regex = compile(r'\(/\w+\)')
    usernames = regex.findall(calendar_text)
    usernames = set(usernames)
    return [x[2:-1] for x in usernames]



if __name__ == '__main__':

    save_from_url(my_calendar_url, CALENDAR_FILE_NAME)




    filtered_calendar = filter_calendar(username, CALENDAR_FILE_NAME)




