from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('track.html')  # Référencez track.html ici

if __name__ == '__main__':
    app.run(debug=True,port=5000)
