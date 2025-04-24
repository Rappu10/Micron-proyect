from flask import Flask, render_template
import pandas as pd

app = Flask(__name__, template_folder="../templates", static_folder="../static")

@app.route("/")
def home():
    tabla_sst0 = pd.read_csv("data/resultados_sst0.csv").to_html(index=False)
    tabla_actual = pd.read_csv("data/resultados_actual.csv").to_html(index=False)
    tabla_optimo = pd.read_csv("data/resultados_optimo.csv").to_html(index=False)

    return render_template("index.html", tabla_sst0=tabla_sst0, tabla_actual=tabla_actual, tabla_optimo=tabla_optimo)

if __name__ == "__main__":
    app.run(debug=True)
