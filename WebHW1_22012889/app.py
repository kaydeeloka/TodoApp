from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#database 
# username에는 생성한 사용자 계정명 입력
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:password@localhost/flask_todo_db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# SQLAlchemy 객체 생성
db = SQLAlchemy(app) 

#create class for table
class Todo(db.Model): 
    id = db.Column(db.Integer, primary_key=True) #auto primary key id
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200)) 
    completed = db.Column(db.Boolean, default=False) 
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp()) 
    
    def __repr__(self): 
        return f'<Todo {self.title}>'

@app.route('/todo', methods=['POST']) 
def add_todo(): 
    data = request.json 
    if not data or 'title' not in data: 
        return jsonify({'error': 'Title is required'}), 400 
    
    new_todo = Todo( 
        title=data['title'], 
        description=data.get('description', '') ) 
    db.session.add(new_todo) 
    db.session.commit() 

    return jsonify({ 
            'id': new_todo.id, 
            'title': new_todo.title, 
            'description': new_todo.description, 
            'completed': new_todo.completed, 
            'created_at': new_todo.created_at 
}), 201 

#get all info in db
@app.route('/todos', methods=['GET']) 
def get_todos():
    todos = Todo.query.all() 
    return jsonify([
        {
            'id': todo.id, 
            'title': todo.title,
            'description': todo.description,
            'completed': todo.completed, 
            'created_at': todo.created_at
        } for todo in todos
 ])

#get info in db by id
@app.route('/todo/<int:id>', methods=['GET'])
def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return jsonify({
    'id': todo.id,
    'title': todo.title,
    'description': todo.description, 
    'completed': todo.completed, 
    'created_at': todo.created_at
    })

#update info in db    
@app.route('/todo/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    data = request.json
    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    todo.completed = data.get('completed', todo.completed)
    
    db.session.commit()
    return jsonify({
    'id': todo.id,
    'title': todo.title,
    'description': todo.description,
    'completed': todo.completed,
    'created_at': todo.created_at
    })

@app.route('/todo/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id) 
    db.session.delete(todo) 
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'}), 200

@app.route('/todos/completed', methods=['GET']) 
def get_completed_todos():
    completed_todos = Todo.query.filter_by(completed=True).all() 
    return jsonify([
    {
    'id': todo.id, 
    'title': todo.title,
    'description': todo.description,
    'created_at': todo.created_at
    } for todo in completed_todos
    ])

@app.route('/todos/sorted', methods=['GET']) 
def get_sorted_todos():
    sorted_todos = Todo.query.order_by(Todo.created_at.desc()).all() 
    return jsonify([
    {
    'id': todo.id, 
    'title': todo.title,
    'description': todo.description,
    'completed': todo.completed,
    'created_at': todo.created_at
    } for todo in sorted_todos
    ])

@app.route('/todos/paginated', methods=['GET']) 
def get_paginated_todos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    paginated_todos = Todo.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({ 
    'todos': [
    {
    'id': todo.id, 
    'title': todo.title,
    'description': todo.description, 
    'completed': todo.completed, 
    'created_at': todo.created_at
    } for todo in paginated_todos.items
    ],
    'total': paginated_todos.total,
    'pages': paginated_todos.pages, 
    'current_page': page
    })
 
@app.route('/todos/search', methods=['GET'])
def search_todos():
    keyword = request.args.get('keyword', '')
    todos = Todo.query.filter(
        Todo.title.like(f'%{keyword}%'),
        Todo.completed == False
    ).all()
    
    return jsonify([
    {
        'id': todo.id, 
        'title': todo.title,
        'description': todo.description,
        'completed': todo.completed, 
        'created_at': todo.created_at
        } for todo in todos
    ])
 
with app.app_context():
    db.create_all()

#connect with web front end
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__': 
    app.run(debug=True) 