from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None

    if request.method == 'POST':
        try:
            ley_cabeza = float(request.form['ley_cabeza'])
            ley_colas = float(request.form['ley_colas'])
            toneladas = float(request.form['toneladas'])
            variable_adicional = request.form['variable_adicional']
            valor_variable = float(request.form['valor_variable'])

            # Cálculos base
            metal_alimento = toneladas * ley_cabeza / 100
            metal_colas = toneladas * ley_colas / 100
            metal_recuperado = metal_alimento - metal_colas

            # Cálculo según variable seleccionada
            if variable_adicional == 'ley_concentrado':
                ley_concentrado = valor_variable
                toneladas_concentrado = metal_recuperado / (ley_concentrado / 100)
            elif variable_adicional == 'toneladas_concentrado':
                toneladas_concentrado = valor_variable
                ley_concentrado = metal_recuperado / toneladas_concentrado * 100
            else:
                toneladas_concentrado = 0
                ley_concentrado = 0

            # Resultados finales
            rendimiento = toneladas_concentrado / toneladas * 100
            recuperacion = metal_recuperado / metal_alimento * 100
            eficiencia = (rendimiento * recuperacion) / 100

            resultado = {
                'rendimiento': round(rendimiento, 2),
                'recuperacion': round(recuperacion, 2),
                'eficiencia': round(eficiencia, 2),
                'ley_concentrado': round(ley_concentrado, 2),
                'toneladas_concentrado': round(toneladas_concentrado, 2)
            }

        except ValueError:
            resultado = {'error': 'Por favor ingresa solo valores numéricos válidos.'}

    return render_template('index.html', resultado=resultado)
