from flask import *  
app = Flask(__name__)  

def db():
  con = sqlite3.connect("employee.db") 
  return con
  
@app.route('/')
def sendData():
  return render_template('sendData.html')

@app.route('/login',methods = ['POST'])  
def login():  
      uname=request.form['uname']  
      passwrd=request.form['pass']  
      if uname=="yasir" and passwrd=="yasir@developer":  
          return "<h1>Welcome " + uname  
   
if __name__ == '__main__':  
   app.run(debug = True)  