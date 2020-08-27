from flask import Flask,redirect,url_for,render_template,request
import araba_fiyat
from flask_mysqldb import MySQL


app = Flask(__name__)



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass'
app.config['MYSQL_DB'] = 'arabalar'
mysql = MySQL(app)


@app.route("/",methods=["POST","GET"])
def index():
	if request.method == "POST":
		model = request.form["araba_model"]
		yil = request.form["araba_yil"]
		ort_fiyat = araba_fiyat.piyasa(yil,model)
		cursor = mysql.connection.cursor()
		insert_values = (yil,model,ort_fiyat)
		query = 'INSERT INTO araba_fiyat (yil,model,fiyat) values(%s,%s,"%s")'
		if ort_fiyat > 0:
			cursor.execute(query,(yil,model,ort_fiyat))
			mysql.connection.commit()
			cursor.close()
			text1 = str(yil)+" Model "+str(model)+" Otomobilin Ortalama Piyasa Değeri: "+str(ort_fiyat)+" TL"
		else:
			text1="Arama herhangi bir sonuç vermedi."
		return render_template('index.html',piyasa_fiyati=text1)
	else:
		return render_template('index.html',piyasa_fiyati=" ")

@app.route("/gecmis_aramalar", methods=["POST","GET"])
def gecmis_aramalar():
	cursor = mysql.connection.cursor()
	cursor.execute("select yil,model,fiyat from araba_fiyat")
	
	gecmis = cursor.fetchall()
	if request.method == "POST":
		silme_onay = request.form["sil"]
		if silme_onay=="tum_veriyi_sil":
			cursor.execute("truncate arabalar.araba_fiyat")
		else:
			None
		return redirect("/gecmis_aramalar")
	else:
		None
	return render_template("gecmis_aramalar.html",gecmis=gecmis)

if __name__=="__main__":
	app.run(debug=True)

  
