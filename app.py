from flask import Flask, render_template, url_for, make_response, redirect, request, session
from logic import calendar

app = Flask(__name__)

app.secret_key = b'\x12\x06\x97O\x8aaw\xadW\x18\xa7\x08%n\x7f\x1a_\xb6\xe03\xf3\xe4\x9f'


def make_download_response(filtered_calendar):
    response = make_response(str(filtered_calendar))
    response.headers['content-type'] = "text/calendar; charset=utf-8"
    response.headers['cache-control'] = "no-storage, no-cache, must-revalidate, proxy-revalidate"
    response.headers['etag'] = 'W/"filtered-calendar.ics"'
    return response


@app.route('/', methods=["GET", "POST"])
def route_index():
    if request.method == 'POST':  # show usernames
        usernames = request.args.get('usernames', '')
        usernames = usernames.split(',')
        input_url = request.args.get('input_url', '')
        return render_template('index.html',
                               usernames=usernames,
                               input_url=input_url)

    if request.method == "GET":
        username = request.args.get('username', False)
        calendar_url = request.args.get('calendar', False)
        if username and calendar_url:  # download a file
            calendar_url = calendar.amplify_calendar_url(calendar_url)
            calendar_text = calendar.load_calendar(calendar_url)
            filtered_calendar = calendar.make_filtered_calendar(calendar_text, username)
            return make_download_response(filtered_calendar)
        else:  # just show start page
            return render_template('index.html')


@app.route('/loaded', methods=["POST"])
def route_load():
    calendar_url = request.form.get('calendar-url', '')
    calendar_text = calendar.load_calendar(calendar_url)
    session['calendar_url'] = calendar_url
    if calendar_text:
        usernames = calendar.extract_usernames(calendar_text)
        usernames = ','.join(usernames)
        session['usernames'] = usernames
        return redirect(url_for('route_index',
                                usernames=session['usernames'],
                                input_url=calendar_url
                                ), code=307)
    else:
        return redirect(url_for('route_index'))


@app.route('/filtered', methods=["POST"])
def route_download():
    username = request.form.get('username', '')
    action = request.form.get('action', '')
    input_url = session.get('calendar_url', '')
    calendar_url = calendar.compress_calendar_url(input_url)
    if action == 'generate':
        generated_url_query_string = request.host_url[:-1]  # to skip over trailing slash
        generated_url_query_string += url_for('route_index', username=username, calendar=calendar_url)
        usernames = session.get('usernames', '').split(',')
        return render_template('index.html',
                               username=username,
                               calendar=calendar_url,
                               output_url=generated_url_query_string,
                               input_url=input_url,
                               usernames=usernames)
    elif action == 'download':
        return redirect(url_for('route_index',
                                username=username,
                                calendar=calendar_url))
    else:
        return "Unknown action"


if __name__ == '__main__':
    app.run(debug=True)
