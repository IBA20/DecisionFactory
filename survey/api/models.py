import uuid

from django.db import models
from datetime import date


class Survey(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    start_date = models.DateField(blank=False, default=date.today)
    end_date = models.DateField(blank=False)
    owner = models.ForeignKey('auth.User', related_name='surveys', on_delete=models.CASCADE)

    class Meta:
        ordering = ['start_date']


class Question(models.Model):
    number = models.SmallIntegerField(blank=False, default=0)
    text = models.TextField(blank=True, default='')
    type = models.SmallIntegerField(choices=[(1, 'text box'), (2, 'single choice'), (3, 'multiple choice')],
                                    blank=False, default=1)
    source = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)

    class Meta:
        ordering = ['number']


class Option(models.Model):
    number = models.SmallIntegerField(blank=False, default=0)
    text = models.TextField(blank=True, default='')
    toquestion = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)

    class Meta:
        ordering = ['number']


class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Answer(models.Model):
    text = models.TextField(blank=True, default='')
    questionId = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, related_name='answers', on_delete=models.CASCADE)
