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

@app.route('/blog', methods=['POST', 'GET'])
def index():
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
        # TODO: create better error display using flash 
        title_error = ""
        body_error = ""
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(blog_title, blog_body)
        if blog_title ==  "":
            title_error = "Need a title"
        if blog_body == "":
            body_error = "Need a body"
        # no errors, post blog, redirect to blog
        if not title_error and not body_error:
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog')
        else:
            return render_template("newpost.html", title = "New Post",
            title_error = title_error, body_error = body_error)
    return render_template("newpost.html", title="New Post")


if __name__ == '__main__':
    app.run()