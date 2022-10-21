import os

from flask_base.config.mysqlconnection import connectToMySQL
from flask_base.models.modelo_base import ModeloBase
from flask import flash

class Recipe(ModeloBase):
    
    modelo = 'recipes'
    campos = ['name','description','instructions','date_made','under_30','usuario_id']

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.usuario_id = data['usuario_id']
        self.usuario_nombre = data['nombre']
        self.usuario_apellido = data['apellido']
        self.image = data['images.name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_all_width_user(cls):
        query = f"SELECT * FROM {cls.modelo} JOIN usuarios ON usuarios.id = {cls.modelo}.usuario_id;"
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query)
        print("AQUI QUIERO VER -->",results)
        all_data = []
        for data in results:
            data['images.name'] = ''
            all_data.append(cls(data))
        return all_data

    @classmethod
    def view_by_id(cls, id):
        query = f"SELECT * FROM {cls.modelo} JOIN usuarios ON usuarios.id = {cls.modelo}.usuario_id JOIN images ON recipe_id = recipes.id WHERE recipes.id = %(id)s;" 
        data = {'id': id }
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query,data)
        print("AQUI QUIERO VER -->",results)
        return cls(results[0])if len(results) > 0 else None

    @classmethod
    def get_by_id_user(cls, id):
        query = f"SELECT * FROM {cls.modelo} JOIN usuarios ON usuarios.id = {cls.modelo}.usuario_id WHERE recipes.id = %(id)s;" 
        data = {'id': id }
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query,data)
        print("AQUI QUIERO VER -->",results)
        all_data = []
        for data in results:
            data['images.name'] = ''
            all_data.append(cls(data))
        return all_data
    
    @classmethod
    def update(cls,data):
        query = """UPDATE recipes SET
                        name = %(name)s,
                        description = %(description)s,
                        instructions = %(instructions)s,
                        date_made = %(date_made)s,
                        under_30 = %(under_30)s,
                        updated_at=NOW() 
                    WHERE id = %(id)s"""
        resultado = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        return resultado
    
    @classmethod
    def delete(cls,id):
        query = f"DELETE FROM {cls.modelo} WHERE id = %(id)s"
        data = {
            'id': id
        }
        resultado = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        print("RESULTADO: ", resultado)
        return resultado    

    @staticmethod
    def validar_largo(data, campo, largo):
        is_valid = True
        if len(data[campo]) <= largo:
            flash(f'El largo del {campo} no puede ser menor o igual {largo}', 'error')
            is_valid = False
        return is_valid

    @classmethod
    def validar(cls, data):

        is_valid = True

        is_valid = cls.validar_largo(data, 'name', 3)
        if not is_valid:
            is_valid = cls.validar_largo(data, 'description', 3)
            is_valid = False
        if not is_valid:
            is_valid = cls.validar_largo(data, 'instructions', 3)
            is_valid = False
        if not is_valid:
            is_valid = cls.validar_largo(data, 'date_made', 9)
            is_valid = False
        return is_valid