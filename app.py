from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_script import Manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False, default='9999-12-31 00:00:00.000000')

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_end_date = request.form['enddate']
        #print(task_content, task_end_date)
        y, m, d = task_end_date.split('-')
        end_date = datetime(int(y), int(m), int(d))
        new_task = Todo(content=task_content, end_date=end_date)
        print(new_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return 'Issue in adding the Task ' + str(e)

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Problem While deleting the Task'


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        task.end_date = request.form['enddate']
        y, m, d = task.end_date.split('-')
        task.end_date = datetime(int(y), int(m), int(d))
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error While Updating the Task"
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    # manager.run()
    app.run(debug=True)
