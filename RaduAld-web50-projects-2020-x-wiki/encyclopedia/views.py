from django import forms
from django.db import models
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from markdown2 import Markdown

import random
import re
from . import util


def index(request):
    if request.method == "POST":
        q = request.POST["q"]
        s = util.list_entries() 
        for item in s:
            if item.lower() == q.lower():
                return redirect("/wiki/" + item + "/")
        result = util.search_entry(q)      
        return render(request, "encyclopedia/searchresults.html", {
            "result":result
        })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    if request.method == "POST":
        q = request.POST["q"]
        s = util.list_entries() 
        for item in s:
            if item.lower() == q.lower():
                return redirect("/wiki/" + item + "/")
        result = util.search_entry(q)  
        if not result:
            return render(request, "encyclopedia/ersuc.html", {
                "alert": "Error",
                "message": "There were no result.",
            }) 
        return render(request, "encyclopedia/searchresults.html", {
            "result":result
        })
    if request.method == "GET":
        try:
            f = default_storage.open(f"entries/{title}.md")
            content = f.read().decode("utf-8") 
            markdowner = Markdown()
            content = markdowner.convert(content)   
            return render(request, "encyclopedia/page.html", {
                "title":title.capitalize(),
                "message":content
            })
        except FileNotFoundError:
            return render(request, "encyclopedia/ersuc.html", {
                "alert":"Error",
                "message":"The searched wiki page does not exist yet."
            })

def create(request):
    if request.method == "POST":
        if "q" in request.POST:
            q = request.POST["q"]
            s = util.list_entries() 
            for item in s:
                if item.lower() == q.lower():
                    return redirect("/wiki/" + item + "/")
            result = util.search_entry(q)  
            if not result:
                return render(request, "encyclopedia/ersuc.html", {
                    "alert": "Error",
                    "message": "There were no result.",
                }) 
            return render(request, "encyclopedia/searchresults.html", {
                "result":result
            })
        title = request.POST["title"]
        content = request.POST["content"]
        if title != "" and content != "":
            filename = f"entries/{title.capitalize()}.md"
            if default_storage.exists(filename) or default_storage.exists(filename.swapcase()) or default_storage.exists(filename.lower()) or default_storage.exists(filename.upper()):
                return render(request, "encyclopedia/newpage.html", {
                    "alert":"The page you are trying to create already exists.",
                    "title":title,
                    "content":content,
                })
            default_storage.save(filename, ContentFile(content))
            return redirect("/wiki/" + title.capitalize() + "/")
        else:
            return render(request, "encyclopedia/newpage.html", {
                "alert":"Please fill in the form",
                "title":title,
                "content":content,
            })
    return render(request, "encyclopedia/newpage.html")

def edit(request, title):
    if request.method == "POST":
        if "q" in request.POST:
            q = request.POST["q"]
            s = util.list_entries() 
            for item in s:
                if item.lower() == q.lower():
                    return redirect("/wiki/" + item + "/")
            result = util.search_entry(q)  
            if not result:
                return render(request, "encyclopedia/ersuc.html", {
                    "alert": "Error",
                    "message": "There were no result.",
                }) 
            return render(request, "encyclopedia/searchresults.html", {
                "result":result
            })
        elif "content" in request.POST:
            content = request.POST["content"]
            util.save_entry(title, content)
            return redirect("/wiki/" + title + "/")
        else:
            return render(request, "encyclopedia/editpage.html", {
                "alert":"Please fill in the form",
                "title":title,
                "content":content,
            })
    content = util.get_entry(title)
    return render(request, "encyclopedia/editpage.html", {
        "title":title,
        "content":content,
    })

def rdm(request):
    results = util.list_entries()
    result = random.choice(results)
    return redirect("/wiki/" + result + "/")