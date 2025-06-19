from flask import Flask, jsonify, request, send_from_directory
from db_connection import  DB_Connection
from datetime import  datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db = DB_Connection()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = db.get_all()
    task_list = [
        {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "is_done": row[3],
            "created_on": row[4].strftime("%Y-%m-%d %H:%M")
        } for row in tasks
    ]
    return jsonify(task_list), 200

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = db.get_by_id(task_id)
    if task:
        return  jsonify({
            "id": task[0],
            "title": task[1],
            "description": task[2],
            "is_done": task[3],
            "created_on": task[4].strftime("%Y-%m-%d %H:%M")
        }), 200
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        db.delete_by_id(task_id)
        return  jsonify({"message":"Task deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def mark_as_done(task_id):
    task = db.get_by_id(task_id)
    if not task:
        return  jsonify({"error": "Task not found"}), 404

    try:
        db.update_task(task_id, None, None, True)
        return  jsonify({"message": "successfully updated task"}), 200
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    if not title or not description:
        return jsonify({"error": "Title and description are required"}), 400
    try:
        db.insert(title, description, False, datetime.now())
        return jsonify({"message": "Task created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)