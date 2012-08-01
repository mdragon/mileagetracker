import os
import datetime
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template

import webapp2

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
    
editApp = webapp2.WSGIApplication(
                                     [('/edit/delete', Delete),
                                     ('/edit/.*', Edit),
                                     ],
                                     debug=True)