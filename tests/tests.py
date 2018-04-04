import requests
import unittest
from sqlalchemy.engine import create_engine

# IN_CONTAINER_DB_URI = 'postgresql://cs162_user:cs162_password@db/cs162'
DB_URI = 'postgresql://cs162_user:cs162_password@127.0.0.1/cs162?port=5432'


class TestApp(unittest.TestCase):
    def setUp(self):
        engine = create_engine(DB_URI)
        self.conn = engine.connect()

    def test_happy_case(self):
        # 1. Post an HTTP request with a valid expression to the server.
        # Examine the response & confirm that the correct answer is returned
        start_results = self.conn.execute('select count(*) from expression')
        for result in start_results:
            beginning_count = result['count']
        data = {
            'expression': '1+2'
        }
        r = requests.post('http://localhost:5000/add', data=data)
        self.assertEqual(r.status_code, requests.codes.ok)

        # 2. Establish a connection to the database directly & verify that the
        # string you sent has been directly stored in the database.
        results = self.conn.execute('select count(*) from expression')
        for result in results:
            actual_count = result['count']

        expected_count = beginning_count + 1
        self.assertEqual(actual_count, expected_count)

    def test_unhappy_case(self):
        # 3. POST an HTTP request with an invalid expression to the server.
        # Examine the response and confirm that an error is raised.
        start_results = self.conn.execute('select count(*) from expression')
        for result in start_results:
            beginning_count = result['count']
        data = {
            'expression': 'foo * bar'
        }
        r_post = requests.post('http://localhost:5000/add', data=data)
        self.assertEqual(r_post.status_code, requests.codes.server_error)

        # 4. Confirm that no more rows have been added to the database since
        # the last valid expression was sent to the server.
        results = self.conn.execute('select count(*) from expression')
        for result in results:
            actual_count = result['count']

        self.assertEqual(actual_count, beginning_count)


if __name__ == '__main__':
    unittest.main()
