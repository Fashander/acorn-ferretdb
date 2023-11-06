import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

db_uri = os.environ["DB_URI"]
db_name = os.environ["DB_NAME"]

print("DB_URI:", db_uri)
print("DB_NAME:", db_name)

client = MongoClient(db_uri)
db = client[db_name]
todos_collection = db['todos']

def redirect_url():
    return request.args.get('next') or \
            request.referrer or \
            url_for('home')

@app.route("/")
def home():
    todo_list = list(todos_collection.find({}))
    return render_template("template.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = {"title": title, "done": False}
    todos_collection.insert_one(new_todo)
    return redirect(redirect_url())

@app.route("/update/<todo_id>")
def update(todo_id):
    todo = todos_collection.find_one({"_id": ObjectId(todo_id)})
    todos_collection.update_one({"_id": ObjectId(todo_id)}, {"$set": {"done": not todo["done"]}})
    return redirect(redirect_url())

@app.route("/delete/<todo_id>")
def delete(todo_id):
    todos_collection.delete_one({"_id": ObjectId(todo_id)})
    return redirect(redirect_url())

if __name__ == "__main__":
    app.run(debug=True)
