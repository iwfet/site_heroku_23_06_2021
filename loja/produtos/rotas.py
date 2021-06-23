from flask import redirect, render_template, url_for, flash, request,session
from werkzeug.utils import secure_filename
from .forms import Addprodutos
from loja import db, app, photos
from .models import Marca, Categoria,Addproduto
import secrets


@app.route('/addmarca', methods =['GET','POST'])
def addmarca():  
    if 'email'  not in session:
        flash('Faça login para prosseguir!', 'danger')
        return redirect(url_for('login'))

    if (request.method == "POST") :
        if ('email' in session) and (session['email'] == 'j13vvc@gmail.com' or 'arturluz933@gmail.com'):
            getmarca = request.form.get('marca')
            marca = Marca(name=getmarca)
            db.session.add(marca)
            flash(f'A marca {getmarca} foi cadastrada com sucesso', 'success')
            db.session.commit()
            return redirect(url_for('addmarca'))
        else:
            flash(f'Usuário sem autorização!', 'danger')
    return render_template('/produtos/addmarca.html', marcas='marcas')


@app.route('/addcat', methods =['GET','POST'])
def addcat():
    if 'email'  not in session:
        flash('Faça login para prosseguir!', 'danger')
        return redirect(url_for('login'))

    if request.method == "POST":
        if ('email' in session) and (session['email'] == 'j13vvc@gmail.com' or 'arturluz933@gmail.com'):
            getcategoria = request.form.get('categoria')
            cat = Categoria(name=getcategoria)
            db.session.add(cat)
            flash(f'A categoria {getcategoria} foi cadastrada com sucesso', 'success')
            db.session.commit()
            return redirect(url_for('addcat'))
        else:
            flash(f'Usuário sem autorização!', 'danger')
    return render_template('/produtos/addmarca.html')




@app.route('/addproduto',  methods =['GET','POST'])
def addproduto():
    if 'email'  not in session:
        flash('Faça login para prosseguir!', 'danger')
        return redirect(url_for('login'))

    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    form = Addprodutos(request.form) 
    if request.method == "POST": 
        if ('email' in session) and (session['email'] == 'j13vvc@gmail.com' or 'arturluz933@gmail.com'):

            name = form.name.data
            preco = form.preco.data
            discount = form.discount.data
            stock = form.stock.data
            discription = form.discription.data
            colors = form.colors.data 
            marca = request.form.get('marca')
            categoria = request.form.get('categoria')        

            image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex()+ ".")
            image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex()+ ".")
            image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex()+ ".")
            


            addprotu = Addproduto(name=name,preco=preco,discount=discount,stock=stock,discription=discription,colors=colors,marca_id=marca,categoria_id=categoria,imagem_1=image_1, imagem_2=image_2, imagem_3=image_3
            )

            db.session.add(addprotu)
            flash(f'Porduto {name} foi cadastrada com sucesso', 'success')  
            db.session.commit()
            return redirect(url_for('admin'))
        else:
            flash(f'Usuário sem autorização!', 'danger')      

    return render_template('produtos/addproduto.html', title="Cadastrar Produtos", form=form, marcas=marcas, categorias=categorias)



@app.route('/updatemarca/<int:id>', methods =['GET','POST'])
def updatemarca(id):
    if 'email'  not in session:
        flash('Faça login para prosseguir!', 'danger')
        return redirect(url_for('login'))

    updatemarca = Marca.query.get_or_404(id)
    marca = request.form.get('marca')
    if request.method == "POST":
        if ('email' in session) and (session['email'] == 'j13vvc@gmail.com' or 'arturluz933@gmail.com'):
            updatemarca.name = marca        
            flash(f'Fabricante atualizado com successo', 'success')  
            db.session.commit()  
            return redirect(url_for('marcas')) 
        else:
            flash(f'Usuário sem autorização!', 'danger')   
    return render_template('/produtos/updatemarca.html', title='Atulizar Fabricantes', updatemarca=updatemarca)



@app.route('/updatecat/<int:id>', methods =['GET','POST'])
def updatecat(id):
    if 'email'  not in session:
        flash('Faça login para prosseguir!', 'danger')
        return redirect(url_for('login'))

    updatecat = Categoria.query.get_or_404(id)
    categoria = request.form.get('categoria')
    if request.method == "POST":
        if ('email' in session) and (session['email'] == 'j13vvc@gmail.com' or 'arturluz933@gmail.com'):
            updatecat.name = categoria      
            flash(f'Fabricante atualizado com successo', 'success')  
            db.session.commit()  
            return redirect(url_for('categoria')) 
        else:
            flash(f'Usuário sem autorização!', 'danger')   
    return render_template('/produtos/updatemarca.html', title='Atulizar Fabricantes',updatecat=updatecat)





@app.route('/updateproduto/<int:id>', methods =['GET','POST'])
def updateproduto(id):
    if 'email'  not in session:
        flash('Faça login para prosseguir!', 'danger')
        return redirect(url_for('login'))

    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    produto = Addproduto.query.get_or_404(id)
    marca = request.form.get('marca')
    categoria = request.form.get('categoria')
    form = Addprodutos(request.form)
    if request.method =="POST":
        if ('email' in session) and (session['email'] == 'j13vvc@gmail.com' or 'arturluz933@gmail.com'):
            produto.name = form.name.data
            produto.preco = form.preco.data
            produto.discount = form.discount.data

            produto.marca_id = marca
            produto.categoria_id = categoria
            
            produto.stock = form.stock.data
            produto.colors = form.colors.data
            produto.discription = form.discription.data

            db.session.commit()
            flash(f'Produto atualizado com successo', 'success') 
            return redirect(url_for('admin'))
        else:
            flash(f'Usuário sem autorização!', 'danger')

    form.name.data = produto.name
    form.preco.data = produto.preco
    form.discount.data = produto.discount
    form.stock.data = produto.stock
    form.colors.data = produto.colors
    form.discription.data = produto.discription
    

    return render_template('/produtos/updateproduto.html', title='Atulizar Produtos',form=form, marcas=marcas, categorias=categorias, produto=produto)











