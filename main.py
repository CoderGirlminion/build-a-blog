from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    #instance variables of the Blog class
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    #Blog constructor with two parameters
    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():
    
    blogs = Blog.query.all()
    return render_template('blog_list.html', blogs=blogs)
         


@app.route('/newpost', methods=['POST', 'GET'])
def entry ():

    if request.method == 'POST':
        title_name = request.form['title-blog']
        text = request.form['body']

        title_error = ''
        body_error = ''

        #object instance create through the Blog constructor
        new_blog = Blog(title_name, text)

        if new_blog.title == '':
            title_error = 'Please enter a title for the blog'
        else:
            new_blog.title=new_blog.title    

        if new_blog.body == '':
            body_error = 'This field is empty'
        else:
            new_blog.body=new_blog.body    

        if not title_error and not body_error:
            db.session.add(new_blog)
            db.session.commit()

            return redirect('/')
        else:
            return render_template('entry.html', title_error=title_error, body_error=body_error)
        
        #get request
    return render_template('entry.html')


@app.route('/blog', methods = ['POST', 'GET'])
def list_blog ():

    if request.method == 'POST':
        blog_id = request.form['blog-id']
        return redirect('/display')

    blogs=Blog.query.all()
    return render_template('blog_list.html', blogs=blogs)


@app.route('/display', methods = ['GET'])
def display():

    blog_id = request.args.get('blog-id')
    blog = Blog.query.get(blog_id)
    return render_template('ind_blog.html', blog=blod)


if __name__ == '__main__':
    app.run()