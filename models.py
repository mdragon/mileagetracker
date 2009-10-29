import datetime
from google.appengine.ext import db

class Entry(db.Model):
    date = db.DateTimeProperty()
    miles = db.IntegerProperty()
    gallons = db.FloatProperty()
    cost = db.FloatProperty()
    entered = db.DateTimeProperty(auto_now_add=True)
    location = db.StringProperty()
    mpg = db.FloatProperty()
    cpg = db.FloatProperty()
   
    def calc_cpg(self):
        return self.cost/self.gallons
        
    def calc_mpg(self, prior):
        return (self.miles - prior.miles)/self.gallons
        
    def jstime(self):
        d3 = self.date - datetime.datetime(1970,1,1)
        return ((d3.days * 86400000000) + (d3.seconds + 1000000) + d3.microseconds)/1000
