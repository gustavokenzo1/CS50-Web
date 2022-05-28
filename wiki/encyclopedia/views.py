import random
from django.shortcuts import render, redirect
from django import forms

import markdown2

from . import util


class SearchForm(forms.Form):
    language = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Search for a language', "class": 'search'}))


class NewPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Title of your new page', "class": "form-title"}))
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={'placeholder': 'Markdown content of your new page', "class": "form-content"}))


class EditPageForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={"class": "form-content"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


def language(request, language):
    try:
        formated = markdown2.markdown(util.get_entry(language))
        return render(request, "encyclopedia/language.html", {
            "language": language,
            "description": formated
        })
    except:
        return render(request, "encyclopedia/language.html", {
            "language": language,
        })


def search(request):
    language = request.POST["language"]
    languageExists = util.entry_exists(language)

    if languageExists:
        return redirect("language", language=language)
    else:
        possibleMatches = []
        for entry in util.list_entries():
            if language in entry:
                possibleMatches.append(entry)
            elif language.lower() in entry.lower():
                possibleMatches.append(entry)
            elif language.capitalize() in entry.capitalize():
                possibleMatches.append(entry)
            elif language.upper() in entry.upper():
                possibleMatches.append(entry)

        return render(request, "encyclopedia/search.html", {
            "entries": possibleMatches,
            "language": language
        })


def error(request):
    return render(request, "encyclopedia/error.html")


def new_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        if not util.entry_exists(title):
            util.save_entry(title, content)
            return redirect("language", language=title)
        else:
            error = "Page already exists"
            return redirect("error")

    return render(request, "encyclopedia/new_page.html", {
        "newPageForm": NewPageForm()
    })


def edit(request, language):
    if request.method == "POST":
        content = request.POST["content"]

        util.save_entry(language, content)
        return redirect("language", language=language)

    return render(request, "encyclopedia/edit_page.html", {
        "language": language,
        "editPageForm": EditPageForm(initial={"content": util.get_entry(language)})
    })


def random_page(request):
    entries = util.list_entries()
    return redirect("language", language=random.choice(entries))
