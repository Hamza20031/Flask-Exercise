from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


blog_posts = [
    {
        'id': 1,
        'author': 'Author Name',
        'title': 'Title of the Blog Post',
        'content': 'Content of the blog post...'
    }
]
with open('blog_posts.json', 'w') as file:
    json.dump(blog_posts, file, indent=4)


@app.route('/')
def index():
    with open(blog_posts, 'r') as file:
        blog_info = json.load(file)
    return render_template('index.html', posts=blog_info)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        new_post = {
            'id': len(blog_posts) + 1,
            'author': author,
            'title': title,
            'content': content
        }
        blog_posts.append(new_post)
        return redirect(url_for('index'))
    return render_template('add.html')


def find_post_by_id(post_id):
    for post in blog_posts:
        if post['id'] == post_id:
            return post


@app.route('/delete/<int:post_id>')
def delete(post_id):
    post = find_post_by_id(post_id)
    blog_posts.remove(post)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post_to_update = find_post_by_id(post_id)
    if post_to_update is None:
        return "Post not found", 404
    if request.method == 'POST':
        post_to_update['title'] = request.form.get('title')
        post_to_update['content'] = request.form.get('content')
        return redirect(url_for('index'))

    return render_template('update.html', post=post_to_update)


@app.route('/like/<int:id>')
def like(post_id):
    post_to_like = find_post_by_id(post_id)

    if post_to_like is None:
        return "Post not found", 404
    post_to_like['likes'] += 1
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
