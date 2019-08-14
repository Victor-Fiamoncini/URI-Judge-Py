# Imports:
from flask import Flask, request, jsonify, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from urllib.request import Request, urlopen
from bar import Bar
from pie import Pie
import datetime, os, re, json, random, string

# App:
app = Flask(__name__)
app.secret_key = 'mytopmegafuckingsecret'
basedir = os.path.abspath(os.path.dirname(__file__))

# Database Configs:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'trabalhoUri.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Turma Class/Model:
class Turma(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(255))

  def __init__(self, name):
    self.name = name

# Turma Schema:
class TurmaSchema(ma.Schema):
  class Meta:
    fields = (
      'id', 
      'name'
    )

# Instituicao Class/Model:
class Instituicao(db.Model):
  id = db.Column(
    db.Integer, 
    primary_key=True,
    autoincrement=True,
  )
  name = db.Column(db.String(255))
  instituicao_id = db.relationship(
    'Aluno',
    backref='instituicao'
  ) 

  def __init__(self, name):
    self.name = name

# Instituicao Schema:
class InstituicaoSchema(ma.Schema):
  class Meta:
    fields = (
      'id', 
      'name'
    )

# Aluno Class/Model:
class Aluno(db.Model):
  id = db.Column(
    db.Integer, 
    primary_key=True, 
    autoincrement=True
  )
  name = db.Column(db.String(255))
  since = db.Column(db.Date)
  solved = db.Column(db.Float)
  tried = db.Column(db.Float)
  submissions = db.Column(db.Float)
  points = db.Column(db.Float)
  place = db.Column(db.Float)
  instituicao_id = db.Column(
    db.Integer, 
    db.ForeignKey('instituicao.id')
  )
  
  def __init__(self, name, since, solved, tried, submissions, points, place, instituicao_id):
    self.name = name
    self.since = since
    self.solved = solved
    self.tried = tried
    self.submissions = submissions
    self.points = points
    self.place = place
    self.instituicao_id = instituicao_id

# Aluno Schema:
class AlunoSchema(ma.Schema):
  class Meta:
    fields = (
      'id', 
      'name', 
      'since', 
      'solved', 
      'tried', 
      'submissions', 
      'points', 
      'place', 
      'instituicao_id'
    )

