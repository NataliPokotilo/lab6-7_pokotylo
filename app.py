from flask import Flask, render_template, request, redirect, url_for
import database_connector as db


app = Flask(__name__)


# Ініціалізація таблиці при старті
db.create_db_table()


@app.route("/")
def index():
    """Головна сторінка: показ усіх завдань."""
    tasks = db.get_all_items()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["GET", "POST"])
def add():
    """Create: додати нове завдання."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "new")

        if title:  # простенька валідація
            db.insert_item(title, description, status)

        return redirect(url_for("index"))

    return render_template("edit.html", task=None)


@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit(item_id):
    """Update: редагування існуючого завдання."""
    task = db.get_item_by_id(item_id)
    if task is None:
        return "Task not found", 404

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "new")

        if title:
            db.update_item(item_id, title, description, status)

        return redirect(url_for("index"))

    return render_template("edit.html", task=task)


@app.route("/delete/<int:item_id>", methods=["POST"])
def delete(item_id):
    """Delete: видалення завдання."""
    db.delete_item(item_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
