from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:benny@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "secret"


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['GET'])
def index():
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    posted_blog = Blog.query.all()
    return render_template('blog.html',title="My Blog!", 
        posted_blog=posted_blog)

@app.route('/selected_blog', methods=['GET'])
def selected_blog():
    blog_id = request.args.get('id')
    blog_post = Blog.query.filter_by(id=blog_id).first()
    return render_template('selectedblog.html', selected_blog = blog_post)

@app.route('/newpost', methods=['POST', 'GET'])
def new_blog():
    if request.method == 'POST':
        #display errors for if no input in title or body
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(blog_title, blog_body)
        if not blog_title and not blog_body:
            flash ("Please type title and stuff in body")
            return render_template("newpost.html", title="New Post")
        if not blog_title:
            flash ("Please type a title")
            return render_template("newpost.html", title="New Post")
        if not blog_body:
            flash ("Please type stuff in body")
            return render_template("newpost.html", title="New Post")
        else:
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog')
    return render_template("newpost.html", title="New Post")


if __name__ == '__main__':
    app.run()