from flask import Flask, Blueprint, flash,  redirect, render_template, request, url_for
from flask import render_template

from app import searcher

bp = Blueprint('main', __name__)

@bp.route('/', methods=['POST','GET'])
def index():
  if request.method == 'POST':
    media_type = request.form['watching']
    title = request.form['movie']
    persons, real_title = searcher.search(title, media_type)
    return render_template('result.html', persons=list(persons.values())[:10], title=real_title, is_movie=True if media_type == "movie" else False)
  return render_template('index.html')

