# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import base64
import random  
# Start your middleware class
class ProxyMiddleware(object):
    proxy_list = [
                  ("http://125.65.0.173:24884", ""),
                  ("http://223.90.177.176:12213",""),
                  ("http://111.73.19.139:23727",""),
                  ("http://183.33.40.217:27701",""),
                  ("http://116.209.61.60:29434",""),
                  ("http://14.212.120.80:12942", ""),
                  ("http://182.207.107.157:28510",""),
                  ("http://125.79.149.150:20224",""),
                  ("http://125.79.149.150:20224",""),
                  ("http://106.123.211.172:26018",""),
                  ("http://222.140.144.164:13323",""),
                  ("http://180.160.166.228:22452",""),
                  ("http://112.7.121.38:19948",""),
                  ("http://36.56.46.56:18245",""),
                  ("http://221.202.20.81:16232",""),
                  ]
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        idx = random.randint(0, (len(self.proxy_list)-1));
        request.meta['proxy'] = self.proxy_list[idx][0]
          
        # Use the following lines if your proxy requires authentication
        proxy_user_pass = self.proxy_list[idx][1]#"USERNAME:PASSWORD"
        
        if proxy_user_pass:
            # setup basic authentication for the proxy
            encoded_user_pass = base64.encodestring(proxy_user_pass)
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
