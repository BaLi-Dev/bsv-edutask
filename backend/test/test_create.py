import pytest
from unittest.mock import MagicMock
from src.util.dao import DAO
import pymongo
import os, json

@pytest.fixture
def dao():
    """
    Fixture to create a DAO instance with the test database.
    """
    dao = DAO("todo")
    yield dao
    # Teardown
    dao.collection.delete_many({}) 

@pytest.mark.integration
def test_create_valid_data(dao):
    """
    Test creating a document with valid data.
    """
    data = {"description":"hej", "done":False}
    result = dao.create(data)
    assert "_id" in result
    assert result["description"] == "hej"
    assert result["done"] == False


@pytest.mark.integration
def test_create_missing_data(dao):
    """
    Test creating a document with valid data.
    """
    data = {"done":True}
    
    with pytest.raises(pymongo.errors.WriteError):
        dao.create(data)


@pytest.mark.integration
def test_create_bson_type(dao):
    """
    Test creating a document with valid data.
    """
    data = {"description":89271349, "done":False}
    
    with pytest.raises(pymongo.errors.WriteError):
        dao.create(data)

@pytest.mark.integration
def test_create_unique(dao):
    """
    Test creating a document with valid data.
    """
    data = {"description":"hej", "done":False}

    dao.create(data)
    with pytest.raises(pymongo.errors.WriteError):
        dao.create(data)
