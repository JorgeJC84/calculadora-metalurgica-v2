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

            metal_cabeza = toneladas * ley_cabeza / 100
            metal_colas = toneladas * ley_colas / 100
            metal_recuperado = metal_cabeza - metal_colas
            recuperacion = (metal_recuperado / metal_cabeza) * 100

            resultado = {
                'metal_cabeza': round(metal_cabeza, 2),
                'metal_colas': round(metal_colas, 2),
                'metal_recuperado': round(metal_recuperado, 2),
                'recuperacion': round(recuperacion, 2)
            }
        except:
            resultado = 'Error en los datos. Por favor, revisa tus entradas.'

    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
