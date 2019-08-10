# Imports:
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# App:
app = Flask(__name__)
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
    fields = ('id', 'name')

# Instituicao Class/Model:
class Instituicao(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(255))
  def __init__(self, name):
    self.name = name

# Instituicao Schema:
class InstituicaoSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name')

# Aluno Class/Model:
class Aluno(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(255))
  since = db.Column(db.Date)
  solved = db.Column(db.Float)
  tried = db.Column(db.Float)
  submissions = db.Column(db.Float)
  points = db.Column(db.Float)
  place = db.Column(db.Float)
  instituicao_id = db.Column(
    db.Integer, 
    db.ForeignKey('instituicao.id'), nullable=False
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
    fields = ('id', 'aluno_id', 'turma_id')

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
@app.route('/', methods=['GET'])
def index():  
  return render_template('pages/index.html')

# Server:
if __name__ == '__main__':
  app.run(debug=True)

# Create database (CLI):
# -> python3
# -> from app import db
# -> db.create_all()
