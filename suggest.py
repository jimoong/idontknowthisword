import webapp2
import cgi
import urllib
import urllib2
import httplib
from urllib2 import urlopen
from google.appengine.api import urlfetch

class ProxyController(webapp2.RequestHandler):

	def doProxy(self, p, urlmethod):
		page = self.response.out

		values = {'q' : p['q']}
		values_encoded = urllib.urlencode(values)
		urlsuggest = "http://ac.endic.naver.com/ac?st=11001&r_format=json&r_lt=10001&" + values_encoded
		req = urllib2.Request(urlsuggest)
		result = urllib2.urlopen(req).read()

		self.response.out.write(result)

	def get(self):
		self.doProxy(self.request.str_GET, urlfetch.GET)

	def post(self):
		self.doProxy(self.request.str_POST, urlfetch.POST)
	
application = webapp2.WSGIApplication([('/sdsuggest', ProxyController)],debug=True)
