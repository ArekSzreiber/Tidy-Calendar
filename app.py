from flask import Flask, render_template, url_for, make_response, redirect, request, session
from logic import calendar
CALENDAR_FILE_NAME = "raw_calendar.ics"
app = Flask(__name__)

app.secret_key = b'\x12\x06\x97O\x8aaw\xadW\x18\xa7\x08%n\x7f\x1a_\xb6\xe03\xf3\xe4\x9f'

"""
TODO pod [Generate link] wpierdolić jakiegoś dziawaskripta, który wpierdoli 
wygenerowany link do inputa [Filtered calendar URL]
"""
@app.route('/', methods=["GET", "POST"])
def route_index():
    if request.method == 'POST':  # show usernames
        usernames = request.args.get('usernames', '')
        usernames = usernames.split(',')
        return render_template('index.html', usernames=usernames)

    if request.method == "GET":
        username = request.args.get('username', False)
        calendar_url = request.args.get('calendar', False)
        if username and calendar_url:  # download a file
            calendar_url = calendar.amplify_calendar_url(calendar_url)
            calendar_text = calendar.load_calendar(calendar_url)
            filtered_calendar = calendar.make_filtered_calendar(calendar_text, username)
            response = make_response(str(filtered_calendar))
            response.headers['content-type'] = "text/calendar; charset=utf-8"
            response.headers['cache-control'] = "no-storage, no-cache, must-revalidate, proxy-revalidate"
            response.headers['etag'] = "filtered-calendar.ics"
            return response
        else:  # show just start page
            return render_template('index.html')


@app.route('/loaded', methods=["POST"])
def route_load():
    calendar_url = request.form.get('calendar-url', '')
    calendar_text = calendar.load_calendar(calendar_url)
    session['calendar_url'] = calendar_url
    if calendar_text:
        usernames = calendar.extract_usernames(calendar_text)
        usernames = ','.join(usernames)
        return redirect(url_for('route_index', usernames=usernames), code=307)
    else:
        return redirect(url_for('route_index'))


@app.route('/filtered', methods=["POST"])
def route_download():
    username = request.form.get('username', '')
    action = request.form.get('action', '')
    calendar_url = session.get('calendar_url', '')
    calendar_url = calendar.compress_calendar_url(calendar_url)
    if action == 'generate':
        generated_url_query_string = request.host_url
        generated_url_query_string += url_for('route_index', username=username, calendar=calendar_url)
        return render_template('index.html',
                               username=username,
                               calendar=calendar_url,
                               output_url=generated_url_query_string)
        #TODO: żeby wstawiało te zmienne w stronę i można było x-ileś razy generowac link za jednym zamachem

        #return redirect(url_for('route_index',
        #                        username=username,
        #                        calendar=calendar_url,
        #                        output_url=generated_url_query_string))
        # query_url = calendar.assemble_query_url(calendar_url, username)
        # return render_template('index.html', output_url=query_url, )
    elif action == 'download':
        return redirect(url_for('route_index', username=username, calendar=calendar_url))
    else:
        return "Błąd"


if __name__ == '__main__':
    app.run(debug=True)
