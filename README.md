# Lab5

# python3 flaskHttpServer.py

# Apple> 
# curl -X POST -H "Content-Type: application/json" -d "{\"name\":\"Alice\",\"URI\":\"http://good.site.com\"}" http://localhost:5000/add-subscriber
# curl -X POST -H "Content-Type: application/json" -d "{\"name\":\"Bob\",\"URI\":\"http://bob.com\"}" http://localhost:5000/add-subscriber
# curl -X POST -H "Content-Type: application/json" -d "{\"name\":\"Carole\",\"URI\":\"http://carole.com\"}" http://localhost:5000/add-subscriber
 
# Apple> 
# curl http://localhost:5000/list-subscribers
# Apple> 
# curl -X DELETE -H "Content-Type: application/json" -d "{\"name\":\"Bob\"}" http://localhost:5000/delete-subscriber
#
