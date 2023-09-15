from Blog.models import Blog
from django.core.paginator import Paginator
from django.shortcuts import render

def searchResults(request):
    query = request.GET.get('search')
    data = Blog.objects.filter(title__icontains=query)
    # paginator = Paginator(data, 4)
    # page = request.GET.get('page')
    # data = paginator.get_page(page)
    context = {'data': data, 'query': query}
    return render(request, 'searchResult.html', context)