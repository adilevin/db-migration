import sys
import os

port = int(sys.argv[1])

os.chdir('nginx-1.9.9/nginx-1.9.9/conf')

config = """
worker_processes  1;
events {}
http {
	server {
		listen 5000;
		server_name host1 localhost;
		location / {
			proxy_pass http://127.0.0.1:%i/;
		}
  }
}
""" % port

f = file('nginx.conf','wt')
f.write(config)
f.close()

f = file('nginx.conf','rt')
s = f.read()
print s
f.close()