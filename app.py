from flask import Flask, render_template, request, redirect
app = Flask(__name__)

import census_data

from datetime import datetime
@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>This is my census data analysis</h1>
    
    <p>Here is a random cat:</p>
    <img src="http://loremflickr.com/600/400" />
    
    <p>Here is a pdf file from the analysis, hosted from google drive:</p>
    <iframe src="https://drive.google.com/file/d/0B2h-M49bJOxNUlVnR29tQzhLVWc/preview" width="600" height="400"></iframe>

    <p>Here is a pdf file from the analysis, hosted from plot.ly:</p>
    <iframe width="450" height="400" frameborder="0" scrolling="no" src="//plot.ly/~andrew.hornig/8.embed"></iframe>
    
    """.format(time=the_time)

    census_data.makeplots()

if __name__ == "__main__":
#    app.run(debug=True)
    app.run(debug=True, use_reloader=True)

