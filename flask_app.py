from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample users (simulating a database)
users = [
    {"id": 1, "name": "Alice", "age": 25, "email": "alice@example.com", "city": "New York"},
    {"id": 2, "name": "Bob", "age": 30, "email": "bob@example.com", "city": "Los Angeles"}
]

# Home page with form, search, and user list
@app.route('/')
def home():
    search_query = request.args.get('search', '').lower()
    filtered_users = [user for user in users if search_query in user["name"].lower()] if search_query else users
    return render_template('index.html', users=filtered_users, search_query=search_query)

# API: Add a new user via form
@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    age = request.form.get('age')
    email = request.form.get('email')
    city = request.form.get('city')

    if not name or not age or not email or not city:
        return "Missing details", 400

    new_user = {
        "id": len(users) + 1,
        "name": name,
        "age": int(age),
        "email": email,
        "city": city
    }
    users.append(new_user)

    return redirect(url_for('home'))

# API: Delete a user
@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    global users
    users = [u for u in users if u["id"] != user_id]
    return redirect(url_for('home'))

# API: Edit user details (Show edit form)
@app.route('/edit/<int:user_id>')
def edit_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return "User not found", 404
    return render_template('edit.html', user=user)

# API: Update user details (Submit edit form)
@app.route('/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    name = request.form.get('name')
    age = request.form.get('age')
    email = request.form.get('email')
    city = request.form.get('city')

    for user in users:
        if user["id"] == user_id:
            user["name"] = name
            user["age"] = int(age)
            user["email"] = email
            user["city"] = city
            break

    return redirect(url_for('home'))

# API: View more details of a user
@app.route('/details/<int:user_id>')
def user_details(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return "User not found", 404
    return render_template('details.html', user=user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
