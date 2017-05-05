from flask import Flask
from datetime import datetime
app = Flask(__name__)

import census_data

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>This is my census data analysis</h1>
    
    <p>Here is a random cat:</p>
    <img src="http://loremflickr.com/600/400" />
    
    <p>Here is a pdf file from the analysis, hosted from google drive:</p>
    <iframe src="https://drive.google.com/file/d/0B2h-M49bJOxNUlVnR29tQzhLVWc/preview" width="600" height="400"></iframe>


    """.format(time=the_time)

    census_data.makeplots()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
