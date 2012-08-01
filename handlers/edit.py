import datetime
import logging
import os
import webapp2

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template

import models

class Edit(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        key = self.request.get('key')
        if user == None:
            self.redirect(self.request.relative_url(users.create_login_url("/Edit?key=" + key)))
            return
           
        if users.is_current_user_admin() == False:
            self.redirect("/?not-admin")
            return
    
        if key != "":
            entry = db.get(key)
        else:
            entry = models.Entry()

        if entry.is_saved():
            key = entry.key()
            entry.prettyDate = entry.date.strftime('%m/%d/%y')
        else:
            key = ""
    
        template_values = {
            'entry': entry,
            'key': key,
            'admin': users.is_current_user_admin(),
            'login_link': users.create_login_url(self.request.url),
            'logout_link': users.create_logout_url('/'),
            'user': users.get_current_user()
        }
        
        path = os.path.join(os.path.dirname(__file__), '../views/edit.html')
        #self.response.out.write(path)
        self.response.out.write(template.render(path, template_values))	
    
    def post(self):
        if users.is_current_user_admin() == False:
            self.redirect("/?not-admin")
            return
        
        key = self.request.get('key')
        if key != "":
            entry = db.get(key)
        else:
            entry = models.Entry()
        
        if( len(self.request.get('date').strip().split(' ')) > 1 ):
            entry.date =  datetime.datetime.strptime(self.request.get('date'), '%Y-%m-%d %H:%M:%S')
        else:
            entry.date =  datetime.datetime.strptime(self.request.get('date'), '%m/%d/%y')
        entry.gallons = float(self.request.get('gallons'))
        entry.cost = float(self.request.get('cost'))
        entry.miles = int(self.request.get('miles'))
        entry.estimate = (self.request.get('estimate') == 'checked')
        entry.location = self.request.get('location')
        entry.cpg = entry.calc_cpg()
        entry.mpg = None

        car = models.Car.all().filter('default = ', True).fetch(1)[0]
        entry.car = car
        db.put(entry)
        key = str(entry.key())

        self.redirect(self.request.relative_url("/edit/?key=" + key))
        #path = os.path.join(os.path.dirname(__file__), '../views/edit.html')
        #self.response.out.write(path)
        #self.response.out.write(template.render(path, template_values))
        
class Delete(webapp2.RequestHandler):
    def get(self):
        if users.is_current_user_admin() == False:
            self.redirect("/")
            return
        
        key = self.request.get('key')
        if key != "":
            entry = db.get(key)

        if entry != None and entry.is_saved():
            db.delete(key)
            
        self.redirect("/?delete")
    
class Migration1(webapp2.RequestHandler):
    def get(self):
        if len(models.Car().all().fetch(999)) > 0:
            logging.debug('skipping migration there are already Cars in the datastore')
            return
        
        c = models.Car()
        c.name = '09 Civic'
        c.make = 'Honda'
        c.model = 'Civic'
        c.year = '2009'
        c.leaseStart = datetime.datetime.strptime('2009-08-01','%Y-%m-%d').date()
        c.leaseEnd = datetime.datetime.strptime('2012-06-29','%Y-%m-%d').date()
        
        c.put()
        
        entries = models.Entry.all()
        es = entries.fetch(999)
        logging.debug('setting car on ' + str(len(es)) + ' entities')
        for e in es:
            e.car = c
            e.put()
        
        c = models.Car()
        c.name = '12 Accord'
        c.make = 'Honda'
        c.model = 'Accord'
        c.year = '2012'
        c.startingMiles = 105
        c.leaseStart = datetime.datetime.strptime('2012-06-29','%Y-%m-%d').date()
        c.leaseEnd = datetime.datetime.strptime('2015-06-29','%Y-%m-%d').date()
        c.default = True
        
        c.put()
        
editApp = webapp2.WSGIApplication(
                                     [('/edit/delete', Delete),
                                     ('/edit/migration1', Migration1),
                                     ('/edit/.*', Edit),
                                     ],
                                     debug=True)