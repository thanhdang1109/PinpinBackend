from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

thisYear = datetime.now().year
thisMonth = datetime.now().month
YEAR_CHOICES = [(str(y), str(y)) for y in range(1900, thisYear + 5)][::-1]
MONTH_CHOICES = [(str(m), str(m)) for m in range(1, 13)]


# + -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --+
# Location


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=6)
    code = models.CharField(max_length=255)
    country = models.ForeignKey(Country)

    def __str__(self):
        return "{} ({})".format(self.name, self.country)


class City(models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    def __str__(self):
        return "{} ({})".format(self.name, self.country)


class Follower(models.Model):
    user = models.ForeignKey(User, related_name='user')
    follower = models.ForeignKey(User, related_name='followers')
    created = models.DateTimeField(auto_now_add=True)

    def ___str__(self):
        return self.follower.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, null=True, blank=True)

    def get_followers(self):
        followers = list(Follower.objects.filter(
            user=self.user).values('follower_id'))
        return list(followers)

    def get_followings(self):
        following = list(Follower.objects.filter(
            follower=self.user).values_list('user_id', flat=True))
        return list(following)

    def is_following(self, user_id):
        followings = self.get_followings()
        if user_id in followings:
            return True
        else:
            return False

    def is_follower(self, user_id):
        followers = self.get_followers()
        if user_id in followers:
            return True
        else:
            return False


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Video(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    link = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    date = models.CharField(max_length=30)
    description = models.CharField(max_length=140)

    def __str__(self):
        return "Video: {}, {}, {}".format(self.title,
                                          self.user.username,
                                          self.created)
