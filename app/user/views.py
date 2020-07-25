from django.utils import timezone
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import (UserSerializer,
                          UserLoginSerializer,
                          UserAnaliticsQueryParamsSerializer)
from core.models import Like


class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'User registered  successfully',
        }

        return Response(response, status=status_code)


class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token': serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class UserProfileView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'id': self.request.user.id,
                    'email': self.request.user.email,
                    'name': self.request.user.name,
                    'last_login': self.request.user.last_login,
                    'last_activity': self.request.user.last_activity,
                    }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)


class UserAnaliticsView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get_dates_from_valid_data(self, valid_data):
        date_from = valid_data.get('date_from')
        date_to = valid_data.get('date_to')
        today = timezone.now()
        if not date_from:
            date_from = '2020-01-01'
        if not date_to:
            date_to = today
        return date_from, date_to

    def get(self, request):
        query_params_serializer = UserAnaliticsQueryParamsSerializer(
            data=request.query_params)
        if not query_params_serializer.is_valid():
            return Response({'errors': query_params_serializer.errors})
        validated_data = query_params_serializer.validated_data
        date_from, date_to = self.get_dates_from_valid_data(validated_data)
        statistics = Like.objects.filter(
            created__gte=date_from,
            created__lte=date_to,
            user_id=self.request.user.id
        ).count()

        return Response(
            {
                "user": self.request.user.email,
                "date_from": date_from,
                "date_to": date_to.strftime("%Y-%m-%d"),
                "likes": statistics
            }
        )
