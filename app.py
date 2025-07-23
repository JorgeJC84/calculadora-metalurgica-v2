from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    if request.method == 'POST':
        try:
            # Entrada principal del formulario
            ley_cabeza = float(request.form['ley_cabeza'])
            ley_colas = float(request.form['ley_colas'])
            toneladas = float(request.form['toneladas'])

            # Entrada extra para balance completo
            tipo_variable = request.form.get('tipo_variable')
            valor_variable = float(request.form['valor_variable'])

            # Cálculo inicial de metal en cabeza, colas y recuperado
            metal_cabeza = toneladas * ley_cabeza / 100
            metal_colas = toneladas * ley_colas / 100
            metal_recuperado = metal_cabeza - metal_colas
            recuperacion = (metal_recuperado / metal_cabeza) * 100 if metal_cabeza > 0 else 0

            # Variables que vamos a calcular según lo que ingrese el usuario
            masa_conc = masa_rels = ley_conc = None

            if tipo_variable == 'ley_conc':
                ley_conc = valor_variable
                masa_conc = metal_recuperado / (ley_conc / 100)
                masa_rels = toneladas - masa_conc

            elif tipo_variable == 'masa_conc':
                masa_conc = valor_variable
                ley_conc = (metal_recuperado / masa_conc) * 100
                masa_rels = toneladas - masa_conc

            elif tipo_variable == 'masa_rels':
                masa_rels = valor_variable
                masa_conc = toneladas - masa_rels
                ley_conc = (metal_recuperado / masa_conc) * 100

            # Preparar los resultados redondeados
            resultado = {
                'metal_cabeza': round(metal_cabeza, 2),
                'metal_colas': round(metal_colas, 2),
                'metal_recuperado': round(metal_recuperado, 2),
                'recuperacion': round(recuperacion, 2),
                'masa_conc': round(masa_conc, 2),
                'masa_rels': round(masa_rels, 2),
                'ley_conc': round(ley_conc, 2)
            }

        except Exception as e:
            resultado = {'error': f'Ocurrió un error al procesar los datos: {str(e)}'}

    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
