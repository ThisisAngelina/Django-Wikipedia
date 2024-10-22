from django.shortcuts import render, redirect 
import re
import random
import markdown2
from django.http import Http404

from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#variables : title, content
def read_entry(request, title):
    try: 
        md = util.get_entry(title) #get title from the url, use the pre-made function to obtain the requested entry from the set of existing entries .
        content = markdown2.markdown(md)# convert md into HTML using markdown2. NOTE had to add the 'safe' ttribute to my DTL varuable 'content' to have the HTML template render the HTML correctly
        return render(request, "encyclopedia/read_entry.html", {'content': content, 'title': title})
    except:
        raise Http404("This entry does not exist") #deal with the case where the requested entry does not exist


#searching for an entry through the search bar
#have the form POST to the 'search' route to distinguish it from the 'create_entry' view.

def search(request):
    if request.method == 'POST':
        term = request.POST.get('search_form') #escaping special characters, just in case 
        print('the search term is', term)
        if term and term != "": #if a search term exists and it is not an empty string:
            #get the list of entries
            entries = util.list_entries()
            matched_entries = [] #prepare a list to hold partial matches

            #looping over existing entries
            for entry in entries:
                #if it is a complete entry name (CASE-INCENSITIVE), send the user to the exact page
                if re.fullmatch(term, entry, re.IGNORECASE):
                    print("there was a full match")
                    return redirect('read_entry', title=entry)
           
            #else if if it a partial match, send the user to the list of possible matches. Clicking on any of the entry names on the search results page should take the user to that entry’s page.
                elif re.search(term, entry, re.IGNORECASE):
                    matched_entries.append(entry)
                    print("there was a partial match")
                
            #after we finish looping through the existing entries, redierect to the list of matches. if the list is empty, redict to the home page.
            if len(matched_entries) > 0:
                return render(request,'encyclopedia/search_results.html', {'matched_entries' : matched_entries}) 
            else: #there are no matches - #TODO display an alert 
                message = "Oops there seems to be no such entry. But there are these ones that might interest you:"
                return render(request, 'encyclopedia/index.html', {'message' : message,  "entries": util.list_entries()})
        #else - the search term was empty or not valid
        else:
            return redirect('index')
            


#allow users to create and save their own wiki entries
def create_entry(request):
    #if the form has been submitted:
    if request.method == 'POST':
        title = request.POST.get('title')
        content =  request.POST.get('content')
        #preparing the list of existing enty titles (needed to ensure that the user does not create a duplicate of an existing entry)
        existing_titles = util.list_entries()
        print('existing titles are', existing_titles)
        #if the entry title or the entry content are missing, redirect the user to the same page with a message
        if not title or not content:
            message = "Oops! An entry title and content are required!"
            return render(request, 'encyclopedia/create_entry.html', {'message' : message})
        #if an encyclopedia entry already exists with the provided title, the user is presented with an error message and is redirected back to same page to try submitting the form again
        elif title in existing_titles:
            message = "Oops! An entry with this title already exists!"
            return render(request, 'encyclopedia/create_entry.html', {'message' : message})
        else: #if all goes well - save the entry and redirect the user to the new entry’s page.
            util.save_entry(title,content)
            return redirect('read_entry', title=title)
    #if the request method is GET and the user just wants to see the form
    else:
        return render(request, 'encyclopedia/create_entry.html')


# edit existing entries

# access a random entry
def read_random(request):
    existing_entries = util.list_entries()
    index = random.randint(0, len(existing_entries)-1)
    chosen_entry = existing_entries[index]
    print("the title of the chosen entry is", chosen_entry)
    md = util.get_entry(chosen_entry) #get title from the url, use the pre-made function to obtain the requested entry from the set of existing entries .
    content = markdown2.markdown(md)# convert md into HTML using markdown2. NOTE had to add the 'safe' ttribute to my DTL variable 'content' to have the HTML template render the HTML correctly
    return render(request, "encyclopedia/read_entry.html", {'content': content, 'title': chosen_entry})


def custom_404(request, exception): #custom 404 that adheres to the style of the website and is not the standard (ugly) 404 page.
    return render(request, '404.html', {'message': str(exception)}, status=404)

