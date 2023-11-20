from flask import Flask, render_template, request, redirect, url_for, session
import random
import string

app = Flask(__name__)
# Change this to a random secret key in production
app.secret_key = 'your_secret_key'

# Dictionary to store game rooms
game_rooms = {}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/create_room', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        # Generate a unique game code
        code = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=6))
        game_rooms[code] = {'players': []}
        # Redirect to the game room
        return redirect(url_for('game_room', code=code))
    return render_template('create_room.html')


@app.route('/join_room', methods=['GET', 'POST'])
def join_room():
    if request.method == 'POST':
        code = request.form['code']
        if code in game_rooms:
            # Redirect to the existing game room
            return redirect(url_for('game_room', code=code))
        else:
            # Add logic here for handling invalid code, e.g., showing an error message
            return render_template('join_room.html', error="Invalid room code.")
    return render_template('join_room.html')


@app.route('/room/<code>')
def game_room(code):
    if code in game_rooms:
        # Handle the game room logic here
        return render_template('game_room.html', code=code)
    else:
        # Redirect to home if room code does not exist
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
