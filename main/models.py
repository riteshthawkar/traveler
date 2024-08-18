from django.db import models

# Create your models here.
    

class TravelGuide(models.Model):
    city_name = models.CharField(max_length=50)
    country_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    activities = models.JSONField(blank=True, null=True)
    tips = models.JSONField(blank=True, null=True)
    img = models.ImageField(upload_to="uploads", blank=True, null=True)

    def __str__(self):
        return self.city_name


class Tourist_Place(models.Model):
    place_name = models.CharField(max_length=100)
    description = models.TextField()
    travel_guide = models.ForeignKey(TravelGuide, on_delete=models.CASCADE)

    def __str__(self):
        return self.place_name


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=100)
    description = models.TextField()
    travel_guide = models.ForeignKey(TravelGuide, on_delete=models.CASCADE)

    def __str__(self):
        return self.restaurant_name


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=100)
    description = models.TextField()
    travel_guide = models.ForeignKey(TravelGuide, on_delete=models.CASCADE)

    def __str__(self):
        return self.hotel_name


class Emergency_Contact(models.Model):
    entity = models.CharField(max_length=50)
    value = models.TextField()
    travel_guide = models.ForeignKey(TravelGuide, on_delete=models.CASCADE)

    def __str__(self):
        return self.entity


class Tour_Package(models.Model):
    package_name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=50)
    duration = models.IntegerField()
    cost = models.IntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    places_to_visit = models.JSONField()
    hotels = models.JSONField()
    restaurants = models.JSONField()
    activities = models.JSONField()
    tips = models.JSONField()
    timeline = models.JSONField()
    emergency_contacts = models.JSONField()
    reviews = models.JSONField(blank=True, null=True)
    img = models.ImageField(upload_to="uploads", blank=True, null=True)

    def __str__(self):
        return self.package_name + " - "+ self.country
    

class Blog(models.Model):
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    content = models.TextField()
    heading = models.TextField(max_length=200, blank=True, null=True)
    img = models.ImageField(upload_to="uploads", blank=True, null=True)

    def __str__(self):
        return self.city + " - " + self.country
    




class Visa_Assitance(models.Model):
    country = models.CharField(max_length=50)
    overview = models.TextField()
    visa_types = models.JSONField()
    visa_requirements = models.JSONField()
    visa_process = models.JSONField()
    additional_info = models.JSONField()
    faqs = models.JSONField()
    img = models.ImageField(upload_to="uploads", blank=True, null=True)

    def __str__(self) -> str:
        return self.country
    
# class Chat_History(models.Model):


    