import webapp2
import urllib
from google.appengine.api import mail
from google.appengine.api import taskqueue
import wards

WEB_FORM = """\
<html>
  <head>
    <title>Ward Wiz</title>
  </head>
  <body>
    <h1>Ward Wiz</h1>
    <p>This service looks up the wards for Minneapolis street addresses,
       and returns the results by email. </p>
    <p>Results may take several minutes to arrive, so please be patient.</p>
    <p><strong>Tips:</strong> Include the house number, street name, and direction.<p>
    <p>Do not include apartment number, city, state, or zip code.</p> 
    <p>This service uses the 
    <a href="http://apps.ci.minneapolis.mn.us/AddressPortalApp/?AppID=WardFinderApp">City 
    of Minneapolis ward finder application</a>.</p>
    <form action="/enqueue" method="post">
      <div>Email: <input type="text" name="user"></div>
      <br>
      Enter Minneapolis street addresses (one per line) <br>
      <div><textarea name="streets" rows="20" cols="60" placeholder="2799 1st Ave SE"></textarea></div>
      <div><input type="submit" value="submit"></div>
    </form>
  </body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(WEB_FORM)


class Enqueue(webapp2.RequestHandler):
    def post(self):
        streets = self.request.get('streets')
        user = self.request.get('user')
        taskqueue.add(params={'user': user, 'streets': streets})
        self.redirect('/')

class TaskRunner(webapp2.RequestHandler):
    def post(self):
        user_address = self.request.get('user')
        streets = self.request.get('streets')
        if user_address and streets:
            streets = streets.split('\n')
            output = []
            for street in streets:
                street = street.strip()
                if street:
                    ward = wards.get_ward(street)
                    output.append("%s,%s" % (street, ward))
            sender_address = "dradcliffe@gmail.com"
            subject = "Your ward information"
            body = "\n".join(output)
            mail.send_mail(sender_address, user_address, subject, body)
            # print body


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/enqueue', Enqueue),
    ('/_ah/queue/default', TaskRunner)
], debug=False)
