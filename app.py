from flask import Flask, render_template, request, url_for
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

def calcular_eficiencia(ley_cabeza, ley_colas):
    return round((ley_cabeza - ley_colas) / ley_cabeza * 100, 2)

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
        print("✅ Se activó el método POST")

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

            resultado = {
                'recuperacion': calcular_eficiencia(ley_cabeza, ley_colas)
            }

            if ley_concentrado:
                ley_concentrado = float(ley_concentrado)
                valores['ley_concentrado'] = ley_concentrado
                resultado['ley_concentrado'] = ley_concentrado

            if toneladas_concentrado:
                toneladas_concentrado = float(toneladas_concentrado)
                valores['toneladas_concentrado'] = toneladas_concentrado
                resultado['toneladas_concentrado'] = toneladas_concentrado

            if toneladas_relaves:
                toneladas_relaves = float(toneladas_relaves)
                valores['toneladas_relaves'] = toneladas_relaves
                resultado['toneladas_relaves'] = toneladas_relaves

            # Cálculos adicionales si hay datos suficientes
            F = toneladas_tratadas
            f = ley_cabeza
            t = ley_colas
            C = valores.get('toneladas_concentrado')
            c = valores.get('ley_concentrado')
            T = valores.get('toneladas_relaves')

            if C and c:
                # Relación de concentración
                resultado['RC'] = round(c / f, 2) if f != 0 else None

                # Relación de enriquecimiento
                resultado['RE'] = round((c - t) / (f - t), 2) if (f - t) != 0 else None

                # Ley teórica del concentrado
                metal_feed = F * f / 100
                resultado['ley_teorica_conc'] = round((metal_feed / C) * 100, 2) if C != 0 else None

            if T:
                # Pérdida en colas
                resultado['perdida_colas'] = round(T * t / 100, 2)

            generar_flowsheet(valores)
            imagen = url_for('static', filename='flowsheet.png')

        except Exception as e:
            resultado = {'error': str(e)}
            print("❌ Error:", e)

    return render_template('index.html', resultado=resultado, imagen=imagen)

if __name__ == '__main__':
    app.run(debug=True)
