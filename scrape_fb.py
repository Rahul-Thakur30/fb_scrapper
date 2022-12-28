from flask import Flask
from facebook_scraper import get_posts
import pandas as pd
import json
app = Flask(__name__)


@app.route('/health')
def health():
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


@app.route('/')
def scrape_fb():
    post_dict = {"post":[],"comments":[],"comments_count":[]}
    for post in get_posts('zomato', pages=5,options={"comments": True},cookies='facebook.com_cookies.txt'):
        try:
            comments = []
            post_dict['post'].append(post['text'])
            post_dict['comments_count'].append(post['comments'])
            for comment in post['comments_full']:
                comments.append(comment.get('comment_text'))
            post_dict['comments'].append(comments)
            
        except Exception as e:
            print(e)
    
    df = pd.DataFrame(post_dict)
    df.to_csv('data/fb_posts.csv')