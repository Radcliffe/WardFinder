import webapp2
import urllib
from google.appengine.api import urlfetch
from google.appengine.api import mail
import wards


class MainPage(webapp2.RequestHandler):
    def get(self):
        address = self.request.get('Address')
        ward = wards.lookup_address(address)
        sender_address = "Ward Wiz <info@ward-wiz.appspot.com>"
        user_address = "dradcliffe@gmail.com"
        subject = "Your ward information"
        body = self.request.get("body")
        mail.send_mail(sender_address, user_address, subject, body)
        self.response.write("Thanks!")


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
