import json
from flask import Flask, request, redirect, url_for, render_template
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
    question = db.Column(db.String(250), nullable=True)
    taboo_words = db.Column(db.String(250), nullable=True)
    clue_giver = db.Column(db.String(50), nullable=True)
    guesser = db.Column(db.String(50), nullable=True)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def home():
    return render_template('home.html')


def load_questions():
    with open('questions.json') as f:
        data = json.load(f)
    return data["questions"]


@app.route('/create_room', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        questions = load_questions()
        selected_question = random.choice(questions)

        code = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=6))
        new_room = GameRoom(code=code, question=selected_question["content"], taboo_words=",".join(
            selected_question["tabooWords"]))
        new_room.clue_giver = request.remote_addr
        # new_room.guesser = request.remote_addr
        db.session.add(new_room)
        db.session.commit()
        return redirect(url_for('game_room', code=code))
    return render_template('create_room.html')

# ... [rest of your routes and logic] ...


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


@app.route('/room/<code>', methods=['GET', 'POST'])
def game_room(code):
    room = GameRoom.query.filter_by(code=code).first()
    if room:
        player_role = "guesser" if request.remote_addr == room.guesser else "clue_giver"
        print(player_role)
        if request.method == 'POST':
            if player_role == "clue_giver":
                room.question = request.form.get('question')
                taboo_words_list = room.taboo_words.split(
                    ',') if room.taboo_words else []
                print("clue giver")

            else:
                room.guess = request.form.get('guess')
                taboo_words_list = room.taboo_words.split(
                    ',') if room.taboo_words else []
                print("guessor")

            print(taboo_words_list)
            db.session.commit()
        return render_template('game_room.html', room=room, taboo_words=taboo_words_list)
    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
