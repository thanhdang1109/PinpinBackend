from django.db import models
from datetime import datetime

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
    timezone = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.country)


class Street(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    suburb = models.CharField(max_length=255, null=True, blank=True)
    state = models.ForeignKey(State, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    def __str__(self):
        return "{}, {}, {}".format(self.name, self.city, self.country)


class Address(models.Model):
    number = models.CharField(max_length=10, blank=True)
    street = models.ForeignKey(Street)
    zipcode = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return "{}, {}".format(self.number, self.street)


# + -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --+
# Organization & School


class Organization(models.Model):
    name = models.CharField(max_length=400)
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class School(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City)

    def __str__(self):
        return self.name


class Degree(models.Model):
    name = models.CharField(max_length=400)
    school = models.ForeignKey(School)

    def __str__(self):
        return "{} - {}".format(self.name, self.school)


# + -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --+
# User info


class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=200, unique=True)
    firstname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255, blank=True)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    street = models.ForeignKey(Street, blank=True)
    city = models.ForeignKey(City, blank=True)
    country = models.ForeignKey(Country)
    password = models.CharField(max_length=50)
    facebook_token = models.CharField(max_length=600, blank=True, null=True)

    def __str__(self):
        return "{}, {} {} {}, {}, \
                {} {} {}".format(self.username, self.firstname,
                                 self.middlename, self.lastname,
                                 self.email, self.street,
                                 self.city, self.country)


class Education(models.Model):
    user = models.ForeignKey(User)
    degree = models.ForeignKey(Degree, blank=True)
    year = models.CharField(choices=YEAR_CHOICES,
                            max_length=4, default=str(thisYear))

    def __str__(self):
        return "{}, {}, {}".format(self.user, self.degree, self.year)


class Skill(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User_Skill(models.Model):
    user = models.ForeignKey(User)
    skill = models.ForeignKey(Skill)
    description = models.TextField(blank=True)

    def __str__(self):
        return "{}, {}, {}".format(self.skill,
                                   self.user.username,
                                   self.description)

    def display_user(self):
        return self.user.username

    display_user.short_description = 'User'
    display_user.allow_tags = True


class Experience(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    month_start = models.CharField(choices=MONTH_CHOICES,
                                   default=str(thisMonth),
                                   max_length=2, blank=True)
    year_start = models.CharField(choices=YEAR_CHOICES,
                                  default=str(thisYear),
                                  max_length=4, blank=True)
    month_end = models.CharField(choices=MONTH_CHOICES,
                                 default=str(thisMonth),
                                 max_length=2, blank=True)
    year_end = models.CharField(choices=YEAR_CHOICES,
                                default=str(thisYear),
                                max_length=4, blank=True)

    def __str__(self):
        return "{}, {} at {} ({}-{} to {}-{}) is {}".format(self.user.username,
                                                            self.title,
                                                            self.organization,
                                                            self.month_start,
                                                            self.year_start,
                                                            self.month_end,
                                                            self.year_end,
                                                            self.description)


class Video_Education(models.Model):
    education = models.ForeignKey(Education)
    storage_link = models.URLField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}, video {} stored at {}".format(self.education,
                                                  self.created,
                                                  self.storage_link)


class Video_Skill(models.Model):
    skill = models.ForeignKey(Skill)
    storage_link = models.URLField()
    created = models.DateTimeField(auto_now_add=True)


class Video_Experience(models.Model):
    experience = models.ForeignKey(Experience)
    storage_link = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
