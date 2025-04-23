from flask import Flask, render_template, request, redirect, url_for
import re  
import os  
import pickle

app = Flask(__name__)


TODO_LIST_FILE = "todo_list.pkl"  
todo_list = []


if os.path.exists(TODO_LIST_FILE):
    try:
        with open(TODO_LIST_FILE, "rb") as f:
            todo_list = pickle.load(f)
    except Exception as e:
        print(f"Error loading todo list from file: {e}")
        todo_list = []  
else:
    todo_list = [] 


EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Displays the ToDo list and the form to add new items.
    """
    return render_template('index.html', todos=todo_list)


@app.route('/submit', methods=['POST'])
def submit():
    """
    Handles the submission of a new ToDo item.
    Validates the input and adds the item to the list.
    """
    task = request.form.get('task')
    email = request.form.get('email')
    priority = request.form.get('priority')

    
    if not task or not email or not priority:
        return render_template('index.html', todos=todo_list, error="All fields are required.")

    if not re.match(EMAIL_REGEX, email):
        return render_template('index.html', todos=todo_list, error="Invalid email address.")

    if priority not in ['Low', 'Medium', 'High']:
        return render_template('index.html', todos=todo_list, error="Invalid priority level.")

    
    todo_list.append({'task': task, 'email': email, 'priority': priority})

    return redirect(url_for('index'))


@app.route('/clear')
def clear():
    """
    Clears the ToDo list.
    """
    global todo_list  
    todo_list = []
    return redirect(url_for('index'))

@app.route('/save')
def save():
    """
    Saves the ToDo list to a file (Extra Credit I).
    """
    try:
        with open(TODO_LIST_FILE, "wb") as f:
            pickle.dump(todo_list, f)
        return render_template('index.html', todos=todo_list, message="List saved successfully!")
    except Exception as e:
        return render_template('index.html', todos=todo_list, error=f"Error saving list: {e}")

@app.route('/delete/<int:index>')
def delete(index):
    """
    Deletes a ToDo item from the list (Extra Credit II).
    """
    try:
        del todo_list[index]
    except IndexError:
        
        print(f"Invalid index for deletion: {index}")

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)  
