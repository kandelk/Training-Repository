from http.server import BaseHTTPRequestHandler, HTTPServer
import random


def generate_csv():
    header = "created_at,tweet_id,tweet,likes,retweet_count,source,user_id,user_name,user_screen_name,user_description," \
           "user_join_date,user_followers_count,user_location,lat,long,city,country,continent,state,state_code," \
           "collected_at\n"
    random_int = random.randint(1, 59)
    row = "2020-10-15 00:00:" + random_int + "," + random_int + ",Test string " + random_int + ",0.0,0.0,Twitter for iPhone,8.24259601," \
          "Michelle Ferg,MichelleFerg4,,2017-01-25 14:16:17,27.0,,,,,,,,,2020-10-21 00:00:01.553481849"

    return header + row


class HttpProcessor(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()

        self.wfile.write(bytes(generate_csv(), 'utf-8'))


serv = HTTPServer(("", 8080), HttpProcessor)
serv.serve_forever()
