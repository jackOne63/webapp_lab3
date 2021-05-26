from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
import shortuuid as shortid
from django.db import IntegrityError

# Create your models here.

class Link(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link_to = models.URLField()
    link_from = models.CharField(max_length=10, unique=True)
    counter = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "[%s]:%s -> %s" % (self.user.username, self.link_from, self.link_to[:30])

    def save(self, *args, **kwargs):
        attempt = 0
        if self.link_from != '':
            super().save(*args, **kwargs)
            return
        while True:
            try:
                self.link_from = shortid.uuid()[:8]
                super().save(*args, **kwargs)
                return 
            except IntegrityError as E:
                attempt = attempt + 1
                if attempt == 3:
                    raise E  

class Profile(models.Model):
    GENDERS = (
        ('m', 'Male'),
        ('f', 'Female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=1, choices=GENDERS, default='m')
    birth_date = models.DateField(default=date.today)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()