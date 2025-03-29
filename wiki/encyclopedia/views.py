from django.shortcuts import render
from django import forms
import markdown
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def show_entry(request, title):
    html_content = markdown.markdown(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {
        "entry": html_content,
        "binary": False if util.get_entry(title) == None else True,
        "title": title,
    })

def search(request):
    if "q" in request.GET:
        query = request.GET['q']
        results = []
        for entry in util.list_entries():
            if query.lower() in entry.lower():
                html_content = markdown.markdown(util.get_entry(entry))
                entry = entry
        return render(request, "encyclopedia/entry.html", {
            "entry": html_content,
            "binary": False if results == None else True,
            "title": entry,
        })
    

def new(request):
    return render(request, "encyclopedia/new.html", {
        "form": NewPageForm()
    })

def save(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            html_content = markdown.markdown(content)
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html", {
                    "error": "Page already exists."
                })
            else:
                util.save_entry(title, html_content)
                return render(request, "encyclopedia/entry.html", {
                    "entry": util.get_entry(title),
                    "binary": False if util.get_entry(title) == None else True,
                    "title": title,
                })
            

def edit(request,title):
    contentt = util.get_entry(title)
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
    return render(request, "encyclopedia/edit.html",{
        "form": EditPageForm(initial={"content": contentt}),
        "title": title,
    })
    

 
          


