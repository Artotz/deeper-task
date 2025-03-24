from flask import Blueprint, request, jsonify
from database import users_collection
from models import UserSchema

routes = Blueprint("routes", __name__)

@routes.route("/users", methods=["GET"])
def get_users():
    users = list(users_collection.find({}, {"_id": 0}))
    return jsonify(users), 200


@routes.route("/users/<string:username>", methods=["GET"])
def get_user(username):
    user = users_collection.find_one({"username": username}, {"_id": 0})

    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "Usuário não encontrado"}), 404


@routes.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.json
        user_data = UserSchema(**data)

        # Inserir no MongoDB
        users_collection.insert_one(user_data.model_dump())

        return jsonify({"message": "Usuário criado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@routes.route("/users/<string:username>", methods=["PUT"])
def edit_user(username):
    data = request.json
    user = users_collection.find_one({"username": username})

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    updated_data = {k: v for k, v in data.items() if v is not None}
    users_collection.update_one({"username": username}, {"$set": updated_data})

    return jsonify({"message": "Usuário atualizado!"}), 200


@routes.route("/users/<string:username>", methods=["DELETE"])
def delete_user(username):
    result = users_collection.delete_one({"username": username})
    if result.deleted_count:
        return jsonify({"message": "Usuário deletado!"}), 200
    return jsonify({"error": "Usuário não encontrado"}), 404
