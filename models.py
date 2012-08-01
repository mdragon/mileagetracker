import datetime
from google.appengine.ext import db

class Car(db.Model):
    name = db.StringProperty()
    make = db.StringProperty()
    model = db.StringProperty()
    year = db.StringProperty()
    
    default = db.BooleanProperty()
    leaseStart = db.DateProperty()
    leaseEnd = db.DateProperty()
    startingMiles = db.IntegerProperty()

class Entry(db.Model):
    date = db.DateTimeProperty()
    miles = db.IntegerProperty()
    gallons = db.FloatProperty()
    cost = db.FloatProperty()
    entered = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    estimate = db.BooleanProperty()
    location = db.StringProperty()
    mpg = db.FloatProperty()
    cpg = db.FloatProperty()
    
    car = db.ReferenceProperty(Car)
   
    def calc_cpg(self):
        return self.cost/self.gallons
        
    def calc_mpg(self, prior):
        return (self.miles - prior.miles)/self.gallons
        
    def calc_mpg_miles(self, miles):
        return (self.miles - miles)/self.gallons
        
    def jstime(self):
        d3 = self.date - datetime.datetime(1970,1,1)
        return ((d3.days * 86400000000) + (d3.seconds + 1000000) + d3.microseconds)/1000
