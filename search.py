import webapp2
import cgi
import urllib
import urllib2
import httplib
import lxml
from urllib2 import urlopen
from google.appengine.api import urlfetch
from lxml import html
from lxml import etree

class ProxyController(webapp2.RequestHandler):

	def doProxy(self, p, urlmethod):
		page = self.response.out

		if p.get('dic', '') == 'naver':
			urlsearch = "http://endic.naver.com/searchAssistDict.nhn"
			values = {'query' : p['q']}
			values_encoded = urllib.urlencode(values)
			req = urllib2.Request(urlsearch, values_encoded)
			result = urllib2.urlopen(req).read()

		else:
			query = '/' + urllib2.quote(p['q'])
			dictionary = '/'

			if p.get('source', '') != '':
				dictionary = dictionary + p['source']

			if p.get('target', '') != '':
				dictionary = dictionary + p['target']

			urlsearch = "http://api.wordreference.com/0.8/d4199/json" + dictionary + query
			result = urlfetch.fetch(url = urlsearch, method = urlmethod).content

		self.response.out.write(result)

	def get(self):
		self.doProxy(self.request.str_GET, urlfetch.GET)

	def post(self):
		self.doProxy(self.request.str_POST, urlfetch.POST)
	
application = webapp2.WSGIApplication([('/sdsearch', ProxyController)],debug=True)
