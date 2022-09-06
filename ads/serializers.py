from sre_constants import SRE_FLAG_DEBUG
from rest_framework import serializers
from ads.models import Ad, Category, Selection
from users.models import User


class AdListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Ad
        fields = ['Id', 'name', 'category']


class AdDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        required=False,
        slug_field="name",
        queryset=Category.objects.all())
    author = serializers.SlugRelatedField(
        required=False,
        slug_field="username",
        queryset=User.objects.all())

    class Meta:
        model = Ad
        fields = '__all__'


class AdCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.SlugRelatedField(
        required=False,
        slug_field="name",
        queryset=Category.objects.all())
    author = serializers.SlugRelatedField(
        required=False,
        slug_field="username",
        queryset=User.objects.all())

    class Meta:
        model = Ad
        exclude = ['image']

    def is_valid(self, raise_exception=False):
        self._category = self.initial_data.pop('category', None)
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        ad = Ad.objects.create(**validated_data)
        if self._category:
            category_obj = Category.objects.get_or_create(name=self._category)[0]
            ad.category = category_obj
            ad.save()  
            return ad


class AdUpdateSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        required=False,
        slug_field="name",
        queryset=Category.objects.all())
    author = serializers.SlugRelatedField(
        required=False,
        slug_field="username",
        queryset=User.objects.all())


    class Meta:
        model = Ad
        exclude = ['Id', 'image']

    def is_valid(self, raise_exception=False):
        self._category = self.initial_data.pop('category', None)
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        ad = super().save()
        if self._category:
            category_obj = Category.objects.get_or_create(name=self._category)[0]
            ad.category = category_obj
            ad.save()  
            return ad


class AdDestroySerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = '__all__'


class SelectionDetailSerializer(serializers.ModelSerializer):

    items = AdDetailSerializer(many=True)

    owner = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ['id', 'name']


class SelectionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Selection
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
        

class CategoryUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name']


class CategoryDestroySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
