from flask import request, render_template, redirect, url_for, session
from flask_login import login_required, logout_user

from golf import app, login_manager
from golf.models import User
from golf.utils import login_custom_func, get_events, add_mail, send_appeal


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_get'))


@app.route('/add_mail/', methods=['POST'])
def mail():
    if add_mail():
        session['mail_obj'] = True
        session.modified = True
    return redirect(url_for('main_get'))


@app.route('/join_request/', methods=['POST'])
@app.route('/appeal/', methods=['POST'])
def appeal():
    send_appeal()
    return redirect(url_for('main_get'))


@app.route('/', methods=['GET', 'POST'])
def main_get():
    if request.method == 'POST':
        if not login_custom_func():
            return redirect(url_for('main_get'))
    return render_template('index.html', events=get_events())


@app.route('/events/')
def events():
    return render_template('event-listing.html')


@app.route('/events/detail/')
def events_detail():
    return render_template('event-detail.html')
