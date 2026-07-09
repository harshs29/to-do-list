# Import required libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_db_connection

# Create Flask application
app = Flask(__name__)

# Enable CORS so React (Frontend) can communicate with Flask (Backend)
CORS(app)

# ============================================================
# API 1 - GET ALL TODOS
# URL: http://localhost:5000/todos
# Method: GET
#
# This API is called by the frontend whenever it needs to
# display all tasks.
# ============================================================

@app.route('/todos', methods=['GET'])
def get_todos():

    # Connect to MySQL
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch all records
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()

    cursor.close()
    conn.close()

    # Return JSON response to frontend
    return jsonify(todos)


# ============================================================
# API 2 - ADD NEW TODO
# URL: http://localhost:5000/todos
# Method: POST
#
# Called when user clicks "Add Task" button.
# Frontend sends JSON data.
# ============================================================

@app.route('/todos', methods=['POST'])
def add_todo():

    # Receive JSON from frontend
    data = request.get_json()

    task = data.get("task")

    # Simple validation
    if not task:
        return jsonify({"message": "Task is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert into MySQL
    cursor.execute(
        "INSERT INTO todos(task) VALUES(%s)",
        (task,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Task added successfully"
    })


# ============================================================
# API 3 - UPDATE TODO STATUS
# URL: http://localhost:5000/todos/<id>
# Method: PUT
#
# Example:
# PUT /todos/3
#
# When frontend clicks Complete button,
# this API changes status from
# Pending -> Completed
# Completed -> Pending
# ============================================================

@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE todos SET status = NOT status WHERE id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Task updated successfully"
    })


# ============================================================
# API 4 - DELETE TODO
# URL: http://localhost:5000/todos/<id>
# Method: DELETE
#
# Example:
# DELETE /todos/2
#
# Called when Delete button is clicked.
# ============================================================

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM todos WHERE id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Task deleted successfully"
    })


# ============================================================
# Start Flask Server
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)