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
        return str(self.name)


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
        return f'Car Make: {self.car_make}\nName: {self.name}\n\
            Dealed Id: {self.dealer_id}\nType: {self.type}\n\
            Year: {self.year}'


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer():

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip) -> None:
        self.address = address          # Dealer address       
        self.city = city                # Dealer city
        self.full_name = full_name      # Dealer Full Name
        self.id = id                    # Dealer id
        self.lat = lat                  # Location lat
        self.long = long                # Location long
        self.short_name = short_name    # Dealer short name
        self.st = st                    # Dealer state
        self.state = state              # Dealer state
        self.zip = zip                  # Dealer zip

    def __str__(self) -> str:
        return f'Dealer name: {self.full_name}'
    

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview():
    sentiment = ""
    
    def __init__(self, car_make, car_model, car_year, dealership, id, name, purchase, purchase_date, review) -> None:
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.dealership = dealership
        self.id = id
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review

    def __str__(self) -> str:
        return f'Dealer review: {self.review}'
