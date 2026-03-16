from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Simple in-memory storage for todos.
# Each todo is a dict: {'id': int, 'text': str, 'completed': bool}
todos = []
next_id = 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    global next_id
    data = request.json
    if not data or 'text' not in data or not data['text'].strip():
        return jsonify({'error': 'Task text is required'}), 400
    
    new_todo = {
        'id': next_id,
        'text': data['text'].strip(),
        'completed': False
    }
    todos.append(new_todo)
    next_id += 1
    return jsonify(new_todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.json
    for todo in todos:
        if todo['id'] == todo_id:
            if 'completed' in data:
                todo['completed'] = data['completed']
            if 'text' in data:
                todo['text'] = data['text'].strip()
            return jsonify(todo)
    return jsonify({'error': 'Todo not found'}), 404

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    initial_length = len(todos)
    todos = [todo for todo in todos if todo['id'] != todo_id]
    if len(todos) < initial_length:
        return '', 204
    return jsonify({'error': 'Todo not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
