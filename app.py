from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

def calcular_eficiencia(ley_cabeza, ley_colas):
    return (ley_cabeza - ley_colas) / ley_cabeza * 100

def generar_flowsheet(valores):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('off')

    # Extrae valores
    t = valores['toneladas_tratadas']
    lc = valores['ley_cabeza']
    lco = valores['ley_colas']
    tc = valores.get('toneladas_concentrado')
    lc_conc = valores.get('ley_concentrado')
    tr = valores.get('toneladas_relaves')

    # Dibuja flowsheet
    ax.text(0.05, 0.5, f"Mineral\n{t} t\n{lc:.2f}%", bbox=dict(facecolor='lightgray'), ha='center')
    ax.arrow(0.15, 0.5, 0.2, 0, head_width=0.05, head_length=0.03, fc='blue', ec='blue')
    ax.text(0.4, 0.7, f"Concentrado\n{tc if tc else '?'} t\n{lc_conc if lc_conc else '?'}%", bbox=dict(facecolor='lightgreen'), ha='center')
    ax.arrow(0.35, 0.5, 0.1, 0.15, head_width=0.03, head_length=0.03, fc='green', ec='green')
    ax.text(0.4, 0.3, f"Relaves\n{tr if tr else '?'} t\n{lco:.2f}%", bbox=dict(facecolor='lightcoral'), ha='center')
    ax.arrow(0.35, 0.5, 0.1, -0.15, head_width=0.03, head_length=0.03, fc='red', ec='red')

    # Guarda
    plt.savefig('static/flowsheet.png', bbox_inches='tight')
    plt.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    imagen = None

    if request.method == 'POST':
        try:
            ley_cabeza = float(request.form['ley_cabeza'])
            ley_colas = float(request.form['ley_colas'])
            toneladas_tratadas = float(request.form['toneladas_tratadas'])

            # Variables adicionales
            tipo_var = request.form.get('tipo_variable')
            valor_var = float(request.form.get('valor_variable'))

            valores = {
                'ley_cabeza': ley_cabeza,
                'ley_colas': ley_colas,
                'toneladas_tratadas': toneladas_tratadas,
            }

            if tipo_var == 'masa_conc':
                valores['toneladas_concentrado'] = valor_var
            elif tipo_var == 'ley_conc':
                valores['ley_concentrado'] = valor_var
            elif tipo_var == 'masa_rels':
                valores['toneladas_relaves'] = valor_var

            resultado = calcular_eficiencia(ley_cabeza, ley_colas)
            generar_flowsheet(valores)
            imagen = 'static/flowsheet.png'

        except Exception as e:
            resultado = f"Error: {e}"

    return render_template('index.html', resultado=resultado, imagen=imagen)

if __name__ == '__main__':
    app.run(debug=True)
