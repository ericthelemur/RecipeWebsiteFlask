from flask import request
from os.path import join, isfile
import json


def loadJSONFromRequest():
    # Get recipe location
    if "recipe" in request.args:
        rid = request.args["recipe"]
    else:  # If no tag specified, return error
        return "Error: No recipeID field provided. Please specify a recipeID."

    return loadJSON(rid)


def loadJSON(rid):
    # Construct location of recipe json
    location = join("static", "recipes", rid)
    if not location.endswith(".json"): location += ".json"

    if not isfile(location):  # Check json exists
        return "Error: Invalid recipeID field provided. Please specify a valid recipeID."

    # Load data
    with open(location, 'r', encoding="utf8") as recipeJSON:
        data = json.load(recipeJSON)
    return data
