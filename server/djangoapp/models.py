from django.db import models
from django.utils.timezone import now
import requests


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = 1
    SUV = 2
    WAGON = 3
    TYPES = (
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON'),
    )
    maker = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealerId = models.IntegerField()
    name = models.TextField()
    type = models.IntegerField(choices = TYPES, max_length = 256)
    year = models.DateField()

    def __str__(self):
        return self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data

class DealerReview:

    def __init__(self, id_review, dealership, name, purchase, review, purchase_date=None, car_make=None, car_model=None, car_year=None, sentiment=None):
        # Review id
        self.id = id_review
        # Dealership id
        self.dealership = dealership
        # Reviewer name
        self.name = name
        # Reviewer has purchased
        self.purchase = purchase
        # Reviewer review
        self.review = review
        # Reviewer purchase date
        self.purchase_date = purchase_date
        # Car Make
        self.car_make = car_make
        # Car Model
        self.car_model = car_model
        # Car Year
        self.car_year = car_year
        # Reviewer sentiment
        self.sentiment = sentiment

    """def __str__(self):
        return "Review name: " + self.name """