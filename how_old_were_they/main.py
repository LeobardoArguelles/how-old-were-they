from flask import Flask, Blueprint, flash,  redirect, render_template, request, url_for
from flask import render_template

from how_old_were_they import searcher

bp = Blueprint('main', __name__)

@bp.route('/', methods=['POST','GET'])
def index():
  if request.method == 'POST':
    persons = searcher.search(request.form['movie'])
    return render_template('result.html', persons=list(persons.values())[:3])
  return render_template('index.html')

