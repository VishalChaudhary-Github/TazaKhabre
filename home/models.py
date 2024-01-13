from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(blank=False, null=False, unique=True)  # Required Field
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'subscriber'
