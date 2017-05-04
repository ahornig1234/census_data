from flask import Flask
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>This is my census data analysisasys</h1>

    <img src="/fig.pdf" />
    """.format(time=the_time)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

