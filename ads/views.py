
from django.http import JsonResponse
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from django.views.generic import UpdateView
from ads.models import Category, Ad
from ads.serializers import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from ads.permissions import SelectionUpdateAndDeletePermission, AdminOrModeratorOrAuthor

# Create your views here.
def index(request):
    return JsonResponse({"status": "ok"}, status=200)


class CategoryListView(ListAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(RetrieveAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryCreateView(CreateAPIView):

    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer


class CategoryUpdateView(UpdateAPIView):

    queryset = Category.objects.all()
    serializer_class = CategoryUpdateSerializer


class CategoryDeleteView(DestroyAPIView):

    queryset = Category.objects.all()
    serializer_class = CategoryDestroySerializer



class AdListView(ListAPIView):

    queryset = Ad.objects.all()
    serializer_class = AdListSerializer

    def get(self, request, *args, **kwargs):
		# Фильтр по категории
        category_filter = request.GET.get('category')
        if category_filter:
            self.queryset = self.queryset.filter(category__name__icontains=category_filter)

        # Поиск по тексту
        search_text = request.GET.get('text')
        if search_text:
            self.queryset = self.queryset.filter(name__icontains=search_text)

		# Поиск по городу
        location = request.GET.get('location')
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

		# Диапазон цен
        price_from, price_to = request.GET.get('price_from', ), request.GET.get('price_to')
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):

    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [IsAuthenticated]

class AdCreateView(CreateAPIView):

    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer
    permission_classes = [IsAuthenticated]

class AdUpdateView(UpdateAPIView):

    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [AdminOrModeratorOrAuthor]


class AdDeleteView(DestroyAPIView):

    queryset = Ad.objects.all()
    serializer_class = AdDestroySerializer
    permission_classes = [AdminOrModeratorOrAuthor]


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
	model = Ad
	fields = ['name', 'author', 'price', 'description', 'image', 'is_published', 'category']

	def post(self, request, *args, **kwargs):
		ad = self.get_object()

		ad.image = request.FILES['image']
		ad.save()

		return JsonResponse({
			'id': ad.id,
			'name': ad.name,
			'author': ad.author.username,
			'price': ad.price,
			'description': ad.description,
			'image': ad.image.url if ad.image else None,
			'is_published': ad.is_published,
			'category': ad.category.name,
		}, safe=False)
        
class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer

class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer
    permission_classes = [IsAuthenticated]

class SelectionCreateView(CreateAPIView):

    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated]

class SelectionUpdateView(UpdateAPIView):

    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [SelectionUpdateAndDeletePermission]

class SelectionDeleteView(DestroyAPIView):

    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [SelectionUpdateAndDeletePermission]