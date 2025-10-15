from flask import Flask, request, jsonify

'''
This lab's goal is to give us understanding of how the HTTP protocol works in conjunction with
a publish-subscribe pattern. We will do this with Python Flask.
Basic requirements
1. All subscribers are stored in the HTTP server.
2. There is one endpoint for adding a subscriber - each subscriber is a name and a URI
3. There is one endpoint for deleting subscribers - supplying only the subscriber's name
4. There is one endpoint for returning a list of subscribers and their URIs
5. There is one endpoint for updating the published subject and notifying all subscribers
  a. The notifications can be print statements on the backen
  b. The backend should be run in one terminal and another terminal should be used
     for testing with curl
'''

# Define the Flask app
app = Flask(__name__)

subscribers = {}

def home():
  return "Hello from Flask!"

@app.route('/', methods=['GET'])
def root():
  print(f"Hello at the root")
  return jsonify({'main endpoint':'Ack'})


# Listing Subscriber - returning a list of subscribers and their URLs
@app.route('/list-subscribers', methods=['GET'])
def listSubscribers():
  return jsonify(subscribers)
'''
 Windows> curl.exe -X POST -H "Content-Type: application/json" -d "{\"name\":\"Alice\",\"URI\":\"http://good.site.com\"}" http://localhost:5000/add-subscriber
 Apple> 
 curl -X POST -H "Content-Type: application/json" -d "{\"name\":\"Alice\",\"URI\":\"http://alice.com\"}" http://localhost:5000/add-subscriber
 curl -X POST -H "Content-Type: application/json" -d "{\"name\":\"Bob\",\"URI\":\"http://bob.com\"}" http://localhost:5000/add-subscriber
 curl -X POST -H "Content-Type: application/json" -d "{\"name\":\"Carole\",\"URI\":\"http://carole.com\"}" http://localhost:5000/add-subscriber
 Apple> 
 curl http://localhost:5000/list-subscribers
 Apple> 
 curl -X DELETE -H "Content-Type: application/json" -d "{\"name\":\"Bob\"}" http://localhost:5000/delete-subscriber

'''


# Adding Subscriber  – each subscriber is a name and a URL
@app.route('/add-subscriber', methods=['POST'])
def addSubscriber():
  data = request.json
  name = data.get('name')
  URI = data.get('URI')
  #Edge Case
  if not name or not URI:
    return jsonify({'error': 'Both name and URI are required'})
  

  #Edge Case Duplicate Name
  if name in subscribers:
    return jsonify({'error': f'Subscriber with name "{name}" already exists'})


  subscribers[name] = URI
  print(f"You entered: Name={name}, Address={URI}")
  return jsonify({'message': f'You sent name: {name} and address: {URI}'})

# Deleting Subscriber – supplying only the subscriber's name
@app.route('/delete-subscriber', methods=['DELETE'])
def deleteSubscriber():
  data = request.json
  name = data.get('name') 

  #Edge Case 
  if not name:
    return jsonify({'error': 'Name is required to delete a subscriber'}), 400

  #Add Edge Case if list is empty
  if not subscribers:
    return jsonify({'error': 'Subscriber list is empty — nothing to delete \_(-_-)_/ '}), 404

  #Edge Case if name is not in the list
  if name not in subscribers:
    return jsonify({'error': f'Subscriber "{name}" not found'})


  del subscribers[name]
  print(f"You deleted: Name={name}")
  return jsonify({'message': f'You deleted name: {name} sussessfully'})


# Updating the published subject and notifying all subscribers
# fix code
@app.route('/update-and-notify', methods=['POST'])
def updateAndNotifyAllSubscribers():
  data = request.json
  subject = data.get('subject-update')
  print(f"You updated the subject to: {subject}")

  for key in subscribers.keys():
    print(f"Notigying {key} at {subscribers[key]} of the new subject: {subject} ")
  return jsonify({'message': f'You updated subject to {subject}'})





'''
@app.route('/update-subscriber', methods=['PUT'])
def updateSubscriber():
  data = request.json
  subject = data.get('subject')
  print(f"Publishing update: {subject}")
  print("Notifying all subscribers:")

  #Notification
  for name, uri in subscribers.items():
    print(f" Notifying {name} at {uri} with subject: '{subject}'")
    return jsonify({'message': f'Update "{subject}" published to {len(subscribers)} subscribers'})
'''


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)