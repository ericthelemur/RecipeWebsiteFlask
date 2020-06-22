from flask import render_template
from os import listdir
from os.path import isfile, join
import re

import RecipeJSONHandler


def render(template, path, recipeJSON):
    infoJSON = recipeJSON.get("info", {})
    # Path
    path = "/".join(path.split("/")[:-1]) + "/"+infoJSON.get("title", "RECIPE")

    # Serves/Makes
    inp = '<input type="number" placeholder="{serves}" value="{serves}" min="1" name="servingsNumb" id="servingsNumb" class="no-print" style="width: 50px;" onchange="refreshQuantities()"><p id="print-quantities" class="only-print">{serves}</p>'
    if "serves" in infoJSON:    # If serves tag exists, add button for it
        makes = "Serves: " + inp.format(serves=infoJSON.get("serves"))
        if "makes" in infoJSON:     # If make exists as well, add in brackets after
            makes += " (makes " + infoJSON["makes"] + ")"
    else:   # If not serves tag exists, makes tag exists, replace quantity in text with input (i.e. [4] pots -> textfield(4) pots)
        mks = infoJSON.get("makes")
        quantity = re.search(r"\[(\d+)\]", mks) # Get quantity and location of match
        # Insert button formatted with match into makes text
        makes = "Makes: " + mks[0:quantity.start()] + inp.format(serves=quantity.group(1)) + mks[quantity.end():]

    # Ingredients
    ingredients = "<ul>"
    for ingredient in recipeJSON.get("ingredients", []):
        if ingredient.startswith("<h"): ingredients += "</ul>" + ingredient + "<ul>"
        else: ingredients += "<li>" + ingredient + "</li>"
    ingredients += "</ul>"

    # Method
    method = "<ol>"
    for step in recipeJSON.get("method", []):
        if step.startswith("<h"):
            method += "</ol>" + step + "<ol>"
        else:
            method += "<li>" + step + "</li>"
    method += "</ol>"

    # Replace values
    replacements = {
        "path": path,
        "title": infoJSON.get("title", "RECIPE"),
        "serves": makes,
        "prepTime": infoJSON.get("preptime", "-"),
        "cooktime": infoJSON.get("cooktime", "-"),
        "carbs": infoJSON.get("carbs", "-"),
        "ingredients": ingredients,
        "method": method
    }
    return render_template(template, **replacements)


def constructDropDowns(root):
    dd, fp = constructDropDown(root, "")
    with open("templates/navbar.html", "w") as f:
        f.write(dd)

    with open("templates/frontpageList.html", "w") as f:
        f.write(fp)


def constructDropDown(root, subcat):
    dirs = []
    files = []

    subdir = join(root, subcat).replace("/", "\\")

    for f in listdir(subdir):
        if isfile(join(root, subcat, f)): files.append(f)
        else: dirs.append(f)


    ddHTML = ""
    fpHTML = ""

    for dir in dirs:
        ddHTML += '<div class="drop">\n<a class="drop-button">' + dir + '</a>\n<div class="drop-content">\n'
        fpHTML += "<li>"+dir+"<ul>"
        if subcat != "": (dd, fp) = constructDropDown(root, subcat + "/" + dir)
        else: (dd, fp) = constructDropDown(root, dir)
        ddHTML += dd
        fpHTML += fp
        ddHTML += "</div>\n</div>"
        fpHTML += "</ul></li>"

    for file in files:
        if not file.endswith(".json"): continue

        fileJSON = RecipeJSONHandler.loadJSON(subcat + "/" + file)
        if isinstance(fileJSON, str):
            print(fileJSON)
            continue

        buttonText = fileJSON["info"]["title"]

        ddHTML += "<a class='recipeLink' href='/recipe?recipe=" + subcat + '/' + file[:-5] + "'>" + buttonText + "</a>\n"
        fpHTML += "<li><a href='/recipe?recipe=" + subcat + '/' + file[:-5] + "'>" + buttonText + "</a></li>\n"
    return (ddHTML, fpHTML)
