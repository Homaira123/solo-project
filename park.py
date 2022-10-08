from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Park:
    db="parks"

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
        self.users_who_favorited =[]
        self.user_ids_who_favorited = []
    @classmethod
    def get_all(cls):
        query ='''SELECT * FROM parks JOIN users AS creators ON parks.user_id = creators.id
            LEFT JOIN favorited_parks ON parks.id = favorited_parks.park_id
            LEFT JOIN users AS users_who_favorited ON favorited_parks.user_id = users_who_favorited.id;'''
        results =connectToMySQL(cls.db).query_db(query)
        parks=[]
        for row in results:
            new_park = True
            user_who_favorited_data = {
                'id' : row['users_who_favorited.id'],
                'first_name':row['users_who_favorited.first_name'],
                'last_name':row['users_who_favorited.last_name'],
                'email':row['users_who_favorited.email'],
                'password':row['users_who_favorited.password'],
                'created_at':row['users_who_favorited.created_at'],
                'updated_at':row['users_who_favorited.updated_at']
            }
            number_of_parks=len(parks)
            if number_of_parks > 0:
                last_park=parks[number_of_parks-1]
                if last_park.id == row['id']:
                    last_park.user_ids_who_favorited.append(row['users_who_favorited.id'])
                    last_park.users_who_favorited.append(User(user_who_favorited_data))
                    new_park = False

            if new_park:
                park = cls(row)
                user_data ={
                    'id' : row['creators.id'],
                    'first_name':row['first_name'],
                    'last_name':row['last_name'],
                    'email':row['email'],
                    'password':row['password'],
                    'created_at':row['creators.created_at'],
                    'updated_at':row['creators.updated_at']
                }
                user = User(user_data)
                park.user = user
                if row['users_who_favorited.id']:
                    park.user_ids_who_favorited.append(row['users_who_favorited.id'])
                    park.users_who_favorited.append(User(user_who_favorited_data))
                parks.append(park)
        return parks

    @classmethod
    def get_one(cls,data):
        query='''SELECT * FROM parks
                JOIN users AS creators ON parks.user_id=creators.id
                LEFT JOIN favorited_parks ON favorited_parks.park_id=parks.id
                LEFT JOIN users AS users_who_favorited ON favorited_parks.user_id=users_who_favorited.id
                WHERE parks.id=%(id)s;'''

        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results)<1:
            return False
        new_park=True
        for row in results:
            if new_park:
                park= cls(row)
                user_data ={
                    'id' : row['creators.id'],
                    'first_name':row['first_name'],
                    'last_name':row['last_name'],
                    'email':row['email'],
                    'password':row['password'],
                    'created_at':row['creators.created_at'],
                    'updated_at':row['creators.updated_at']
                }
                creator= User(user_data)
                park.creator = creator
                new_park= False
            if row['users_who_favorited.id']:
                user_who_favorited_data={
                    'id' : row['users_who_favorited.id'],
                    'first_name': row['users_who_favorited.first_name'],
                    'last_name': row['users_who_favorited.last_name'],
                    'email': row['users_who_favorited.email'],
                    'password': row['users_who_favorited.password'],
                    'created_at': row['users_who_favorited.created_at'],
                    'updated_at': row['users_who_favorited.updated_at']
                }
                user_who_favorited = User(user_who_favorited_data)
                park.users_who_favorited.append(user_who_favorited)
                park.user_ids_who_favorited.append(row['users_who_favorited.id'])
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

    @classmethod
    def favorite(cls,data):
        query = 'INSERT INTO favorited_parks(user_id, park_id) VALUES(%(user_id)s, %(id)s);'
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def unfavorite(cls,data):
        query='DELETE FROM favorited_parks WHERE user_id=%(user_id)s AND park_id=%(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)
    @staticmethod
    def validate_create(park):
        is_valid=True
        if len(park['name']) <4:
            flash("name must be greater then 4 charecters")
            is_valid = False
        if len(park['location'])<8:
            flash("location must be greater then 8 charecters")
            is_valid=False
        if len(park['contact'])<6:
            flash("contact must be greater then 6 characters")
            is_valid=False
        if len(park['description'])<10:
            flash("description must be greater then 10 characters")
            is_valid=False
        return is_valid
