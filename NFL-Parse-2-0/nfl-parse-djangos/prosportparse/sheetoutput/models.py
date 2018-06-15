from django.db import models
from oauth2client.contrib.django_util.models import CredentialsField
from oauth2client.contrib.django_util.models import FlowField

# Create your models here.
class CredetialsModel(models.Model):
	credential = CredentialsField()

class FlowModel(models.Model):
	flow = FlowField()