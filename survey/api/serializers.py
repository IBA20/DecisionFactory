from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from django.contrib.auth.models import User
from .models import Survey, Question, Option, Answer, Participant


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = ['id', 'number', 'text']


class QuestionSerializer(WritableNestedModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'number', 'text', 'type', 'options']


class SurveySerializer(WritableNestedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    start_date = serializers.ReadOnlyField()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'owner', 'questions']


class SurveyLstSerializer(WritableNestedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'owner', 'questions']


class ActiveSurveySerializer(serializers.ModelSerializer):

    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'start_date', 'end_date']


class UserSerializer(serializers.ModelSerializer):
    surveys = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'surveys']


class ParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant
        fields = ['id']


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['questionId', 'text']


class OptionAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = ['number', 'text']


class QuestionAnswerSerializer(WritableNestedModelSerializer):
    options = OptionAnswerSerializer(many=True, read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['number', 'text', 'type', 'options', 'answers']


class SurveyAnswerSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField()
    description = serializers.ReadOnlyField()
    start_date = serializers.ReadOnlyField()
    end_date = serializers.ReadOnlyField()
    questions = QuestionAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'questions']
