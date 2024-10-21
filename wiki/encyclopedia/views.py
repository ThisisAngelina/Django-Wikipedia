from django.shortcuts import render

from . import util
import markdown2
from django.http import Http404



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

def custom_404(request, exception): #custom 404 that adheres to the style of the website and is not the standard (ugly) 404 page.
    return render(request, '404.html', {'message': str(exception)}, status=404)