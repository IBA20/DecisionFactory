from rest_framework import generics, permissions, status
from rest_framework.response import Response

from . import serializers
from django.contrib.auth.models import User
from .models import Survey, Answer, Participant
from .permissions import IsOwnerOrReadOnly
from datetime import date


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class SurveyList(generics.ListCreateAPIView):
    serializer_class = serializers.SurveyLstSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Survey.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ActiveSurveyList(generics.ListAPIView):
    queryset = Survey.objects.filter(end_date__gte=date.today(), start_date__lte=date.today())
    serializer_class = serializers.ActiveSurveySerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SurveyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Survey.objects.all()
    serializer_class = serializers.SurveySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class ParticipantCreate(generics.CreateAPIView):
    serializer_class = serializers.ParticipantSerializer


class AnswerList(generics.ListCreateAPIView):

    def get_queryset(self):
        participant = Participant.objects.get(id=self.kwargs['pk'])
        return Survey.objects.filter(questions__answers__participant=participant).distinct()

    def perform_create(self, serializer):
        serializer.save(participant=Participant.objects.get(id=self.kwargs['pk']))

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.SurveyAnswerSerializer
        elif self.request.method == 'POST':
            return serializers.AnswerSerializer

    def post(self, *args, **kwargs):
        participant = Participant.objects.get(id=self.kwargs['pk'])

        # duplicate answers protection:
        verifieddata = [answer for answer in self.request.data if
                        not Answer.objects.filter(questionId=answer['questionId'], participant=participant).exists()]

        serializer = serializers.AnswerSerializer(data=verifieddata, many=True)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
