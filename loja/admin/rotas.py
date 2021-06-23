from flask import render_template, session, request, url_for, redirect, flash
from wtforms import form
from loja.produtos.models import Addproduto,Marca, Categoria
from loja import app, db, bycrpt
from .formulario import RegistrationForm, LoginFormulario

from .models import User
import os




@app.route('/')
def home(): 
    
    produtosDesconto = Addproduto.query.filter(Addproduto.discount > 0)
    produtos = Addproduto.query.filter(Addproduto.discount <= 0)
    categorias = Categoria.query.all()
    return render_template('admin/index.html', title='Crypto$tore', produtos=produtos, categorias=categorias, produtosDesconto=produtosDesconto)


@app.route('/categoria/<int:id>', methods=['GET','POST'])
def obter_categoria(id):
    categorias1 = Addproduto.query.filter_by(categoria_id=id)
    categorias = Categoria.query.all()

    return render_template('admin/index.html', title='Crypto$tore', categorias1=categorias1, categorias=categorias)




@app.route('/admin')
def admin():
    if 'email'  not in session:
        flash('Faça login para prosseguir!', 'danger')
        return redirect(url_for('login'))

    if ('email' in session) and (session['email'] == 'j13vvc@gmail.com' or 'arturluz933@gmail.com'):
        produtos = Addproduto.query.all()
        return render_template('admin/admin.html',title='Pagina admin', produtos=produtos)
    else:
        return redirect(url_for('home'))


@app.route('/marcas')
def marcas():  
    if 'email'  not in session:
        flash('Faça login para prosseguir!', 'danger')
        return redirect(url_for('login'))

    if ('email' in session) and (session['email'] == 'j13vvc@gmail.com' or 'arturluz933@gmail.com'):  
        marcas = Marca.query.order_by(Marca.id.desc()).all()
        return render_template('admin/marca.html', title='Pagina Marcas', marcas=marcas)
    else:
        return redirect(url_for('home'))

@app.route('/categoria')
def categoria():
    if 'email'  not in session:
        flash('Faça login para prosseguir!', 'danger')
        return redirect(url_for('login'))
        
    if ('email' in session) and (session['email'] == 'j13vvc@gmail.com' or 'arturluz933@gmail.com'): 
        categoria = Categoria.query.order_by(Categoria.id.desc()).all()
        return render_template('admin/marca.html', title='Pagina categoria', categoria=categoria)
    else:
        return redirect(url_for('home'))


@app.route('/produto/<int:id>', methods =['GET','POST'])
def produto(id):
    produto = Addproduto.query.get_or_404(id)  
    categorias = Categoria.query.all()    
   
        
    return render_template('admin/produto.html', title='Produto', produto=produto, form=form, categorias=categorias )






@app.route('/registrar', methods=['GET','POST'])
def registrar():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():        
        hash_password = bycrpt.generate_password_hash(form.password.data)        
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password= hash_password)        
        db.session.add(user)
        db.session.commit()
        flash(f'Obrigado {form.name.data} por registrar!', 'success')
        return redirect(url_for('login'))  
    else: 
        return render_template('admin/registrar.html', form=form , title="Pagina de registro")


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginFormulario(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bycrpt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            

            name_do_email = User.query.filter_by(email=form.email.data).first() 
            username = name_do_email.username 

            flash(f'Olá, {username}!', 'success')
            return redirect(request.args.get('next')or url_for('home'))
        else:
            flash('Não foi possivel logar no sistema.')
    return render_template('admin/login.html', form=form, title='Pagina Login')

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('Nenhum usuário logado!')
    return redirect(url_for('home'))

'''
prods = "{[1,2,10,90]}";

prodarray = prods.split(",")

prodarray[0]
'''

@app.route('/pagamento')
def pagamento():
    if 'email'  not in session:
        flash('Faça login para prosseguir!', 'danger')
        return redirect(url_for('login'))
    flash("Compra em andamento.")
    return render_template('admin/pagamento.html')

@app.route('/enviar')
def enviar():
    flash("Mensagem enviada!")
    return render_template('admin/index.html')