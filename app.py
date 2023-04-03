import os

from flask import Flask, render_template


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.__static_folder = os.path.join(BASE_DIR, 'static')


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/events/')
def events():
    return render_template('event-listing.html')


@app.route('/events/detail/')
def events_detail():
    return render_template('event-detail.html')
