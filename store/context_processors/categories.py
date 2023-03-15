from store.models import Category


def get_category(request):
    return {'categories': Category.objects.filter(level=0)}
