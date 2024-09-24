
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Item, User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import UserSerializer, ItemSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from django.core.cache import cache
from django.contrib.auth import authenticate


class Register(APIView):
    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        cached_user = cache.get(email)
        if cached_user:
            return Response({"message": "User already exists in cache."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "User with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user( first_name=first_name, last_name=last_name, email= email, username=email, password=password)

        # Cache the user email for 5 minutes (to prevent immediate duplicate registration)
        cache.set(email, user.username, timeout=300)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class Login(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)
        if user is not None:

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

import logging

logger = logging.getLogger(__name__)



# View to handle crud operations
class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        cache_key = f'item_{instance.id}'
        cached_item = cache.get(cache_key)

        if cached_item:
            logger.info(f"Retrieved item {instance.id} from cache")
            return Response(cached_item)

        serializer = self.get_serializer(instance)
        cache.set(cache_key, serializer.data, timeout=3600)  # Cache 1 hour
        logger.info(f"Retrieved item {instance.id} from database and cached")
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            logger.info(f"Created new item: {serializer.data['name']}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Failed to create item: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)