from flask import Flask, request, jsonify, render_template
from os.path import join
from os import getcwd
from pathlib import Path

import RecipePageRenderer
import RecipeJSONHandler

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("frontpage.html")


@app.route('/recipe', methods=["GET"])
def recipePage():
    recipeJSON = RecipeJSONHandler.loadJSONFromRequest()
    if isinstance(recipeJSON, str): return recipeJSON
    return RecipePageRenderer.render("recipe.html", request.args["recipe"], recipeJSON)


@app.route('/api/v1/recipes', methods=["GET"])
def recipeAPI():
    data = RecipeJSONHandler.loadJSONFromRequest()
    # Convert it to flask json
    return jsonify(data)


@app.route('/printall', methods=["GET"])
def printAll():
    p = Path('static/recipes')
    comb = ""
    for file in p.glob('**/*.json'):
        file = ("\\".join(str(file).split("\\")[2:]))[:-5]
        recipeJSON = RecipeJSONHandler.loadJSON(file)
        if isinstance(recipeJSON, str): continue
        comb += RecipePageRenderer.render("print.html", file.replace("\\", "/"), recipeJSON) + "\n"
    return comb


def setup():
    RecipePageRenderer.constructDropDowns(join(getcwd(), "static", "recipes"))


setup()
if __name__ == '__main__':
    app.run(debug=True, host='localhost')