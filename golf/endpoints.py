from flask import request, render_template, redirect, url_for, session
from flask_login import login_required, logout_user

from golf import app, login_manager
from golf.models import User, SiteData, db
from golf.utils import login_custom_func, get_events, add_mail, send_appeal


@app.context_processor
def get_site_data_context_processor():
    site_data = db.get_or_404(SiteData, 1)
    dict_for_return = {'club_name': site_data.club_name,
                       'email': site_data.email,
                       'city': site_data.city,
                       'address': site_data.address,
                       'club_history': site_data.club_history,
                       'work_hours_weekdays': site_data.work_hours_weekdays,
                       'work_hours_weekend': site_data.work_hours_weekend,
                       'url_video_on_main_page': site_data.url_video_on_main_page}
    return dict_for_return


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
