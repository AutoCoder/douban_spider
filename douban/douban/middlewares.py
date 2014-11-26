# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import base64
import random
from proxy.proxyfactory import proxyfactory

# Start your middleware class
class ProxyMiddleware(object):
    def __init__(self):
        self.proxy_list = proxyfactory.GetFreeProxylist()
        
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        proxy = random.choice(self.proxy_list)
        
        request.meta['proxy'] = proxy['http']
        # Use the following lines if your proxy requires authentication
        proxy_user_pass = ""#"USERNAME:PASSWORD"
        
        if proxy_user_pass:
            # setup basic authentication for the proxy
            encoded_user_pass = base64.encodestring(proxy_user_pass)
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
