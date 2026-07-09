import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  // Stores all todos from backend
  const [todos, setTodos] = useState([]);

  // Stores input task
  const [task, setTask] = useState("");

  // ==========================
  // GET API
  // Fetch all todos
  // ==========================
  const getTodos = async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/todos`);
      setTodos(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  // Load todos when page opens
  useEffect(() => {
    getTodos();
  }, []);

  // ==========================
  // POST API
  // Add new task
  // ==========================
  const addTodo = async () => {
    if (task.trim() === "") return;

    try {
      await axios.post(`${import.meta.env.VITE_API_URL}/todos`, {
        task: task,
      });

      setTask("");
      getTodos();
    } catch (error) {
      console.log(error);
    }
  };

  // ==========================
  // PUT API
  // Update task status
  // ==========================
  const updateTodo = async (id) => {
    try {
      await axios.put(`${import.meta.env.VITE_API_URL}/todos/${id}`);
      getTodos();
    } catch (error) {
      console.log(error);
    }
  };

  // ==========================
  // DELETE API
  // Delete task
  // ==========================
  const deleteTodo = async (id) => {
    try {
      await axios.delete(`${import.meta.env.VITE_API_URL}/todos/${id}`);
      getTodos();
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="container">

      <h1>📝 My Todo App</h1>

      <p className="count">
        Total Tasks : <strong>{todos.length}</strong>
      </p>

      <div className="input-box">
        <input
          type="text"
          placeholder="Enter your task..."
          value={task}
          onChange={(e) => setTask(e.target.value)}
        />

        <button className="add-btn" onClick={addTodo}>
          Add Task
        </button>
      </div>

      {
        todos.length === 0 ? (

          <div className="empty">
            No Tasks Available 😊
          </div>

        ) : (

          todos.map((todo) => (

            <div className="todo-card" key={todo.id}>

              <h3>{todo.task}</h3>

              <p>
                Status :
                <span className={todo.status ? "completed" : "pending"}>
                  {todo.status ? " Completed ✅" : " Pending ⏳"}
                </span>
              </p>

              <div className="button-group">

                <button
                  className="complete-btn"
                  onClick={() => updateTodo(todo.id)}
                >
                  {todo.status ? "Undo" : "Complete"}
                </button>

                <button
                  className="delete-btn"
                  onClick={() => deleteTodo(todo.id)}
                >
                  Delete
                </button>

              </div>

            </div>

          ))

        )
      }

    </div>
  );
}

export default App;