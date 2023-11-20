from flask import Flask, request, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class GameRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(6), unique=True, nullable=False)
    players = db.Column(db.PickleType)  # Stores player identifiers
    clue_giver = db.Column(db.String(50))
    round = db.Column(db.Integer, default=0)
    question = db.Column(db.String(250))
    taboo_words = db.Column(db.String(250))


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
        new_room = GameRoom(code=code, players=[], round=1)
        db.session.add(new_room)
        db.session.commit()
        return redirect(url_for('game_room', code=code))
    return render_template('create_room.html')


@app.route('/join_room', methods=['POST'])
def join_room():
    code = request.form['code']
    room = GameRoom.query.filter_by(code=code).first()
    if room and len(room.players) < 2:
        return redirect(url_for('game_room', code=code))
    return redirect(url_for('home'))


@app.route('/room/<code>')
def game_room(code):
    room = GameRoom.query.filter_by(code=code).first()
    if room:
        # Game logic here
        return render_template('game_room.html', room=room)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
