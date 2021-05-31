import os
from flask import Flask, render_template, url_for, request, redirect
from firebase_admin import credentials, firestore, initialize_app
import base64
import json

FIREBASE_SERVICE_KEY = json.loads(base64.b64decode(os.environ['FIREBASE_SERVICE_KEY']))

app = Flask(__name__)
cred = credentials.Certificate(FIREBASE_SERVICE_KEY)
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')

def index():
    if request.method == 'POST':
        try:
            todo_ref.add({'task': request.form['task'], 'completed': False})
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        try:
            todos = []
            for doc in todo_ref.stream():
                todo = doc.to_dict()
                todo['id'] = doc.id
                todos.append(todo)
            print(todos)
            return render_template('index.html', todos=todos)
        except:
            return 'There was an issue loading your todos'