import pickle

blog_file = "blog.pkl"

blog_user="miso"
blog_pass='-905124903459320104'


def save_blog(posts):
    with open(blog_file, 'wb') as f:
        pickle.dump(posts, f, pickle.HIGHEST_PROTOCOL)

def load_blog():
    with open(blog_file, 'rb') as f:
        return pickle.load(f)

def add_blog_post(author, title, content, date):
    posts_temp = load_blog()
    posts_temp.insert(0,{'author':author, 'title':title,'content':content,'date':date})
    save_blog(posts_temp)

def delete_blog_post(title):
    posts_temp = load_blog()
    ret = [i for i in posts_temp if not (i['title'] == title)] 
    save_blog(ret)
