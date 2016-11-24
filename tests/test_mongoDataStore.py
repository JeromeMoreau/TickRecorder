from unittest import TestCase
from data_store import MongoDataStore

class TestMongoDataStore(TestCase):

    def setUp(self):
        """
        run when starting the tests
        Initialize the data_store and a collection.
        """
        self.mongo = MongoDataStore()
        self.library = self.mongo.database['testCollection']


    def test__connect_to_mongodb(self):
        self.assertEqual(self.library.name, 'testCollection', msg="Failed to create a document collection")

    def test_recordTick(self):
        result = self.library.insert_one({'testDocument': 1})
        self.assertIsNotNone(result.inserted_id, msg="Failed to insert in the database")

        data = {}
        result2 = self.library.insert_one(data)





    def tearDown(self):
        """
        run after the tests
        remove the document collection in the database
        """
        self.mongo.database.drop_collection('testCollection')
        super().tearDown()
