from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=20, default='Car make name')
    description = models.CharField(null=True, max_length=1000)
    
    def __str__(self) -> str:
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
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon')
    ]
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30, default='Car model name')
    dealer_id = models.IntegerField(null=False, default=0)
    type = models.CharField(null=False, max_length=5, choices=CAR_TYPES, default=SEDAN)
    year = models.DateField(null=False, default=now)
    
    def __str__(self) -> str:
        return f'Car Make: {self.car_make}\nName: {self.name}\nDealed Id: {self.dealer_id}\nType: {self.type}\nYear: {self.year}'


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
