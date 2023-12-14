from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from .models import BookDetails, BookCategory


@csrf_exempt
def create_book(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            category_name = data.get('category')
            category, _ = BookCategory.objects.get_or_create(name=category_name)

            BookDetails.objects.create(
                title=data.get('title'),
                author=data.get('author'),
                publication_date=datetime.strptime(data.get('publication_date'), "%Y-%m-%d").date(),
                genre=data.get('genre'),
                availability_status=data.get('availability_status'),
                category=category
            )

            return JsonResponse({'message': 'Book created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def delete_book(request, book_id):
    book = get_object_or_404(BookDetails, book_id=book_id)
    if request.method == 'DELETE':
        try:
            book.delete()
            return JsonResponse({'message': 'Book deleted successfully'}, status=200)
        except BookDetails.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def update_book(request, book_id):
    book = get_object_or_404(BookDetails, book_id=book_id)
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            category_name = data.get('category')
            category, created = BookCategory.objects.get_or_create(name=category_name)

            if created:
                book.title = data.get('title')
                book.author = data.get('author')
                book.publication_date = datetime.strptime(data.get('publication_date', str(book.publication_date)),
                                                          "%Y-%m-%d").date()
                book.genre = data.get('genre')
                book.availability_status = data.get('availability_status')
                book.category = category

                book.save()
                return JsonResponse({'message': 'Book updated successfully'}, status=200)
        except BookDetails.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


@csrf_exempt
def filter_books(request):
    if request.method == 'GET':
        category_name = request.GET.get('category')
        try:
            if category_name:
                try:
                    category = BookCategory.objects.get(name=category_name)
                    category_id = category.category_id
                except BookCategory.DoesNotExist:
                    pass

            if category_id:
                books = BookDetails.objects.filter(category_id=category_id)

            else:
                books = BookDetails.objects.all()

            book_list = []

            for book in books:
                book_data = {
                    'book_id': book.book_id,
                    'title': book.title,
                    'author': book.author,
                    'publication_date': str(book.publication_date),
                    'genre': book.genre,
                    'availability_status': book.availability_status,
                    'category': book.category.name
                }
                book_list.append(book_data)

            return JsonResponse({'books': book_list}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

