from flask import Flask, render_template, url_for, make_response, redirect, request
from logic import calendar
CALENDAR_FILE_NAME = "raw_calendar.ics"
app = Flask(__name__)

#my_calendar_url = "https://trello.com/calendar/5b7d6f65755e404dfcc59bdb/5b83f1f958983c8d48ce32aa/4415599e33db400f7f6d7dc3ffecb1b5.ics"
#username = "arekszreiber"
mock_calendar_url = "https://trello.com/calendar/50d5db89cb6ffa473500348e/582dc3522bc2feacb52100c0/06f8c212f9b33a77e162d2aef5550213.ics"
mock_username = "maciejjankowski"



@app.route('/', methods=["GET", "POST"])
def route_index():
    if request.method == 'POST':
        usernames = request.args.get('usernames', 'cos,post,nie,tak')
        usernames = usernames.split(',')
    else:
        usernames = None
    return render_template('index.html', usernames=usernames)

@app.route('/load-calendar', methods=["POST"])
def route_load():
    # get calendar url
    calendar_url = request.form.get('calendar-url', '')
    # load calendar
    if calendar.save_from_url(calendar_url, CALENDAR_FILE_NAME):
        # extract usernames
        usernames = calendar.extract_usernames(CALENDAR_FILE_NAME)
        # activate second form and put usernames to it
        usernames = ','.join(usernames)
        # dodać zmienną usernames, jak usernames nie jest none to 2. formularz jest aktywny
        return redirect(url_for('route_index', usernames=usernames), code=307)
    else:
        return redirect(url_for('route_index'))


@app.route('/filtered-calendar.ics', methods=["POST"])
def route_filter():
    #calendar.save_from_url(my_calendar_url, CALENDAR_FILE_NAME)
    #print(request.form)
    username = request.form.get('username', 'nic')
    print(username)
    filtered_calendar = calendar.filter_calendar(username, CALENDAR_FILE_NAME)
    response = make_response(str(filtered_calendar))
    response.headers['content-type'] = "text/calendar; charset=utf-8"
    return response


if __name__ == '__main__':
    app.run(debug=True)
