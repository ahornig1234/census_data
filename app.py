from flask import Flask
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>This is my census data analysis</h1>
    
    
#    <img src="http://google.com" />
    <img src="http://loremflickr.com/600/400 />

    """.format(time=the_time)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

#<img src="http://drive.google.com/file/d/0B2h-M49bJOxNRlcwa21FOWlDQ0U/view?usp=sharing" />
