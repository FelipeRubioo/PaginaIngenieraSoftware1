from flask import Flask,flash, render_template,request,redirect,session
import pyodbc
#Inicio conexion a base de datos 
try:
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER=AURORA;DATABASE=TiendaRopa;UID=Felipe;PWD=rubio')
    print("conexion exitosa")
    cursor = connection.cursor()

except Exception as ex:
    print (ex)
#Fin conexion a base de datos 


#app de flask
app = Flask(__name__)
app.secret_key = "asdfvfñfes7u2nairfn"



#Inicio
@app.route("/", methods=['GET','POST'])
def index():
        return redirect("/Login")

#Registro
@app.route("/Registro", methods=["GET","POST"])
def Registro(): 
     if request.method == 'GET':
          return render_template('Registro.html')
     elif request.method == 'POST':
          nombre = request.form['nombre']
          correo = request.form['correo']
          contraseña = request.form['contraseña']
        
          #verifica si el usuario ya existe
          cursor.execute("SELECT correo FROM Clientes where correo = '"+correo+"';")
          filas= len(cursor.fetchall())
          if filas == 0:
            print("no existe el usuario, se creará el usuario")
            cursor.execute("INSERT INTO Clientes(correo,contraseña,nombre) VALUES('" +correo+"','"+contraseña+"','"+nombre+"');")
            connection.commit()

             #verifica que se creo el usuario
            cursor.execute("SELECT correo FROM Clientes where correo = '"+correo+"';")
            filas = len(cursor.fetchall())
            if filas ==1:
                print("se creo el usuario")
            elif filas == 0:
               print("no se creo el usuario")
            #Redirige al Login
            return redirect("/Login")
     elif filas == 1:
        print("existe el usuario, no se creara el nuevo registro")

#Login 
@app.route("/Login", methods= ["GET","POST"])
def Login():

    if request.method == 'GET':
        return render_template('Login.html')
    
    elif request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña'] 

        #verifica que el usuario existe y la contraseña es correcta
        cursor.execute("SELECT correo FROM Clientes where correo = '"+ correo +"' AND contraseña = '"+contraseña+"'")
        resultado = cursor.fetchall()
        filas = len(resultado)

        #el query dio un resultado, el usario existe
        if filas == 1:
            print("se encontro el usuario")
            session['logged'] = True
            cursor.execute("SELECT idCliente FROM Clientes where correo = '"+ correo +"'")
            resultado = cursor.fetchall()
            session['idCliente'] = resultado[0][0]
            cursor.execute("Delete from Carrito where idCliente = ?",(session['idCliente'],))
            connection.commit()
            return redirect("/HomeCliente")
        #el query no dio match, el usuario no existe
        else:
            print("no se encontro el usuario")
            session['logged'] = False
            return redirect("/Error")

 #Login 
@app.route("/Logout", methods= ["GET","POST"])
def Logout():
    session['logged'] = False
    cursor.execute("Delete from Carrito where idCliente = ?",(session['idCliente'],))
    connection.commit()
    if request.method == 'GET':
       return redirect("/Login")
    
   

#HomeCliente 
@app.route("/HomeCliente", methods= ["GET","POST"])
def HomeCliente():
    metodo = request.method
    if metodo == 'GET':
            if session['logged'] == True:
                return render_template('HomeCliente.html')
                
            else:
                return redirect("/Error")
    elif metodo == 'POST':
            categoria = request.form['categoria']
            idCategoria = request.form['idCategoria']
            return redirect(f"/Categoria/{categoria}/{idCategoria}")
           
            

#Categoria
@app.route("/Categoria/<categoria>/<idCategoria>", methods= ["GET","POST"])
def Categoria(categoria,idCategoria):
    metodo = request.method
    if metodo == 'GET':
            if session['logged'] == True:
                cursor.execute("SELECT * FROM Prenda where idCategoria= " + idCategoria)
                prendas = cursor.fetchall()
                cursor.execute("SELECT nombre FROM Categoria WHERE idCategoria= ? ", (idCategoria,))
                categoria = cursor.fetchone()
                return render_template("Categoria.html",prendas = prendas, categoria = categoria)
            else:
                return redirect("/Error")
    elif metodo == 'POST':
         #se agrega id de articulo y cantidad del mismo al carrito
         idCliente = session['idCliente']
         idPrenda = request.form['idPrenda']
         cantidad = request.form['cantidad']
         cursor.execute("INSERT INTO Carrito (idCliente, idPrenda, cantidad) VALUES (?, ?, ?);", (idCliente, idPrenda, cantidad))
         connection.commit()
         #Vuelve a cargar la pagina
         return redirect(request.referrer)
         
#Carrito
@app.route("/Carrito", methods= ["GET","POST"])
def Carrito():
    metodo = request.method
    if metodo == 'GET':
            if session['logged'] == True:
                arreglo = []

                #Obtiene los articulos del cliente que tenga en el carrito 
                idCliente = session['idCliente']
                cursor.execute("SELECT * FROM Carrito WHERE idCliente = ?;", (idCliente,))
                carrito = cursor.fetchall()
                
                for compra in carrito:
                    idPrenda = compra[1]
                    cantidad = compra[2]
                    cursor.execute("SELECT nombre, precio, talla FROM Prenda WHERE idPrenda = ?;", (idPrenda,))
                    datos = cursor.fetchall()
                    datos.append(cantidad)
                    arreglo.append(datos)
                
                return render_template("Carrito.html",prendasCarrito = arreglo)
                
            else:
                return redirect("/Error")     
    elif metodo == 'POST':
        print("compra hecha:")
        arreglo = session.get('arreglo')
        print(arreglo)
        
    
#Pantalla de erorr 
@app.route("/Error", methods= ["GET","POST"])
def Error():
    return render_template('Error.html')
    

if __name__ == "__main__":
    app.run(debug=True)


