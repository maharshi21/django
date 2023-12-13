import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item


@csrf_exempt
def item_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item = Item.objects.create(name=data.get('name'), description=data.get('description'))
            response_data = {'id': item.id, 'name': item.name, 'description': item.description}
            return JsonResponse({'data': response_data}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)


@csrf_exempt
def item_delete(request, item_id):
    if request.method == 'DELETE':
        try:
            item = Item.objects.get(id=item_id)
            item.delete()

            return JsonResponse({'message': 'Item deleted successfully'}, status=200)
        except Item.DoesNotExist:

            return JsonResponse({'error': 'Item not found'}, status=404)
    else:

        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def item_update(request, item_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            item = Item.objects.get(id=item_id)

            if 'name' in data:
                item.name = data['name']

            if 'description' in data:
                item.description = data['description']

            item.save()
            response_data = {'name': item.name, 'description': item.description}
            return JsonResponse({'data': response_data}, status=200)
        except Item.DoesNotExist:

            return JsonResponse({'error': 'Invalid request method'}, status=404)

    else:
        return JsonResponse({'error': 'invalid request method'}, status=405)


@csrf_exempt
def filter_data(request):
    if request.method == 'POST':
        try:
            data = request.POST
            name = data.get('name', '')
            description = data.get('description', '')

            filtered_data = Item.objects.filter(
                name__icontains=name,
                description__icontains=description,

            )

            input_data = [{'name': item.name, 'description': item.description} for item in filtered_data]

            return JsonResponse({'data': input_data}, status=200)

        except Exception as e:

            return JsonResponse({'error': str(e)}, status=500)
    else:

        return JsonResponse({'error': 'Invalid request method'}, status=405)
