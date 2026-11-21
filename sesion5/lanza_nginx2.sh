docker run --rm -d --network pruebas --name nginx -p 80:80 \
	   -v $(pwd)/html/videojsHLS:/usr/share/nginx/html nginx