# AlunoTurma Class/Model:
class AlunoTurma(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  aluno_id = db.Column(
    db.Integer, 
    db.ForeignKey('aluno.id'), nullable=False
  )
  turma_id = db.Column(
    db.Integer, 
    db.ForeignKey('turma.id'), nullable=False
  )

  def __init__(self, aluno_id, turma_id):
    self.aluno_id = aluno_id
    self.turma_id = turma_id

# AlunoTurma Schema:
class AlunoTurmaSchema(ma.Schema):
  class Meta:
    fields = (
      'id', 
      'aluno_id', 
      'turma_id'
    )

# Init schemas:
# Turma:
turma_schema = TurmaSchema(strict=True)
turmas_schema = TurmaSchema(many=True, strict=True)
# Instituicao:
instituicao_schema = InstituicaoSchema(strict=True)
instituicoes_schema = InstituicaoSchema(many=True, strict=True)
# Aluno:
aluno_schema = AlunoSchema(strict=True)
alunos_schema = AlunoSchema(many=True, strict=True)
# AlunoTurma:
aluno_turma_schema = AlunoTurmaSchema(strict=True)
aluno_turmas_schema = AlunoTurmaSchema(many=True, strict=True)

# Routes:
# Index page:
@app.route('/', methods=['GET'])
def index():  
  turmas = Turma.query.all()
  turmas = turmas_schema.dump(turmas)
  instituicoes = Instituicao.query.all()
  instituicoes = instituicoes_schema.dump(instituicoes)
  alunos = Aluno.query.all()
  totais = []
  tick_label = []
  for instituicao in instituicoes:
    for inst in instituicao:
      id = inst['id']
      tick_label.append(inst['name'])
      points = db.engine.execute(f'SELECT points FROM aluno WHERE instituicao_id = {id}')
      points =  [
        {column: value for column, value in rowproxy.items()} for rowproxy in points
      ]
      total = 0
      for point in points:
        total += point['points']
      total = total / len(points)
      totais.append(total)
  color = ['red', 'green']
  width = 0.8
  graph = Bar(
    tick_label, 
    totais, 
    width, 
    color, 
    'nome', 
    'média', 
    '', 
    'bar'
  )
  return render_template(
    'pages/index.html', 
    turmas=turmas.data,
    instituicoes=instituicoes.data,
    grafico=graph.plotGraph()
  )

# Cadastro turma:
@app.route('/cadastro-turma', methods=['POST'])
def cadastroTurma(): 
  name = request.form['name-turma']
  new_turma = Turma(name)
  db.session.add(new_turma)
  db.session.commit()
  flash('Turma cadastrada com sucesso', 'success')
  return redirect('/')

# Cadastro Aluno:
@app.route('/cadastro-aluno', methods=['POST'])
def cadastroAluno(): 
  id = request.form['id-aluno']
  turma_id = request.form['turma-aluno']
  # Request para URI Judge:
  try:
    req = Request(f'https://www.urionlinejudge.com.br/judge/en/profile/{id}', headers={
      'User-Agent': 'Mozilla/5.0'
    })
    res = urlopen(req).read()
  except Exception:
    flash('Erro ao requerir os dados do aluno', 'secondary')
    return redirect('/')
  else:
    res = ''.join(map(chr, res))
    res = res.split(' ')
    # Name:
    index = res.index('class="pb-username">\n')
    index = res[index + 30]
    name = index.split('>')[1]
    name = name.split('<')[0]  
    # Place:
    index = res.index('<span>Place:</span>\n')
    place = res[index + 16]
    if place == 'Unknown': 
      place = 0
    else:
      place = re.sub('[^A-Za-z0-9]+', '', place)
      place = re.sub('\D', '', place)
    # University:
    index = res.index('<span>University:</span>\n')
    index = res[index + 19]
    university = index.split('>')[1]
    university = university.split('<')[0]
    # Since:
    index = res.index('<span>Since:</span>\n')
    since = res[index + 16]
    since = datetime.datetime.strptime(since, '%m/%d/%y')
    # Points:
    index = res.index('<span>Points:</span>\n')
    points = res[index + 16]
    # Solved:
    index = res.index('<span>Solved:</span>\n')
    solved = res[index + 16]
    # Tried:
    index = res.index('<span>Tried:</span>\n')
    tried = res[index + 16]
    # Submissions:
    index = res.index('<span>Submissions:</span>\n')
    submissions = res[index + 16]
    # Cadastro instituicao:
    instituicoes = Instituicao.query.all()
    instituicoes = instituicoes_schema.dump(instituicoes)
    if re.search(f'"name": "{university}"', json.dumps(instituicoes), re.M):    
      university_id = db.engine.execute(f'SELECT id FROM instituicao WHERE name = "{university}"')
      university_id = [
        {column: value for column, value in rowproxy.items()} for rowproxy in university_id
      ]
      university_id = university_id[0]['id']
      new_aluno = Aluno(
        name,
        since,
        solved,
        tried,
        submissions,
        points,
        place,
        university_id
      )
      db.session.add(new_aluno)
      db.session.commit()
      db.session.refresh(new_aluno)
      # Insert aluno_turma:
      new_aluno_turma = AlunoTurma(new_aluno.id, turma_id)
      db.session.add(new_aluno_turma)
      db.session.commit()
      flash('Aluno cadastrado com sucesso', 'success')
      return redirect('/')
    else:
      new_instituicao = Instituicao(university)
      db.session.add(new_instituicao)
      db.session.commit()
      db.session.refresh(new_instituicao)
      new_aluno = Aluno(
        name,
        since,
        solved,
        tried,
        submissions,
        points,
        place,
        new_instituicao.id
      )
      db.session.add(new_aluno)
      db.session.commit()
      db.session.refresh(new_aluno)
      # Insert aluno_turma:
      new_aluno_turma = AlunoTurma(new_aluno.id, turma_id)
      db.session.add(new_aluno_turma)
      db.session.commit()
      flash('Aluno cadastrado com sucesso', 'success')
      return redirect('/')
    flash('Erro ao cadastrar', 'secondary')
    return redirect('/')

# Listagem alunos por turma:
@app.route('/turmas', methods=['GET'])
def listarAlunosPorTurma():  
  id = request.args.get('id')
  name = request.args.get('name')
  alunos = db.engine.execute(f'''
    SELECT * FROM aluno LEFT JOIN aluno_turma on aluno_turma.aluno_id = aluno.id 
    WHERE aluno_turma.turma_id = {id}
  ''')
  alunos =  [
    {column: value for column, value in rowproxy.items()} for rowproxy in alunos
  ]
  tick_label = []
  points = []
  explode = []
  for aluno in alunos:
    if aluno['points'] > 0:
      points.append(aluno['points'])
      tick_label.append(aluno['name'])
      explode.append(0)
  get_colors = lambda n: list(map(lambda i: '#' + '%06x' % random.randint(0, 0xFFFFFF), range(n)))
  colors = get_colors(len(alunos))  
  startangle = 90
  shadow = True
  radius = 1.2
  autopct = '%1.1f%%'
  graph = Pie(points, tick_label, colors, startangle, shadow, explode, radius, autopct, 'pie')
  graph.plot()
  return render_template(
    'pages/turma.html', 
    alunos=alunos, 
    turma=name
  )

# Listagem alunos por instituicao:
@app.route('/instituicoes', methods=['GET'])
def listarAlunosPorInstituicao():  
  id = request.args.get('id')
  name = request.args.get('name')
  alunos = db.engine.execute(f'SELECT * FROM aluno WHERE instituicao_id = {id}')
  alunos =  [
    {column: value for column, value in rowproxy.items()} for rowproxy in alunos
  ]
  return render_template(
    'pages/instituicao.html', 
    alunos=alunos, 
    instituicao=name
  )

# Server:
if __name__ == '__main__':
  app.run(
    host='localhost',
    debug=True,
    port=5000,
  )

# Create database (CLI):
# -> python3
# -> from app import db
# -> db.create_all()
