# Intended to grab data from Twitter and DisTimo API's

import urllib, urllib2, base64, json;

	#Twitter


#	consumer_key = "GcdcbHCbK46WXJTwyREvNg";
#	consumer_secret = "rzC4eHex44IWqbX22xRbCDqllvGtV9IpPTuy57t2s";


#	key_sec = consumer_key + ":" + consumer_secret;
#	encoded = "Basic " + base64.standard_b64encode(key_sec);

#	url = "https://api.twitter.com/oauth2/token";
#	http_headers = {"Authorization":encoded,"Content-Type":"application/x-www-form-urlencoded;charset=UTF-8","User-Agent":"twit_analysis"};
#	http_body = {"grant_type":"client_credentials"};

#	post_data_encoded = urllib.urlencode(http_body);
#	request_object = urllib2.Request(url, post_data_encoded, http_headers);

#	response = urllib2.urlopen(request_object);
#	html_string = response.read();

bearer_token = "Bearer " + "AAAAAAAAAAAAAAAAAAAAALMRRQAAAAAAYTLf3c7X0d8CVEO%2FmBWBq8Z1qcU%3D4zPZWN1xSXYFVoZm4xVruOcja5xOBX7OyPSOusDqgA"

url = "https://api.twitter.com/1.1/search/tweets.json?q=%23yahoo&count=100&lang=en&page=1"
all = set()

request_object = urllib2.Request(url)
request_object.add_header("Authorization",bearer_token)
response = urllib2.urlopen(request_object);
json_string = response.read();
json_dict = json.loads(json_string)
tweet_list = json_dict[u"statuses"]



for x in range(len(tweet_list)):
	all.add(tweet_list[x][u"text"])

url = "https://api.twitter.com/1.1/search/tweets.json?q=%23yahoo&count=100&lang=en&page=2"

request_object = urllib2.Request(url)
request_object.add_header("Authorization",bearer_token)
response = urllib2.urlopen(request_object);
json_string = response.read();
json_dict = json.loads(json_string)
tweet_list = json_dict[u"statuses"]

for x in range(len(tweet_list)):
	all.add(tweet_list[x][u"text"])


print len(all)
