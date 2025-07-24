from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Crear carpeta static si no existe
os.makedirs('static', exist_ok=True)

def calcular_eficiencia(ley_cabeza, ley_colas, toneladas_tratadas, variable, valor_variable):
    if variable == 'Ley de concentrado':
        ley_concentrado = valor_variable
        toneladas_concentrado = (ley_cabeza - ley_colas) / (ley_concentrado - ley_colas) * toneladas_tratadas
    else:  # variable == 'Toneladas de concentrado'
        toneladas_concentrado = valor_variable
        ley_concentrado = ((ley_cabeza - ley_colas) * toneladas_tratadas) / toneladas_concentrado + ley_colas

    recuperacion = (toneladas_concentrado * ley_concentrado) / (toneladas_tratadas * ley_cabeza) * 100
    return round(recuperacion, 2), round(toneladas_concentrado, 2), round(ley_concentrado, 2)

def generar_flowsheet(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')

    # Variables
    Lc = data['ley_cabeza']
    Lt = data['ley_colas']
    Lcn = data['ley_concentrado']
    Tt = data['toneladas_tratadas']
    Tc = data['toneladas_concentrado']

    # Dibujo
    ax.text(0.1, 0.8, f'Toneladas Tratadas:\n{Tt} t\nLey Cabeza: {Lc}%', bbox=dict(boxstyle="round", facecolor="lightblue"), ha='center')
    ax.arrow(0.3, 0.8, 0.15, 0, head_width=0.02, head_length=0.02, fc='black', ec='black')

    ax.text(0.55, 0.9, f'Concentrado\n{Tc} t\nLey: {Lcn}%', bbox=dict(boxstyle="round", facecolor="lightgreen"), ha='center')
    ax.arrow(0.45, 0.8, 0.1, 0.07, head_width=0.02, head_length=0.02, fc='black', ec='black')

    ax.text(0.55, 0.7, f'Colas\n{round(Tt - Tc, 2)} t\nLey: {Lt}%', bbox=dict(boxstyle="round", facecolor="salmon"), ha='center')
    ax.arrow(0.45, 0.8, 0.1, -0.07, head_width=0.02, head_length=0.02, fc='black', ec='black')

    ax.set_title('Flujograma del Balance Metalúrgico', fontsize=16)

    plt.savefig('static/flowsheet.png')
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
            variable = request.form['variable']
            valor_variable = float(request.form['valor_variable'])

            recuperacion, toneladas_concentrado, ley_concentrado = calcular_eficiencia(
                ley_cabeza, ley_colas, toneladas_tratadas, variable, valor_variable
            )

            resultado = {
                'recuperacion': recuperacion,
                'toneladas_concentrado': toneladas_concentrado,
                'ley_concentrado': ley_concentrado
            }

            datos_flowsheet = {
                'ley_cabeza': ley_cabeza,
                'ley_colas': ley_colas,
                'ley_concentrado': ley_concentrado,
                'toneladas_tratadas': toneladas_tratadas,
                'toneladas_concentrado': toneladas_concentrado
            }

            generar_flowsheet(datos_flowsheet)
            imagen = 'static/flowsheet.png'

        except Exception as e:
            resultado = {'error': f'Error en los datos: {e}'}

    return render_template('index.html', resultado=resultado, imagen=imagen)

if __name__ == '__main__':
    app.run(debug=True)
