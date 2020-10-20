import http.server # SimpleHTTPServer
import json
import argparse
from Motor import Motor
#from Camera import Camera
import io
import base64

# blue, green
left  = Motor("left" , 23, 24)
right = Motor("right", 17, 27)
#camera = Camera("camera", 320,240)

def message_handler(message):
  buffered = io.BytesIO()
  if message['right'] == 'forward':
    right.forward()
  elif message['right'] == 'back':
    right.back()
  elif message['right'] == 'brake':
    right.brake()
  
  if message['left'] == 'forward':
    left.forward()
  elif message['left'] == 'back':
    left.back()
  elif message['left'] == 'brake':
    left.brake()
  
  #if message['camera'] == 'cap':
  #  buffered = camera.capture()

  return buffered

class HTTPHandler( http.server.BaseHTTPRequestHandler):
  def do_POST(self):
    try:
      content_len=int(self.headers.get('Content-length'))
      request = json.loads(self.rfile.read(content_len).decode('utf-8'))
      # process
      cap = message_handler(request)
      #cap_byte = cap.getvalue()
      #cap_base64 = base64.b64encode(cap_byte)
      #cap_str    = cap_base64.decode('utf-8')
      # response
      #response = {'status':200, 'img':cap_str}
      response = {'status':200}
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      response_body = json.dumps(response)
      self.wfile.write(response_body.encode('utf-8'))
    except Exception as e:
      print("ERROR!")
      print(type(e))
      print(e.args)
      print(e)

      response = {'status':500, 'msg':'Failed to handler message.'}
      self.send_response(200)
      self.send_header('Content-type','application/json')
      self.end_headers()
      response_body = json.dumps(response)
      self.wfile.write( response_body.encode('utf-8'))

# argparse
def parse_arg():
  parser = argparse.ArgumentParser("my_parse")
  parser.add_argument('--port','-p',required=False,type=int, default=8000)

  args = parser.parse_args()

  return args.port

def main():

  port = parse_arg()
  server = http.server.HTTPServer(('',port),HTTPHandler)
  server.serve_forever()

if __name__ == '__main__':
  main()
