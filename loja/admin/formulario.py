from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    name = StringField('Nome completo', [validators.Length(min=4, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Endereço de Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Digite sua senha', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Utilize a mesma senha!')
    ])
    confirm = PasswordField('Digite sua senha novamente')

class LoginFormulario(Form):
    email = StringField('Endereço de Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Sua senha', [ validators.DataRequired()])

         
   
   

