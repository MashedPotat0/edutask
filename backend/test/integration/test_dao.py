import pymongo.errors
import pymongo.mongo_client
import pytest
import unittest.mock
import pymongo
import json
from src.util.dao import DAO
from dotenv import dotenv_values

# copy of validator "todo" which follows ground truth, containing both string and bool, to avoid fetching a real validator which could be changed etc.
validator_for_test = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["description"],
        "properties": {
            "description": {
                "bsonType": "string",
                "description": "the description of a todo must be determined",
                "uniqueItems": True
            }, 
            "done": {
                "bsonType": "bool"
            }
        }
    }
}
url = "mongodb://localhost:27017"
#new validator
def mockedGetValidator(collection):
    return validator_for_test

# Initialize our system, get validator and dao.
@pytest.fixture(scope="session")
def sut():
    client = pymongo.mongo_client.MongoClient(url)
    database = client["edutask"]
    database.drop_collection("integration_test")
    with unittest.mock.patch("src.util.dao.getValidator", new=mockedGetValidator):
        testDao = DAO("integration_test")
    yield testDao
    # clean up
    database.drop_collection("integration_test")

#test case 1
def test_dict_not_compliant_at_all(sut):
    notCompliant = {}
    with pytest.raises(pymongo.errors.WriteError) as e:
            sut.create(notCompliant)
    assert e.type == pymongo.errors.WriteError

#test case 2
def test_required_properties(sut):
    notCompliant = {"done": False}
    with pytest.raises(pymongo.errors.WriteError) as e:
            sut.create(notCompliant)
    assert e.type == pymongo.errors.WriteError

#test case 3
def test_property_complies(sut):
    notCompliant = {"description": 100, "done": "this is not acceptable"}
    with pytest.raises(pymongo.errors.WriteError) as e:
            sut.create(notCompliant)
    assert e.type == pymongo.errors.WriteError

#test case 4
def test_unique(sut):
    originalDesc = {"description": "Unique", "done": True}
    sut.create(originalDesc)
    cloneOfTheOriginalDesc = {"description": "Unique", "done": False}
    with pytest.raises(pymongo.errors.WriteError) as e:
            sut.create(cloneOfTheOriginalDesc)
    assert e.type == pymongo.errors.WriteError

#test case 5
def test_compliant(sut):
    description = "this is a todo"
    todo = {"description": description, "done": True}
    result = sut.create(todo)
    assert result["description"] == description
    assert result["done"] == True
    assert "_id" in result