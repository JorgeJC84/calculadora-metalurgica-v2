from flask import Flask, render_template, request, url_for
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

def generar_flowsheet(valores):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('off')

    t = valores['toneladas_tratadas']
    lc = valores['ley_cabeza']
    lco = valores['ley_colas']
    tc = valores.get('toneladas_concentrado')
    lc_conc = valores.get('ley_concentrado')
    tr = valores.get('toneladas_relaves')

    ax.text(0.05, 0.5, f"Mineral\n{t} t\n{lc:.2f}%", bbox=dict(facecolor='lightgray'), ha='center')
    ax.arrow(0.15, 0.5, 0.2, 0, head_width=0.05, head_length=0.03, fc='blue', ec='blue')
    ax.text(0.4, 0.7, f"Concentrado\n{tc if tc else '?'} t\n{lc_conc if lc_conc else '?'}%", bbox=dict(facecolor='lightgreen'), ha='center')
    ax.arrow(0.35, 0.5, 0.1, 0.15, head_width=0.03, head_length=0.03, fc='green', ec='green')
    ax.text(0.4, 0.3, f"Relaves\n{tr if tr else '?'} t\n{lco:.2f}%", bbox=dict(facecolor='lightcoral'), ha='center')
    ax.arrow(0.35, 0.5, 0.1, -0.15, head_width=0.03, head_length=0.03, fc='red', ec='red')

    ruta = os.path.join('static', 'flowsheet.png')
    plt.savefig(ruta, bbox_inches='tight')
    print("✅ Flowsheet generado y guardado en:", ruta)
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

            # Leer múltiples variables opcionales
            ley_concentrado = request.form.get('ley_concentrado')
            toneladas_concentrado = request.form.get('toneladas_concentrado')
            toneladas_relaves = request.form.get('toneladas_relaves')

            valores = {
                'ley_cabeza': ley_cabeza,
                'ley_colas': ley_colas,
                'toneladas_tratadas': toneladas_tratadas,
            }

            resultado = {}

            # Variables base
            F = toneladas_tratadas
            f = ley_cabeza
            t = ley_colas

            # Agregar variables opcionales
            if ley_concentrado:
                c = float(ley_concentrado)
                valores['ley_concentrado'] = c
                resultado['ley_concentrado'] = c
            else:
                c = None

            if toneladas_concentrado:
                C = float(toneladas_concentrado)
                valores['toneladas_concentrado'] = C
                resultado['toneladas_concentrado'] = C
            else:
                C = None

            if toneladas_relaves:
                T = float(toneladas_relaves)
                valores['toneladas_relaves'] = T
                resultado['toneladas_relaves'] = T
            else:
                T = None

            # Cálculo de recuperación real
            if C and c:
                metal_conc = C * c / 100
                metal_feed = F * f / 100
                recuperacion = (metal_conc / metal_feed) * 100 if metal_feed != 0 else 0
                resultado['recuperacion'] = round(recuperacion, 2)
            else:
                # Cálculo por eficiencia base si falta información
                resultado['recuperacion'] = round((f - t) / f * 100, 2) if f != 0 else 0

            # Relación de concentración
            if c and f:
                resultado['RC'] = round(c / f, 2)

            # Relación de enriquecimiento
            if c and f and t and (f - t) != 0:
                resultado['RE'] = round((c - t) / (f - t), 2)

            # Pérdida en colas
            if T:
                perdida_colas = T * t / 100
                resultado['perdida_colas'] = round(perdida_colas, 2)

            # Ley teórica del concentrado
            if C:
                metal_feed = F * f / 100
                ley_teorica = (metal_feed / C) * 100 if C != 0 else 0
                resultado['ley_teorica_conc'] = round(ley_teorica, 2)

            # Flowsheet
            generar_flowsheet(valores)
            imagen = url_for('static', filename='flowsheet.png')

        except Exception as e:
            resultado = {'error': str(e)}
            print("❌ Error:", e)

    return render_template('index.html', resultado=resultado, imagen=imagen)

if __name__ == '__main__':
    app.run(debug=True)
