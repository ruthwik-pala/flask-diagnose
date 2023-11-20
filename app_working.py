from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_rooms.db'
db = SQLAlchemy(app)


class GameRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(6), unique=True, nullable=False)
    # Add more fields as needed


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/create_room', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        code = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=6))
        new_room = GameRoom(code=code)
        db.session.add(new_room)
        db.session.commit()
        return redirect(url_for('game_room', code=code))
    return render_template('create_room.html')


@app.route('/join_room', methods=['GET', 'POST'])
def join_room():
    if request.method == 'POST':
        code = request.form['code']
        room = GameRoom.query.filter_by(code=code).first()
        if room:
            return redirect(url_for('game_room', code=code))
        else:
            return render_template('join_room.html', error="Invalid room code.")
    return render_template('join_room.html')


@app.route('/room/<code>')
def game_room(code):
    room = GameRoom.query.filter_by(code=code).first()
    if room:
        return render_template('game_room.html', code=code)
    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
