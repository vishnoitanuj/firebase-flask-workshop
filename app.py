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

@app.route('/', methods = ['GET', 'POST'])
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

@app.route('/complete/<id>')
def complete(id):
    try:
        todo_ref.document(id).update({'completed': True})
        return redirect('/')
    except:
        return 'There was an issue updating your task'

@app.route('/delete/<id>')
def delete(id):
    try:
        todo_ref.document(id).delete()
        return redirect('/')
    except:
        return 'There was an issue deleting the task'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)