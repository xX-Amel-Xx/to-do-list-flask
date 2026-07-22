from flask import Flask, render_template,redirect, request
from models import db, Lista
from datetime import datetime
import locale

app =Flask (__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lista.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

db.init_app(app)
with app.app_context():
     db.create_all()

#ROTA DO TO_DO_LIST
@app.route("/To-Do-List")
def ListaFazeres():
    todas = Lista.query.filter_by(todas=True).all()

    pendentes = Lista.query.filter_by(concluida=False).all()
    concluidas = Lista.query.filter_by(concluida=True).all()
    quantidade = Lista.query.filter_by(concluida=True).count()

    hoje = datetime.now().strftime("%d de %B")
    return render_template(
        "To-Do-List.html",
        todas=todas,
        pendentes=pendentes,
        concluidas=concluidas,
        quantidade=quantidade,
        hoje=hoje,
    
    )


#ROTA TAREFAS 
@app.route('/tarefas',methods=['POST'])
def tarefas ():

    sugestao=request.form["texto"]

    if sugestao.strip():

        nova_tarefa=Lista(
            texto=sugestao,
            todas=True,
            concluida=False
        )

        db.session.add(nova_tarefa)
        db.session.commit()
    return redirect("/To-Do-List")


#ROTA DELETAR
@app.route("/deletar/<int:id>")
def deletar(id):
     registro = Lista.query.get(id)
     if registro:
        db.session.delete(registro)
        db.session.commit()
     return redirect("/To-Do-List")

#ROTA PENDENTE
@app.route("/pendente/<int:id>")
def pendente(id):
    registro = Lista.query.get(id)

    if registro:
        registro.concluida  = not registro.concluida
        registro.todas=False
        db.session.commit()
    return redirect("/To-Do-List")

#ROTA DELETAR CONCUIDAS
@app.route("/deletPen",methods=['POST'])

def deletPen():
    concluidas=Lista.query.filter_by(concluida=True).all()
    for registro in concluidas:
        db.session.delete(registro)
    db.session.commit()
    return redirect("/To-Do-List")
if __name__ == "__main__":
     app.run(debug=True)
