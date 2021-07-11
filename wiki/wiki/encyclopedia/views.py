from django.shortcuts import render, redirect, reverse
from markdown2 import markdown
from random import randint
from . import util, forms

def index(request):
    return render(request, "encyclopedia/index.html", {                                 # List all entries
        "heading": "All Pages",
        "entries": util.list_entries()
    })

def entry(request, title):
    
    entry = util.get_entry(title)                                                       # Grab entry from disk based on title
    
    if entry:
        return render(request, "encyclopedia/entry.html", {                             # If entry exists, render entry page
        "title": title,
        "entry": markdown(entry)
    })

    return render(request, "encyclopedia/404.html")                                     # If no entry exist, render error page

def random(request):

    entries = util.list_entries()                                                       # Grab all entries
    n = randint(0, len(entries))                                                        # Generate a random integer
    return redirect(reverse("encyclopedia:entry", args=(entries[n-1],)))                # Redirect user to random page    

def search(request):

    if request.method == "GET":
        
        query = request.GET.get('q')                                                    # Grab user query
        query_lower = query.lower()                                                     # Convert user query to lowercase

        entries = util.list_entries()                                                   # Grab list of all entries
        entries_lower = list(map(str.lower, entries))                                   # Lowercase all entry titles

        search_results = []                                                             # If query matches an entry title
        for i in range(len(entries_lower)):                                             # regardless of case, redirect to 
            if query_lower == entries_lower[i]:                                         # entry page
                return redirect(reverse('encyclopedia:entry', args=(entries[i],)))
            elif query_lower in entries_lower[i] or entries_lower[i] in query_lower:    # If query or entry title is a substring
                search_results.append(entries[i])                                       # of one another add to results list
        
        return render(request, "encyclopedia/index.html", {                             # Display search results to user if
            "heading": f"Search Results for {query}",                                   # exact match not found
            "entries": search_results
        })

def add(request):
    
    if request.method == "POST":                                                        # Check request method
        form = forms.NewEntryForm(request.POST)                                         # Populate form instance w/ data from request
        
        if form.is_valid():                                                             # Validate form
            title = form.cleaned_data["title"]                                          # Grab entry title user submitted 
            
            if util.entry_exists(title):                                                # Ensure that another entry with title
                return render(request, "encyclopedia/add.html", {                       # does not exist. If True, display error
                    "form": form,                                                       # to user
                    "error_msg": "Sorry That Title Already Exists... Please choose another :("
                })

            content = form.cleaned_data["content"]                                      # Grab entry content user submitted
            util.save_entry(title, content)                                             # Save new entry to disk
            return redirect(reverse('encyclopedia:entry', args=(title,)))               # Redirect user to new entry page

        return render(request, "encyclopedia/add.html", {                               # If form is invalid, re-render page with
            "form": form,                                                               # existing form information and display
            "error_msg": "Unable to Validate Form."                                     # error to user.
        })
        
        
    return render(request, "encyclopedia/add.html", {                                   # If request method is anything other than
        "form": forms.NewEntryForm(),                                                   # POST, render page with blank form.
        "error_msg": None
    })

def edit(request, title):

    if request.method == "POST":                                                        # If form can be validated, update
        form = forms.EntryForm(request.POST)                                            # content of entry.

        if form.is_valid():
            content = form.cleaned_data["content"]

            util.save_entry(title, content)

            return redirect(reverse("encyclopedia:entry", args=(title,)))
        
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "error_msg": "Unable to Validate Form."
        })

    return render(request, "encyclopedia/edit.html", {                                  # If request method not POST, render page,
        "title": title,                                                                 # with entry content populating edit form                              
        "form": forms.EntryForm(initial={                                        
            'content': util.get_entry(title)
            }),                                            
        "error_msg": None
    })