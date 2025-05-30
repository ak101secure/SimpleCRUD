import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Book

@csrf_exempt

def book_list(request):
    if request.method == 'GET':
        books = list(Book.objects.values())
        return JsonResponse(books, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        book = Book.objects.create(
            title=data['title'],
            author=data['author'],
            published_date=data['published_date']
        )
        return JsonResponse({'id': book.id, 'message': 'Book created'}, status=201)

    return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt

def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'published_date': book.published_date.isoformat()
        })

    elif request.method == 'PUT':
        data = json.loads(request.body)
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.published_date = data.get('published_date', book.published_date)
        book.save()
        return JsonResponse({'message': 'Book updated'})

    elif request.method == 'DELETE':
        book.delete()
        return JsonResponse({'message': 'Book deleted'})

    return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])
