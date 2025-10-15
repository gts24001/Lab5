# import required modules
import unittest
import flaskHttpServer

class FlaskHttpServerTestCase(unittest.TestCase):
	def setUp(self):
		flaskHttpServer.app.config['TESTING'] = True
		self.client = flaskHttpServer.app.test_client()
		# Reset subscribers before each test
		flaskHttpServer.subscribers.clear()

	def test_root_endpoint(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertIn('main endpoint', response.get_json())

	def test_list_subscribers_empty(self):
		response = self.client.get('/list-subscribers')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.get_json(), {})

	def test_add_subscriber_success(self):
		data = {'name': 'Alice', 'URI': 'http://alice.com'}
		response = self.client.post('/add-subscriber', json=data)
		self.assertEqual(response.status_code, 200)
		self.assertIn('message', response.get_json())
		# Check if subscriber was added
		self.assertIn('Alice', flaskHttpServer.subscribers)

	def test_add_subscriber_missing_fields(self):
		response = self.client.post('/add-subscriber', json={'name': 'Bob'})
		self.assertIn('error', response.get_json())
		response = self.client.post('/add-subscriber', json={'URI': 'http://bob.com'})
		self.assertIn('error', response.get_json())

	def test_add_subscriber_duplicate(self):
		data = {'name': 'Alice', 'URI': 'http://alice.com'}
		self.client.post('/add-subscriber', json=data)
		response = self.client.post('/add-subscriber', json=data)
		self.assertIn('error', response.get_json())

	def test_list_subscribers_nonempty(self):
		self.client.post('/add-subscriber', json={'name': 'Alice', 'URI': 'http://alice.com'})
		response = self.client.get('/list-subscribers')
		self.assertEqual(response.status_code, 200)
		self.assertIn('Alice', response.get_json())

	def test_delete_subscriber_success(self):
		self.client.post('/add-subscriber', json={'name': 'Bob', 'URI': 'http://bob.com'})
		response = self.client.delete('/delete-subscriber', json={'name': 'Bob'})
		self.assertIn('message', response.get_json())
		self.assertNotIn('Bob', flaskHttpServer.subscribers)

	def test_delete_subscriber_no_name(self):
		response = self.client.delete('/delete-subscriber', json={})
		self.assertEqual(response.status_code, 400)
		self.assertIn('error', response.get_json())

	def test_delete_subscriber_empty_list(self):
		response = self.client.delete('/delete-subscriber', json={'name': 'NonExistent'})
		self.assertEqual(response.status_code, 404)
		self.assertIn('error', response.get_json())

	def test_delete_subscriber_not_found(self):
		self.client.post('/add-subscriber', json={'name': 'Alice', 'URI': 'http://alice.com'})
		response = self.client.delete('/delete-subscriber', json={'name': 'Bob'})
		self.assertIn('error', response.get_json())

	def test_update_and_notify(self):
		self.client.post('/add-subscriber', json={'name': 'Alice', 'URI': 'http://alice.com'})
		response = self.client.post('/update-and-notify', json={'subject-update': 'TestSubject'})
		self.assertIn('message', response.get_json())


if __name__ == '__main__':
	unittest.main()
