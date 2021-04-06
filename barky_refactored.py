#BRYAN FUDALA - CIDM 6330 - ASSIGNMENT 4 BARKY REFACTORED
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from markupsafe import escape
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookmarks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class bookmarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(80), nullable=False)  
    notes = db.Column(db.String(120), nullable=True)
    date_added = db.Column(db.String, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Bookmark %r>' % self.id
        
#@app.route('/')
#def hello_world():
 #   return 'Hello, World!'

#https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
@app.route("/")
def index():
    bookmark = bookmarks.query.all()
    return render_template("index.html", bookmark=bookmark)


#add a new bookmark - TESTING WORKS
@app.route('/addurl', methods=("GET", "POST"))
def addurl():
    if request.method == "POST":

        title = request.form['title']
        url = request.form['url']
        notes = request.form['notes']
        date_added = datetime.utcnow().isoformat()

        bookmark_x = bookmarks(title=title,url=url,notes=notes,date_added=date_added)

        try:
            db.session.add(bookmark_x)
            db.session.commit()
            return redirect('/')
        except:
            flash("error occured")
    return(render_template("addurl.html"))

#DELETE URL- TESTING WORKS!
@app.route("/deleteurl/<int:id>", methods=("GET", "POST"))
def deleteurl(id):
    if request.method == "POST":
     bookmark_delete = bookmarks.query.get_or_404(id)   
     db.session.delete(bookmark_delete)   
     db.session.commit()
     return redirect("/")


#https://flask.palletsprojects.com/en/1.1.x/tutorial/views/
#https://docs.sqlalchemy.org/en/14/core/dml.html
#Edits the bookmark - TESTING WORKS 
@app.route('/<int:id>/editurl', methods=("GET", "POST"))
def editurl(id):
    bookmark_edit = bookmarks.query.get_or_404(id)
    

    if request.method == 'POST':
        title_scrape= request.form['title']
        url_scrape = request.form['url']
        notes_scrape = request.form['notes']

        if title_scrape is not None:
            bookmark_edit.title = title_scrape
        if title_scrape is not None:
            bookmark_edit.url = url_scrape
        if title_scrape is not None:
            bookmark_edit.notes = notes_scrape

        db.session.commit()
        return redirect('/')
   
    return(render_template("editurl.html", bookmark=bookmark_edit))

if __name__ == '__main__':
    app.run(debug=True)
    


     







    



    
        
        





