# Assuming your models are imported like this:
# from .models import BookDetails, BookCategory

def filter_books(request):
    if request.method == 'GET':
        category_name = request.GET.get('category')
        try:
            # If category name is provided, get the associated category id
            category_id = None
            if category_name:
                try:
                    category = BookCategory.objects.get(name=category_name)
                    category_id = category.category_id
                except BookCategory.DoesNotExist:
                    pass

            # Filter books based on the provided parameters
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
                    'category': book.category.name if book.category else None
                }
                book_list.append(book_data)

            return JsonResponse({'books': book_list}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
