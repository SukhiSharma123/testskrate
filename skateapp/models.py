from django.db import models

from account.models import User

STATUS_CHOICE = {
    ('open','open'),
    ('close','close'),
}
PRIORITY_CHOICE = {
    ('low','low'),
    ('medium','medium'),
    ('high','high'),
}
# Create your models here.
class Tickets(models.Model):
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICE, default='low')
    assignedTo = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='employee_user')
    createdAt = models.DateField(auto_now_add=True)