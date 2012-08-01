import os
import datetime
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template

import webapp2

import models

class Main(webapp2.RequestHandler):
  def get(self):

    entries = models.Entry.all()
    entries.order("date")
    
    last = None
    anychange = False
    calcMPG = 0.0
    avgMPG = 0.0
    avgCPG = 0.0
    totalGallons = 0.0
    totalMPG = 0.0
    miles = [
        {'date': datetime.datetime(2012,8,1), 'miles': None, 'lease': 36000, 'jstime': 0}
    ]
    for e in entries:
        change = False
        miles.append({'date': e.date, 'miles': e.miles, 'lease': getLease(e.date), 'jstime': 0})
        
        if e.cpg == None:
            e.cpg = e.calc_cpg()
            change = True

        if last != None:
            calcMPG = e.calc_mpg(last)
            if e.mpg != calcMPG:
                e.mpg = calcMPG
                change = True
        else:
            if e.mpg != 0.0:
                e.mpg = 0.0
                change = True
        
        if change:
            anychange = True
            db.put(e)

        if e.mpg != 0: 
            avgMPG += e.mpg
            totalMPG += 1
        avgCPG += (e.cpg * e.gallons)
        totalGallons += e.gallons
            
        last = e

    if anychange:
        entries = models.Entry.all()
        entries.order("date")
    
    if totalMPG == 0:
        avgMPG = 0
        avgCPG = 0
    else:
        avgMPG = avgMPG/totalMPG
        avgCPG = avgCPG/totalGallons
        
    for m in miles:
        m['jstime'] = jstime(m['date'])
    miles.sort()

    template_values = {
      'entries': entries,
      'avgMPG': avgMPG,
      'avgCPG': avgCPG,
      'admin': users.is_current_user_admin(),
      'login_link': users.create_login_url(self.request.url),
      'logout_link': users.create_logout_url('/'),
      'user': users.get_current_user(),
      'miles': miles
      }

    path = os.path.join(os.path.dirname(__file__), '../views/main.html')
    self.response.out.write(template.render(path, template_values))	

def jstime(date):
    d3 = date - datetime.datetime(1970,1,1)
    return ((d3.days * 86400000000) + (d3.seconds + 1000000) + d3.microseconds)/1000

def getLease(date):
    d3 = date - datetime.datetime(2009,8,1)
    return 36000/(3*365)* d3.days
    
mainApp = webapp2.WSGIApplication(
                                     [('/', Main)],
                                     debug=True)