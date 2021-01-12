from flask import Flask, Blueprint, flash,  redirect, render_template, request, url_for
from flask import render_template

from app import searcher

bp = Blueprint('main', __name__)

@bp.route('/', methods=['POST','GET'])
def index():
  if request.method == 'POST':
    media_type = request.form['watching']
    title = request.form['movie']
    persons = searcher.search(title)
    return render_template('result.html', persons=list(persons.values())[:3], title=title)
  return render_template('index.html')

