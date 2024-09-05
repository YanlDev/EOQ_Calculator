from flask import Flask, request, render_template, jsonify
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Obtener los datos del formulario
    D = float(request.form['demand'])
    S = float(request.form['cost_order'])
    H = float(request.form['holding_cost'])

    # Calcular el EOQ
    EOQ = np.sqrt((2 * D * S) / H)
    
    # Datos para el gráfico
    orders = np.arange(100, 1500, 10)
    cost_pedido = (D / orders) * S
    cost_mantenimiento = (orders / 2) * H
    cost_total = cost_pedido + cost_mantenimiento

    # Generar el gráfico con Matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot(orders, cost_pedido, label="Costo de Pedido", linestyle="--")
    plt.plot(orders, cost_mantenimiento, label="Costo de Mantenimiento", linestyle="--")
    plt.plot(orders, cost_total, label="Costo Total", linewidth=2)
    plt.axvline(x=EOQ, color="black", linestyle=":", label=f"EOQ = {int(EOQ)}")
    plt.legend()

    # Convertir la gráfica a una imagen en base64 para enviarla al frontend
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    # Interpretación temporal sin GPT-4
    interpretation = f"El EOQ calculado es de {EOQ:.2f} unidades. Basado en una demanda de {D}, un costo por pedido de {S}, y un costo de mantenimiento de {H}."

    # Devolver los datos como JSON
    return jsonify({
        'eoq': EOQ,
        'plot_url': plot_url,
        'interpretation': interpretation
    })



if __name__ == '__main__':
    app.run(debug=True)
