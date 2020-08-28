import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor
assistant = "Bearer {}".format(os.environ['ASSISTANT'])
director = "Bearer {}".format(os.environ['DIRECTOR'])
producer = "Bearer {}".format(os.environ['PRODUCER'])
print(assistant)


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', '62328243', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.add_new_actor = {
            "actor": "Stephen Lang",
            "gender": "Male",
            "movie": "Don't Breathe"
        }

        self.failed_add_actor = {
            'actor': "susan Levy",
            'movie': "don't breathe"
        }
        self.add_new_movie = {
            'movie': "Fake movie",
            'catogry': "Fake catogary"}

        self.failed_add_movie = {
            'movie': "The Ring 2"}

        self.updated_actor = {"actor": "Dylan Minnette"}
        self.updated_movie = {"catogry": "Comedy"}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_01_get_actors(self):
        """Testing the success of retriving actors and  paginating """
        res = self.client().get('/actors',
                                headers={"Authorization": (assistant)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_02_404_beyoned_valied_page_of_actors(self):
        """Testing the faliur 404 of retriving actors and paginating """
        res = self.client().get(
            '/actors?page=30',
            headers={
                "Authorization": (assistant)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_03_get_movies(self):
        """Testing the success of retriving movies and  paginating """
        res = self.client().get('/movies',
                                headers={"Authorization": (assistant)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_04_beyoned_valied_page_of_movies(self):
        """Testing the faliur 404 of retriving movies and paginating """
        res = self.client().get(
            '/movies?page=20',
            headers={
                "Authorization": (assistant)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_05_insert_new_actors(self):
        """Testing the success of posting new actor"""
        res = self.client().post(
            '/actors',
            json=self.add_new_actor,
            headers={
                "Authorization": (director)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # filed becuse gender is null in new actor
    def test_06_422_failed_insert_new_actors(self):
        """Testing the faliur 422 of posting new actor """
        res = self.client().post(
            '/actors',
            json=self.failed_add_actor,
            headers={
                "Authorization": (director)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_07_insert_new_movies(self):
        """Testing the success of posting new movie"""
        res = self.client().post('/movies', json=self.add_new_movie,
                                 headers={"Authorization": (producer)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # filed becuse catogry is null in new movie
    def test_08_422_failed_insert_new_movies(self):
        """Testing the faliur 422 of posting new movie """
        res = self.client().post(
            '/movies',
            json=self.failed_add_movie,
            headers={
                "Authorization": (producer)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_09_delete_new_actor(self):
        """Testing the success of delete exictence actor"""
        res = self.client().delete(
            '/actors/4',
            headers={
                "Authorization": (director)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # failed becuse id not exictence
    def test_10_404_failed_delete_new_actor(self):
        """Testing the faliur 404 of delete none exictence actor"""
        res = self.client().delete(
            '/actors/100',
            headers={
                "Authorization": (director)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_11_delete_new_movie(self):
        """Testing the success of delete exictence movie"""
        res = self.client().delete(
            '/movies/5',
            headers={
                "Authorization": (producer)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # failed becuse id not exictence
    def test_12_404_failed_delete_new_movie(self):
        """Testing the faliur 404 of delete none exictence movie"""
        res = self.client().delete(
            '/movies/11',
            headers={
                "Authorization": (producer)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_13_update_actor(self):
        """Testing the success of update exictence actor"""
        res = self.client().patch(
            '/actors/2',
            json=self.updated_actor,
            headers={
                "Authorization": (director)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # failed becuse id not exictence
    def test_14_404_failed_updated_actor(self):
        """Testing the faliur 404 of update none exictence actor"""
        res = self.client().patch(
            '/actors/20',
            json=self.updated_actor,
            headers={
                "Authorization": (director)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_15_update_movie(self):
        """Testing the success of update exictence movie"""
        res = self.client().patch(
            '/movies/1',
            json=self.updated_movie,
            headers={
                "Authorization": (director)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # failed becuse id not exictence
    def test_16_404_failed_updated_movie(self):
        """Testing the faliur 404 of update none exictence movie"""
        res = self.client().patch(
            '/movies/20',
            json=self.updated_movie,
            headers={
                "Authorization": (director)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
