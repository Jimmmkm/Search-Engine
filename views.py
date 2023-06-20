from flask import Blueprint, render_template, jsonify, request, redirect, url_for
import sys
import os

from utils.search import Search
from bs4 import BeautifulSoup

views = Blueprint(__name__, "views")

search=Search()
allUrl = []

@views.route("/")
def home():
    return render_template("index.html")


@views.route('/results', methods = ['POST'])
def submit_form():
    query = request.form['pay']
    query_list = search._tokenizer.tokenize(query)
    if len(query_list) >= 1:
        results = search.complex_search(query_list)
        search_result = results[0]
        docIDs = results[1]
    else:
        print("Invalid Query")
    rank = 1
    count = 0
    output="<p>"
    current = os.getcwd()
    pt = os.path.join(current, 'WEBPAGES_RAW')
    for url, tfidf in search_result:
        if rank > 20:
            output+="</p>"
        docID = docIDs[count].replace('/', '\\')
        output+="<span style='font-size: 25px'>{rank}</span>. <a style='font-size: 25px' href=http://{url}>{url}</a>".format(rank=rank, url=url)
        
        with open(os.path.join(pt, docID), 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            texts = soup.find_all(text=True)
            clean_text = ''.join(t.text for t in texts)
            content = ' '.join(clean_text.split())
            if len(content)>400:
                content = content[:400]+" ..."
            output+="<br>"
            output+="<span style='font-size: 20px'>"
            output+=content
            output+="</span>"
            output+="<p></p>"
        
        output+="<br>"

        rank += 1
        count += 1
    output+="<p></p>"
    output+="<form action = '/'><input class='btn btn-primary' style='font-size: 20px; margin-left: auto' type='submit' value='Go back to home page'></form>"
    output+="<script src='https://cdnjs.cloudflare.com/ajax/libs/mathjs/10.0.2/math.js' integrity='sha512-U9fwz8ekKht5NdL1x4+Yh3DoXeSrsZ0M7ALcijykvrVKD+101nax1MVdc0wNSVh4GOwZGY7yQpz+rAnnoX7O3Q==' crossorigin='anonymous' referrerpolicy='no-referrer'></script>"
    output+="<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css' rel='stylesheet' integrity='sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3' crossorigin='anonymous'>"
    return output
