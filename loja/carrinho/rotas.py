from flask import render_template, session, request, url_for, redirect, flash, current_app
from loja.produtos.models import Addproduto,Categoria
from loja.carrinho.models import Carrinho
from loja import app, db


@app.route('/addcarrinho/<int:id>', methods=['POST','GET'])
def addcarrinho(id): 
    if 'email'  not in session:
        flash('Faça login para prosseguir!', 'danger')
        return redirect(url_for('login'))

    if (request.method =='POST'): 
        usuario = session['email'] 
        quantidade = request.form.get('quantidade')       
            
        addprodutocarrinho = Carrinho(usuario=usuario, idproduto=id, quantidade=quantidade ) 
        db.session.add(addprodutocarrinho)
        db.session.commit()    
        
    return redirect(request.referrer)  
      
      
@app.route('/carrinho', methods=['POST','GET'])
def carrinho():
    if 'email'  not in session:
        flash('Faça login para prosseguir!', 'danger')
        return redirect(url_for('login'))

    usuario = session['email']         
    carrinho = Carrinho.query.filter_by(usuario=usuario).all()  
    categorias = Categoria.query.all() 
    produtosStock = Addproduto.query.filter(Addproduto.stock <= 0)
    
    total = 0
    for carin in carrinho:
        subtotal = carin.quantidade * carin.addproduto.preco
        total = total + subtotal 
        
    return render_template('admin/carrinho.html', title='Pagina Login', carrinho=carrinho, categorias=categorias, grande_tota=total)

@app.route('/deleteitem/<int:id>', methods=['POST','GET'])
def deleteitem(id):
    if 'email'  not in session:
        flash('Faça login para prosseguir!', 'danger')
        return redirect(url_for('login'))
    
    itemcarrinho = Carrinho.query.get_or_404(id)
    print(itemcarrinho)
    db.session.delete(itemcarrinho)
    db.session.commit()
    
    return redirect(url_for('carrinho')) 





@app.route('/updateitem/<int:id>', methods=['POST','GET'])
def updateitem(id):
    if 'email'  not in session:
        flash('Faça login para prosseguir!', 'danger')
        return redirect(url_for('login'))
    
    
    
    if (request.method =='POST'): 
        quantidad = request.form.get('quantidade')  
        print(quantidad) 
        
        updated_this = Carrinho.query.filter_by(id=id).first()
        
        updated_this.quantidade = quantidad
        
        db.session.commit()
    
    return redirect(url_for('carrinho')) 