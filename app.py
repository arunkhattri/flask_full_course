#!/usr/bin/env python3
from flask import Flask, render_template, redirect, request
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# My app
app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)


class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Task {self.id}"


# Home page
@app.route("/", methods=["POST", "GET"])
def index():
    # add a task
    if request.method == "POST":
        current_task = request.form["content"]
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
        # see all task
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks=tasks)


# Delete an item
@app.route("/delete/<int:id>")
def delete(id: int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR:{e}"


# Update an item
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id: int):
    update_task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        update_task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR:{e}"
    else:
        return render_template("update.html", task=update_task)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
