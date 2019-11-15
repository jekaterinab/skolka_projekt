from flask import Flask, render_template, request
from databaza import get_activities
from databaza import skolky_mesto
from databaza import tabulka_skolky_detail
import databaza 

app = Flask(__name__)

@app.route('/')
def home():
    #print(get_activities())
    return render_template('index.html')

@app.route('/ranapece/')
def ranapece():
    return render_template('ranapece.html')

@app.route('/skolky/')
def skolky():
    return render_template('skolky.html', city=databaza.skolky_mesto())

@app.route('/odlehcovaci_pece/')
def odlehcovaci_pece():
    return render_template('odlehcovaci_pece.html')

@app.route('/skolky/', methods=['POST'])
def skolky_post():
 if request.method == 'POST':
    nazev= request.form.get("nazev")
    mesto= request.form.get("city")
    ulice= request.form.get("ulice")
    mail= request.form.get("mail")
    web= request.form.get("web")
    kontakt= request.form.get("kontakt")
    postizeni = []
    if "mentalni" in request.form:
      postizeni.append("mentalni")
      postizeni.append("mentálně")
      postizeni.append("mentalnim")
      postizeni.append("mentálním postižením")
      postizeni.append("mentalne")
      postizeni.append("downuv syndrom")

    if "zrakove" in request.form:
      postizeni.append("zrakovým")
      postizeni.append("zrakove postizeni")
      postizeni.append("zrakove")
      postizeni.append("smyslově")
      postizeni.append("logopedicke zrakove")
      postizeni.append("smyslove postizeni")
      postizeni.append("smyslove")
      postizeni.append("dualni senzoricke")
    if "sluchove" in request.form:
      postizeni.append("sluchove")
      postizeni.append("smyslově")
      postizeni.append("sluchove postizení")
      postizeni.append("sluchovým")
      postizeni.append("smyslove postizeni")
      postizeni.append("smyslove")
      postizeni.append("dualni senzoricke")

    if "recove" in request.form:
      postizeni.append("logopedicke")
      postizeni.append("logopedicke zrakove")
      postizeni.append("komunikacne")
      postizeni.append("kom")
      postizeni.append("vady reči")
      postizeni.append("vady reci")
      postizeni.append("komunikacni")
      postizeni.append("recove")
      
    if "telesne" in request.form:
      postizeni.append("telesne")
      postizeni.append("tele")
      postizeni.append("telesne kombinovane")
      postizeni.append("tělesne")
      postizeni.append("teslenim")
      postizeni.append("tělesným")
      postizeni.append("pohybove") 

    if "kombinovane" in request.form:
      postizeni.append("kombinovane")
      postizeni.append("s vice vadami")
      postizeni.append("kobminovane")
      postizeni.append("vice vad")
      postizeni.append("s vice vadami")
      postizeni.append("telesne kombinovane")

    if "autistickeho" in request.form:
      postizeni.append("autistismus")
      postizeni.append("kombinovaným postižením a děti s poruchami autistického spektra")
      postizeni.append("autismem")
      postizeni.append("autisticke")
      postizeni.append("autistickeho spektra")
      postizeni.append("autisticke")
      postizeni.append("poruchy autistickeho spektra")

    if "poruchauceni" in request.form:
      postizeni.append("porucha uceni") 
      postizeni.append("adhd")
      postizeni.append("snizenim rozumovymi schopnostami")
      postizeni.append("hyperaktivita")

    expectation_table = databaza.skolky_vyhladavanie(nazev, postizeni, mesto, ulice)
    lngs = [ x["lng"] for x in expectation_table ]
    lats = [ x["lat"] for x in expectation_table ]
    center = [(max(lngs)-min(lngs))/2 + min(lngs),(max(lats)-min(lats))/2 + min(lats)]
 return render_template("skolky_search.html", center = center,
    expectation_table=expectation_table
    )

@app.route('/skolka/')
def skolka():
  return render_template("skolka.html")
    
@app.route('/skolka/<int:id_skolky>', methods=['GET'])
def skolky_detail(id_skolky):
   skolky_detail=databaza.tabulka_skolky_detail(id_skolky)
   return render_template("skolka.html",
   skolky_detail=skolky_detail,
   )
 
@app.route('/takulka_skolky')
def tabulka_skolky ():
    expectation_table = databaza.tabulka_skolky()
    print(expectation_table)
    return render_template("tabulka_skolky.html",
    expectation_table=expectation_table,
    )

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def pagenot_found(e):
    return render_template("500.html")

if __name__ == '__main__':
    app.run(debug=True)
