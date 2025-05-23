import os
import json
import re
from flask import Flask, render_template, request

app = Flask(__name__)

# Función para cargar datos desde archivos JSON
def cargar_json(nombre_archivo):
    """Carga datos desde un archivo JSON"""
    ruta_archivo = os.path.join(os.path.dirname(__file__), nombre_archivo)
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {nombre_archivo}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: El archivo {nombre_archivo} no contiene JSON válido")
        return {}

# Cargar datos desde archivo JSON
bases_crispr = cargar_json('bases_crispr.json')

# Textos informativos para las páginas
textos_informativos = {
    "crispr": """
        <h2>Tecnología CRISPR</h2>
        <p>CRISPR (Repeticiones Palindrómicas Cortas Agrupadas y Regularmente Espaciadas) es una tecnología revolucionaria de edición genética que permite a los científicos modificar secuencias de ADN con precisión.</p>
        <p>Funciona como unas "tijeras moleculares" que pueden cortar el ADN en lugares específicos, permitiendo eliminar, añadir o alterar secciones del genoma.</p>
        <p>Esta tecnología tiene el potencial de transformar la medicina al permitir el tratamiento de enfermedades genéticas, el desarrollo de nuevas terapias contra el cáncer y la creación de organismos modificados genéticamente.</p>
        <p>CRISPR se basa en un sistema inmune natural encontrado en bacterias, que ha sido adaptado como una poderosa herramienta de ingeniería genética.</p>
    """
}

def es_adn(adn):
    """Verifica si una cadena contiene solo caracteres válidos de ADN (A, T, C, G)"""
    if not adn:  # Verificar si la cadena está vacía
        return False
    caracteres = {'A', 'T', 'C', 'G'}
    for i in adn.upper():
        if i not in caracteres:
            return False
    return True

def limpiar_secuencia_crispr(secuencia):
    """Elimina los caracteres no nucleótidos de la secuencia CRISPR."""
    # Eliminar el formato 5'- y -3' y cualquier otro carácter no ATCG
    return re.sub(r'[^ATCG]', '', secuencia.upper())

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analizar', methods=['POST'])
def analizar():
    if request.method == 'POST':
        adn = request.form['adn'].strip().upper()
        resultados_crispr = []
        
        if es_adn(adn):
            # Buscar secuencias CRISPR
            for gen, info in bases_crispr.items():
                # Limpiar la cadena CRISPR para comparación
                cadena_limpia = limpiar_secuencia_crispr(info['cadena'])
                
                # Verificar si la cadena limpia no está vacía
                if not cadena_limpia:
                    continue
                
                # Buscar coincidencias parciales (substrings)
                if len(cadena_limpia) >= 6:  # Establecer un mínimo de longitud para evitar falsos positivos
                    # Buscar coincidencias de al menos 6 nucleótidos consecutivos
                    for i in range(len(cadena_limpia) - 5):
                        fragmento = cadena_limpia[i:i+6]
                        if fragmento in adn:
                            resultados_crispr.append({
                                "gen": gen,
                                "nombre_enfermedad": info['name'],
                                "cadena": info['cadena'],
                                "cadena_coincidente": fragmento,
                                "coincidencia_parcial": True,
                                "descripcion": info.get('descripcion', 'No hay descripción disponible')
                            })
                            break  # Evitar múltiples coincidencias del mismo gen
                
                # También verificar coincidencia completa
                if cadena_limpia in adn:
                    # Actualizar el resultado existente o agregar uno nuevo
                    for resultado in resultados_crispr:
                        if resultado["gen"] == gen:
                            resultado["coincidencia_parcial"] = False
                            break
                    else:
                        resultados_crispr.append({
                            "gen": gen,
                            "nombre_enfermedad": info['name'],
                            "cadena": info['cadena'],
                            "coincidencia_parcial": False,
                            "descripcion": info.get('descripcion', 'No hay descripción disponible')
                        })
            
            # Imprimir información de depuración
            print(f"ADN analizado: {adn}")
            print(f"Resultados CRISPR: {len(resultados_crispr)}")
            
            return render_template('resultados.html',
                                  resultados_crispr=resultados_crispr,
                                  adn_input=adn)
        else:
            return render_template('resultados.html',
                                  error="La secuencia ingresada no es una cadena de ADN válida. Solo se permiten los caracteres A, T, C y G.",
                                  adn_input=adn)

@app.route('/crispr')
def crispr():
    return render_template('crispr.html', texto_informativo=textos_informativos["crispr"])

@app.route('/diccionarios')
def diccionarios():
    return render_template('diccionarios.html',
                          bases_crispr=bases_crispr)

@app.route('/test_coincidencias/<adn_test>')
def test_coincidencias_route(adn_test):
    """Ruta para probar coincidencias (útil para depuración)"""
    adn_test = adn_test.upper()
    resultados = []
    
    for gen, info in bases_crispr.items():
        cadena_limpia = limpiar_secuencia_crispr(info['cadena'])
        
        # Buscar coincidencias parciales
        for i in range(len(cadena_limpia) - 5):
            fragmento = cadena_limpia[i:i+6]
            if fragmento in adn_test:
                resultados.append({
                    "gen": gen,
                    "cadena_original": info['cadena'],
                    "cadena_limpia": cadena_limpia,
                    "fragmento": fragmento
                })
                break
    
    return {
        "adn_test": adn_test,
        "resultados": resultados
    }

if __name__ == '__main__':
    # Verificar que las secuencias se limpien correctamente al iniciar
    print("Verificando limpieza de secuencias CRISPR:")
    for gen, info in bases_crispr.items():
        cadena_original = info['cadena']
        cadena_limpia = limpiar_secuencia_crispr(cadena_original)
        print(f"{gen}: Original: {cadena_original} -> Limpia: {cadena_limpia}")
    
    app.run(debug=True)
