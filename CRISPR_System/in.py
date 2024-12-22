from flask import Flask, request, render_template
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Diccionario de enfermedades genéticas (ejemplo)
enfermedades_geneticas = {
    "BRCA1": {"nombre": "Cáncer de mama", "secuencia": "AGCT"},
    "CFTR": {"nombre": "Fibrosis quística", "secuencia": "TGTT"},
    "HTT": {"nombre": "Enfermedad de Huntington", "secuencia": "CAG"},
    "DMD": {"nombre": "Distrofia Muscular de Duchenne", "secuencia": "GGA"},
    "HBB": {"nombre": "Anemia de Células Falciformes", "secuencia": "GTG"},
    "FBN1": {"nombre": "Síndrome de Marfan", "secuencia": "TGG"},
    "PAH": {"nombre": "Fenilcetonuria", "secuencia": "GAA"},
    "GALT": {"nombre": "Galactosemia", "secuencia": "GCT"},
    "ATP7B": {"nombre": "Enfermedad de Wilson", "secuencia": "TAT"},
    "SMN1": {"nombre": "Atrofia Muscular Espinal", "secuencia": "TGA"},
    "COL1A1": {"nombre": "Osteogénesis Imperfecta", "secuencia": "GGT"},
    "FMR1": {"nombre": "Síndrome de X Frágil", "secuencia": "CGG"},
    "GAA": {"nombre": "Enfermedad de Pompe", "secuencia": "GAA"},
    "NPC1": {"nombre": "Enfermedad de Niemann-Pick", "secuencia": "TCT"},
    "TSC1": {"nombre": "Esclerosis Tuberosa", "secuencia": "TGC"},
    "PKD1": {"nombre": "Enfermedad Poliquística Renal", "secuencia": "CCT"},
    "MLH1": {"nombre": "Síndrome de Lynch", "secuencia": "AAG"},
    "RET": {"nombre": "Neoplasia Endocrina Múltiple", "secuencia": "GAC"},
    "VHL": {"nombre": "Síndrome de Von Hippel-Lindau", "secuencia": "GTC"},
    "NF1": {"nombre": "Neurofibromatosis Tipo 1", "secuencia": "TGA"},
    "RB1": {"nombre": "Retinoblastoma", "secuencia": "GCG"},
    "WT1": {"nombre": "Tumor de Wilms", "secuencia": "GGA"},
    "P53": {"nombre": "Síndrome de Li-Fraumeni", "secuencia": "TGC"},
    "APC": {"nombre": "Poliposis Adenomatosa Familiar", "secuencia": "GGA"},
    "SMAD4": {"nombre": "Síndrome de Juvenil Poliposis", "secuencia": "GCT"},
    "PTEN": {"nombre": "Síndrome de Cowden", "secuencia": "TTA"},
    "CDH1": {"nombre": "Cáncer Gástrico Hereditario", "secuencia": "GTT"},
    "MEN1": {"nombre": "Neoplasia Endocrina Múltiple Tipo 1", "secuencia": "TGC"},
    "STK11": {"nombre": "Síndrome de Peutz-Jeghers", "secuencia": "GCT"},
    "TP53": {"nombre": "Síndrome de Li-Fraumeni", "secuencia": "TGC"}
}

bases_crispr = {
    "TP53": {
        "cadena": "5'-ATGGCAGGAGGTCAGGCC-3'",
        "name": "Gen del supresor de tumores p53"
    },
    "BRCA1": {
        "cadena": "5'-ATGGCTAGCTGCTGCTGCT-3'",
        "name": "Gen relacionado con el cáncer de mama"
    },
    "EGFR": {
        "cadena": "5'-ATGAGGAGGCTGCTGCTGCT-3'",
        "name": "Gen del receptor del factor de crecimiento epidérmico"
    },
    "CFTR": {
        "cadena": "5'-ATGGGTTTCTGTTTCTGTT-3'",
        "name": "Gen asociado a la fibrosis quística"
    },
    "HBB": {
        "cadena": "5'-ATGGTGACCTGAGGTCAC-3'",
        "name": "Gen de la beta-globina"
    },
    "SOD1": {
        "cadena": "5'-ATGCTGCTGCTGCTGCTG-3'",
        "name": "Gen de la superóxido dismutasa 1"
    },
    "MYC": {
        "cadena": "5'-ATGAGGAGGCTGCTGCTGCT-3'",
        "name": "Gen que codifica un factor de transcripción"
    },
    "KRAS": {
        "cadena": "5'-ATGGGTCGACGTCGACGTC-3'",
        "name": "Gen que codifica una proteína G"
    },
    "PTEN": {
        "cadena": "5'-ATGGGAGGAGGTCAGGCC-3'",
        "name": "Gen supresor de tumores"
    },
    "ALK": {
        "cadena": "5'-ATGACGACGACGACGACG-3'",
        "name": "Gen relacionado con el cáncer de pulmón"
    }
}


def es_adn(adn):
    caracteres= {'A', 'T', 'C', 'G'}
    for i in adn.upper():
        if i not in caracteres:
            return False
    else:
        return True
    
@app.route('/analizar', methods=['POST'])
def analizar():
    
    if request.method=='POST':
        adn= request.form['adn'].strip().upper()
        resultados = []
        resultados_crispr=[]
        
    if es_adn(adn):
        for gen, info in enfermedades_geneticas.items():
            secuencia = info['secuencia']
            for match in re.finditer(secuencia, adn):
                resultados.append({
                    "gen": gen,
                    "posicion": match.start(),
                    "enfermedad": info['nombre']})
                
        for gen, info in bases_crispr.items():
            cadena = info['cadena']
            if cadena in adn:  # Verificar si la cadena está en la cadena de ADN
                resultados_crispr.append({
                    "gen": gen,
                    "nombre_enfermedad": info['name'],
                    "cadena": cadena
                })

        # Renderizar los resultados en resultados.html
        return render_template('resultados.html',resultados=resultados, resultados_crispr=resultados_crispr)  
    else:
        return render_template('resultados.html', error="No es una cadena de ADN")        
        


@app.route('/edicion_genetica')
def edicion_genetica():
    return render_template('edicion_genetica.html')
    
@app.route('/crispr')
def crispr():
    return render_template('crispr.html')
    
@app.route('/diccionarios')
def diccionarios():
    return render_template('diccionarios.html')
    
if __name__ == '__main__':
    app.run(debug=True)
