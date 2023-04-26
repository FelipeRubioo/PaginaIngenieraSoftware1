from flask import Flask,flash, render_template,request,redirect,session
#from passlib.hash import sha256_crypt

#pypyodbc
#import pypyodbc as pypy

'''
db_host = 'AURORA'
db_name = 'dbo.Prenda'
db_user = 'Felipe'
db_password = ''

connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';PWD=' + db_password +';'
db = pypy.connect(connection_string)
'''




#app de flask
app = Flask(__name__)
app.secret_key = "asdfvfñfes7u2nairfn"




@app.route("/", methods=['GET','POST'])
def index():
       # return render_template('Home.html')
        return render_template('Inicio.html')

#Login 
@app.route("/Login", methods= ["GET","POST"])
def Login():
    if request.method == 'GET':
        return render_template('Login.html')
    
    
#HomeEmpleado 
@app.route("/HomeEmpleado", methods= ["GET","POST"])
def HomeEmpleado():
    metodo = request.method
    if metodo == 'GET':
        return render_template('HomeEmpleado.html')
    #elif metodo == 'POST':
     #    correoUsuario =


if __name__ == "__main__":
    app.run(debug=True)


