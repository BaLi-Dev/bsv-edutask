import pytest
from unittest.mock import MagicMock
from src.util.dao import DAO
import pymongo
import os, json

@pytest.fixture
def testDatabase():
    """
    Fixture to create a test database and collection.
    """
    client = pymongo.MongoClient("mongodb://root:root@mongodb:27017/")
    db = client.edutask
    collection = db.test_collection
    collection.create_index("name", unique=True)
    yield collection.name
    # Teardown
    collection.drop()    


@pytest.fixture
def dao(testDatabase):
    """
    Fixture to create a DAO instance with the test database.
    """
    return DAO(testDatabase)

@pytest.mark.integration
def test_create_valid_data(dao):
    """
    Test creating a document with valid data.
    """
    data = {"name": "test", "active": True}
    result = dao.create(data)
    assert "_id" in result
    assert result["name"] == "test"
    assert result["active"] == True


@pytest.mark.integration
def test_create_missing_name(dao):
    """
    Test creating a document with valid data.
    """
    data = {"active": True}
    
    with pytest.raises(pymongo.errors.WriteError):
        dao.create(data)

@pytest.mark.integration
def test_create_missing_value(dao):
    """
    Test creating a document with valid data.
    """
    data = {"name": "test"}
    
    with pytest.raises(pymongo.errors.WriteError):
        dao.create(data)

@pytest.mark.integration
def test_create_beson_type(dao):
    """
    Test creating a document with valid data.
    """
    data = {"name": 213123, "active": True}
    
    with pytest.raises(pymongo.errors.WriteError):
        dao.create(data)

@pytest.mark.integration
def test_create_unique(dao):
    """
    Test creating a document with valid data.
    """
    data = {"name": "213123", "active": True}
    dao.create(data)
    
    with pytest.raises(pymongo.errors.WriteError):
        dao.create(data)

