from flask import Flask, request, jsonify
from models.user import User
from models.meal import Meal
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

def serialize_meal(meal):
  return {
    "id": meal.id,
    "name": meal.name,
    "description": meal.description,
    "hour": meal.hour,
    "is_it_on_diet": meal.is_it_on_diet
  }

def check_permission(meal):
  if current_user.role == "admin":
    return True
  elif current_user.role == "user" and meal.user_id == current_user.id:
    return True
  return False

@app.route("/login", methods=["POST"])
def login():
  data = request.json
  username = data.get("username")
  password = data.get("password")
  if username and password:
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
      login_user(user)
      print(current_user.is_authenticated)
      return jsonify({"message": "Autenticação realizada com sucesso!"})
  return jsonify({"message": "Credenciais inválidas"}), 400

@app.route("/logout", methods=["GET"])
@login_required
def logout():
  logout_user()
  return jsonify({"message": "Logout realizado com sucesso!"})

@app.route("/user", methods=["POST"])
def create_user():
  data = request.json
  username = data.get("username")
  password = data.get("password")
  if username and password:
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Usuario cadastrado com sucesso"})
  return jsonify({"message": "Dados invalidos"}), 400

@app.route("/meal", methods=["POST"])
@login_required
def create_meal():
  data = request.json
  name = data.get("name")
  description = data.get("description")
  hour = datetime.now()
  is_it_on_diet = data.get("is_it_on_diet")
  user_id = current_user.id

  if name and is_it_on_diet == False or is_it_on_diet == True:
    meal = Meal(
      name=name, 
      description=description,
      hour=hour, 
      is_it_on_diet=is_it_on_diet, 
      user_id=user_id
    )
    db.session.add(meal)
    db.session.commit()
    return jsonify({"message": "Refeição cadastrada com sucesso"})
  return jsonify({"message": "Dados inválidos"}), 400

@app.route("/meal/<int:id>", methods=["PUT"])
@login_required
def update_meal(id):
  data = request.json
  meal = Meal.query.get(id)
    
  if not meal:
    return jsonify({"message": "Refeição não encontrada"}), 404
  if not check_permission(meal):  
    return jsonify({"message": "Você não tem nenhuma refeição com esse ID"}), 403
    
  name = data.get("name", meal.name)
  description = data.get("description", meal.description)
  hour = datetime.now()
  is_it_on_diet = data.get("is_it_on_diet", meal.is_it_on_diet)
    
  meal.name = name
  meal.description = description
  meal.hour = hour
  meal.is_it_on_diet = is_it_on_diet
    
  db.session.commit()
    
  return jsonify({"message": "Refeição atualizada com sucesso"}), 200
  
@app.route("/meal/<int:id>", methods=["DELETE"])
@login_required
def delete_meal(id):
  meal = Meal.query.get(id)
  if current_user.role == "admin":
    db.session.delete(meal)
    db.session.commit()
    return jsonify({"message": "Refeição deletada com sucesso"})
  if current_user.role == "user":
    if meal == None:
      return jsonify({"message": "Não foi possível deletar essa refeição"}), 400
    if meal.user_id != current_user.id:
      return jsonify({"message": "Não é possível deletar a refeição informada"}), 403
    if meal:
      db.session.delete(meal)
      db.session.commit()
      return jsonify({"message": "Refeição deletada com sucesso"})

@app.route("/meals/<int:user_id>", methods=["GET"])
@login_required
def user_meals(user_id):
  if current_user.role == "admin" or current_user.id == user_id:
    user_meals = Meal.query.filter_by(user_id=user_id).all()
    meals_list = []
    if user_meals:
      for meal in user_meals:
        meals_list.append(serialize_meal(meal))
      return jsonify(meals_list)
    if len(meals_list) == 0:
      return jsonify({"message": "Não há refeições."}), 404
    return jsonify({"message": "Não foi possível encontrar as refeições do usuário"}), 404
  return jsonify({"message": "Você não tem permissão para realizar essa ação."}), 403


@app.route("/meal/<int:id>", methods=["GET"])
@login_required
def see_meal(id):
  meal = Meal.query.get(id)
  if meal:
    if check_permission(meal):
      return jsonify(serialize_meal(meal))
    else:
      return jsonify({"message": "Você não tem nenhuma refeição com esse ID"})
  return jsonify({"message": "Não foi possível encontrar a refeição"})

if __name__ == "__main__":
  app.run(debug=True)