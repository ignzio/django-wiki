import random

from django.shortcuts import render as render, redirect
import markdown2

from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki_entry(request, title):
    title = title.strip()
    wiki = [entry for entry in util.list_entries() if title.lower() in entry.lower()]

    if not wiki or wiki is None:
        return redirect(notFound)

    entry_content = markdown2.markdown(util.get_entry(wiki[0])).strip()
    return render(request, "encyclopedia/wiki/entry.html", {
        'title': title,
        'entry': entry_content
    })


def notFound(request):
    return render(request, "encyclopedia/notfound.html")


def search_entry(request):

    textinput = request.GET.get('q', '')
    sub_string_entries = [entry for entry in util.list_entries() if textinput.lower() in entry.lower()]

    if not sub_string_entries or sub_string_entries is None:
        return redirect(notFound)

    if textinput.lower() == sub_string_entries[0].lower():
        return wiki_entry(request, textinput)

    return render(request, "encyclopedia/index.html", {
        "entries": sub_string_entries,
        "search": True,
        "value": textinput
    })

def make_new_entry(request):
    if request.method == 'POST':
        title = request.POST.get('t', '').strip()
        content = request.POST.get('content','')
        if title.lower() in [entry.lower() for entry in util.list_entries()]:
            return render(request, "encyclopedia/entryalreadyexist.html")
        util.save_entry(title,content)

        return wiki_entry(request,title)
    return render(request, "encyclopedia/newpage.html")

def edit_entry(request,title):

    title = title.strip()
    wiki = [entry for entry in util.list_entries() if title.lower() in entry.lower()]
    if title in util.list_entries():
        return render(request, "encyclopedia/editentry.html",{
            'title' : title,
            'content' :util.get_entry(wiki[0])
        })

def save_edit(request):
    if request.method == 'POST':
        title = request.POST.get('t', '').strip()
        content = request.POST.get('content', '').rstrip()
        util.save_entry(title, content.rstrip())
        return wiki_entry(request, title)
    return render(request, "encyclopedia/notfound.html")

def random_page(request):
    entries = util.list_entries()
    return wiki_entry(request,entries[random.randint(0,len(entries) -1)])