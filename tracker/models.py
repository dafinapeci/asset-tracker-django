from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    role = models.CharField(max_length=20, default='USER')

    def __str__(self):
        return self.name

class Asset(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    tag_number = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, default='AVAILABLE')

    def __str__(self):
        return f"{self.name} ({self.tag_number})"

class CheckoutLog(models.Model):
    # ForeignKeys are the Django equivalent of @ManyToOne
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    checkout_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='PENDING')

    def __str__(self):
        return f"{self.asset.name} requested by {self.user.name}"