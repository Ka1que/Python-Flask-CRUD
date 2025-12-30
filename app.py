from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

#criando uma instancia do app flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #muda a config do sqlalchemy para o caminho da base citado, neste caso o sqlite pois vem incluido no python
db = SQLAlchemy(app) # inicia a base de dados na variavel DB

#definindo uma tabela na base de dados
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(100), unique = True, nullable=False)
    

#definindo uma rota para a pagina inicial
@app.route('/')
def index():
    tasks = Tasks.query.all() #cRud - READ 
    return render_template('index.html', tasks = tasks)


# Crud
@app.route('/create', methods=["POST"])
def create_task():
    description = request.form['description']
    
    #verificar se ja tem uma tarefa igual 
    existin_task = Tasks.query.filter_by(description = description).first()
    if existin_task:
        return 'Erro: já existe essa tarefa', 400
    
    new_task = Tasks(description = description)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

# cruD
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Tasks.query.get(task_id)
    
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect('/')

@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = Tasks.query.get(task_id)
    
    if task:
        task.description = request.form['description']
        db.session.commit()
    return redirect('/')

#permitindo rodar o app diretamente
if __name__== '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True, port=5123) #debug como true irá mostrar os erros e carrega o servidor automáticamente

