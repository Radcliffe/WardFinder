import webapp2
import urllib
from google.appengine.api import urlfetch
from google.appengine.api import mail
from google.appengine.api import taskqueue
import wards

WEB_FORM = """\
<html>
  <body>
    <form action="/enqueue" method="post">
      <div>Email:<input type="text" name="user"></div>
      <br>
      Enter Minneapolis street addresses (one per line) <br>
      <div><textarea name="streets" rows="20" cols="60"></textarea></div>
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
    

class TaskRunner(webapp2.RequestHandler):
    def post(self):
        user_address = self.request.get('user')
        streets = self.request.get('streets').split('\n')
        output = []
        for street in streets:
            street = street.strip()
            if street:
                ward = wards.lookup_address(street)
                output.append("%s, %s" % (street, ward))
        sender_address = "dradcliffe@gmail.com"
        subject = "Your ward information"
        body = "\n".join(output)
        mail.send_mail(sender_address, user_address, subject, body)


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/enqueue', Enqueue),
    ('/_ah/queue/default', TaskRunner)
], debug=True)