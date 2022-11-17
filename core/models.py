import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    bvn = models.IntegerField(default=54651333604)
    #password = models.CharField(_('password'), max_length=128, defaults='sha234')
    password = models.CharField(max_length=128, default='sha234')
    location = models.CharField(max_length=200)
    age = models.IntegerField(default=19)
    weight = models.IntegerField(default=130)
    blood_group = models.CharField(max_length=4)
    last_donation = models.DateField(auto_now_add=True)
    wants_to_donate = models.BooleanField(default=True)
    needs_donation = models.BooleanField(default=False)

    def eligible_donate(self):
        now = timezone.now()
        last_donation = now - datetime.timedelta(days=80) <= self.last_donation <= now
        weight = 129 > self.weight
        age = 19 < self.age

        eligibity_checker = [last_donation, weight, age]

        if any(requirement is False for requirement in eligibity_checker):
            return False
        else:
            return True

    def __str__(self):
        return self.name


class Donation_history(models.Model):
    donator = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, related_name='donor_history_set')
    patient = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, related_name='paitent_history_set')
    date = models.DateField(auto_now_add=True)