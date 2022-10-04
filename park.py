from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Park:
    db="log_parks"

    def __init__(self,data):
        self.id=data['id']
        self.name=data['name']
        self.location=data['location']
        self.contact=data['contact']
        self.user_id = data['user_id']
        self.description=data['description']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user = None
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM parks JOIN users ON parks.user_id = users.id;"
        results =connectToMySQL(cls.db).query_db(query)
        parks=[]
        for row in results:
            park = cls(row)
            user_data ={
                'id' : row['users.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['users.created_at'],
                'updated_at':row['users.updated_at']
            }
            user = User(user_data)
            park.user = user
            parks.append(park)
        return parks

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM parks JOIN users ON parks.user_id = users.id WHERE parks.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results)<1:
            return False
        row= results[0]
        park= cls(row)
        user_data ={
            'id' : row['users.id'],
            'first_name':row['first_name'],
            'last_name':row['last_name'],
            'email':row['email'],
            'password':row['password'],
            'created_at':row['users.created_at'],
            'updated_at':row['users.updated_at']
        }
        user = User(user_data)
        park.user = user
        return park
    @classmethod
    def create(cls,data):
        query = "INSERT INTO parks(name,location,contact,description,user_id) VALUES(%(name)s,%(location)s,%(contact)s,%(description)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)


    @classmethod
    def update(cls,data):
        query = "UPDATE parks SET name=%(name)s, location=%(location)s, contact=%(contact)s, description=%(description)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    @classmethod
    def delete(cls,data):
        query="DELETE FROM parks WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    @staticmethod
    def validate_create(park):
        is_valid=True
        if len(park['name']) <4:
            flash("park must be greater then 4")
            is_valid = False
        if len(park['location'])<8:
            flash("location must be greater then 8")
            is_valid=False
        return is_valid
