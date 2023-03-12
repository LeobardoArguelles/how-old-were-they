from flask import Flask, Blueprint, flash,  redirect, render_template, request, url_for
from flask import render_template

from . import searcher

bp = Blueprint('main', __name__)


@bp.route('/', methods=['POST','GET'])
def index():
    """
    Página principal. Permite buscar una serie o película para conocer
    la edad de sus actores y actricess.
    """
    if request.method == 'POST':
        media_type = request.form['watching']
        title = request.form['media']
        options = searcher.search_options(title, media_type)

        # if persons is None:
        #     # No se encontró la película
        #     return render_template('notfound.html', title=title)
        return render_template('options.html', options=options)

    return render_template('index.html')

@bp.route('/search', methods=['POST'])
def show_data():
    id = request.form["id"]
    media_kind = request.form["media"]
    characters, title = searcher.search(id, media_kind)

    persons = []
    for char_name, person in characters.items():
        persons.append(person)

    return render_template('result.html', persons=persons[:5], title=title, is_movie=media_kind=="movie")
