from rest_framework import serializers
from .models import User, City, Rule, Property, PropertyImage, Booking, Review
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# --- ПОЛЬЗОВАТЕЛИ И АВТОРИЗАЦИЯ ---

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'avatar']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Создаем пользователя через специальный метод для хеширования пароля
        return User.objects.create_user(**validated_data)

    def to_representation(self, instance):
        # Генерируем токены сразу после регистрации
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'id': instance.id,
                'username': instance.username,
                'role': instance.role,
                'email': instance.email
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверный логин или пароль")

    def to_representation(self, instance):
        # Генерируем токены при успешном входе
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'id': instance.id,
                'username': instance.username,
                'role': instance.role
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

# --- ГОРОДА И ИЗОБРАЖЕНИЯ ---

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['image', 'is_main']

# --- ОБЪЯВЛЕНИЯ (PROPERTY) ---

class PropertyListSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source='city.name', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = ['id', 'title', 'price_per_night', 'city', 'image', 'property_type']

    def get_image(self, obj):
        img = obj.images.filter(is_main=True).first()
        if img and img.image:
            return img.image.url
        return None

class PropertyDetailSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    city = CitySerializer(read_only=True) # Более детально через вложенный сериализатор
    images = PropertyImageSerializer(many=True, read_only=True)
    rules = serializers.SlugRelatedField(many=True, read_only=True, slug_field='rules_name')

    class Meta:
        model = Property
        fields = '__all__'

class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'city', 'price_per_night',
            'address', 'property_type', 'max_guests',
            'bedrooms', 'bathrooms', 'rules'
        ]

# --- БРОНИРОВАНИЕ И ОТЗЫВЫ ---

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['guest'] # Гость берется из request.user в методе perform_create

class ReviewSerializer(serializers.ModelSerializer):
    guest = serializers.CharField(source='guest.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'property', 'guest', 'rating', 'comment', 'created_at']