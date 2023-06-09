from typing import Union

from flask import request, render_template, redirect, url_for, session
from flask_login import login_required, logout_user, current_user

from golf import app, login_manager
from golf.models import User, SiteData, db
from golf.utils import login_custom_func, get_events, add_mail, send_appeal, event_detail, save_settings, new_user, \
    new_event, get_users, delete_user_util, edit_user_util, get_one_user_with_email, delete_event_util, \
    edit_event_util, get_one_event


@app.context_processor
def get_site_data_context_processor() -> dict:
    """
    Контекст-процессор для передачи данных сайта в шаблоны
    """
    site_data = db.get_or_404(SiteData, 1)
    dict_for_return = {'club_name': site_data.club_name,
                       'email': site_data.email,
                       'phone_number': site_data.phone_number,
                       'city': site_data.city,
                       'address': site_data.address,
                       'club_history': site_data.club_history,
                       'work_hours_weekdays': site_data.work_hours_weekdays,
                       'work_hours_weekend': site_data.work_hours_weekend,
                       'url_video_on_main_page': site_data.url_video_on_main_page}
    return dict_for_return


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(int(user_id))


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route('/add_mail/', methods=['POST'])
def mail():
    """
    Запоминает в сессии email, если пользователь авторизовался или иным способом передал свою почту
    """
    if add_mail():
        session['mail_obj'] = True
        session.modified = True
    return redirect(url_for('main'))


@app.route('/join_request/', methods=['POST'])
@app.route('/appeal/', methods=['POST'])
def appeal() -> redirect:
    """
    Эндпоинт для обработки сообщений пользователя (запрос на вступление в клуб или обращение)
    """
    send_appeal()
    return redirect(url_for('main'))


@app.route('/', methods=['GET', 'POST'])
def main() -> Union[redirect, render_template]:
    if request.method == 'POST':
        if not login_custom_func():
            return redirect(url_for('main'))
    return render_template('index.html', events=get_events())


@app.route('/events/')
def events() -> render_template:
    """
    Собирает данные для страницы событий клуба и выводит ее
    """
    upcoming_events = get_events()
    latest_events = upcoming_events[:2]
    return render_template('event-listing.html', latest_events=latest_events, upcoming_events=upcoming_events)


@app.route('/events/detail/<event_id>/')
def events_detail(event_id: int) -> render_template:
    """
    Собирает данные для страницы детального просмотра события и выводит ее
    """
    return render_template('event-detail.html', event=event_detail(event_id))


@app.route('/settings/', methods=['GET', 'POST'])
def site_settings() -> Union[str, redirect, render_template]:
    """
    Реализует вывод данных сайта и их изменение
    """
    if current_user.is_anonymous or not current_user.is_admin:
        return 'You have no rights', 403
    if request.method == 'POST':
        save_settings()
        return redirect(url_for('site_settings'))
    return render_template('settings.html')


@app.route('/admin/', methods=['GET'])
def admin() -> render_template:
    """
    Выводит страницу административного раздела с данными из БД (административный раздел)
    :return:
    """
    users = get_users()
    club_events = get_events()
    return render_template('admin.html', users=users, events=club_events)


@app.route('/admin/create_user/', methods=['GET', 'POST'])
def admin_user() -> Union[redirect, render_template]:
    """
    Реализует вывод формы для создания пользователя и его сохранение в БД (административный раздел)
    """
    if request.method == 'POST':
        new_user()
        return redirect(url_for('admin'))
    return render_template('admin-user.html')


@app.route('/admin/delete_user/<user_id>/')
def delete_user(user_id: int) -> redirect:
    """
    Реализует удаление пользователя (административный раздел)
    """
    delete_user_util(user_id=user_id)
    return redirect(url_for('admin'))


@app.route('/admin/edit_user/<user_id>/', methods=['GET', 'POST'])
def edit_user(user_id: int) -> Union[redirect, render_template]:
    """
    Реализует вывод формы с данными пользователя для изменения (административный раздел)
    """
    if request.method == 'POST':
        edit_user_util(user_id=user_id)
        return redirect(url_for('admin'))
    user, email = get_one_user_with_email(user_id)
    return render_template('admin-user.html', user=user, email=email)


@app.route('/admin/create_event/', methods=['GET', 'POST'])
def admin_events() -> Union[redirect, render_template]:
    """
    Реализует вывод формы для создания нового события и его сохранение в БД (административный раздел)
    :return:
    """
    if request.method == 'POST':
        new_event()
        return redirect(url_for('admin'))
    return render_template('admin-events.html')


@app.route('/admin/delete_event/<event_id>/')
def delete_event(event_id: int) -> redirect:
    """
    Реализует удаление события (административный раздел)
    """
    delete_event_util(event_id)
    return redirect(url_for('admin'))


@app.route('/admin/edit_event/<event_id>/', methods=['GET', 'POST'])
def edit_event(event_id: int) -> Union[redirect, render_template]:
    """
    Реализует вывод формы с данными события для изменения (административный раздел)
    """
    if request.method == 'POST':
        edit_event_util(event_id)
        return redirect(url_for('admin'))
    event = get_one_event(event_id)
    return render_template('admin-events.html', event=event)
