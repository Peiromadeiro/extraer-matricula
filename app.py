from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

# HTML con diseño mejorado usando Bootstrap
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>Extractor de Matrículas</title>
</head>
<body class="bg-light">
    <div class="container py-5">
        <h1 class="text-center text-primary mb-4">Extractor de Matrículas</h1>
        <div class="card shadow">
            <div class="card-body">
                <form method="POST" class="mb-3">
                    <div class="mb-3">
                        <label for="urls" class="form-label">Introduce una o varias URLs (una por línea):</label>
                        <textarea id="urls" name="urls" class="form-control" rows="8" placeholder="Introduce las URLs aquí..."></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Extraer Matrículas</button>
                </form>
                {% if results %}
                    <div class="mt-4">
                        <h2 class="text-success">Matrículas extraídas:</h2>
                        <ul class="list-group">
                            {% for matricula in results %}
                                <li class="list-group-item">{{ matricula }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                {% endif %}
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# Ruta principal
@app.route("/", methods=["GET", "POST"])
def extract_matriculas():
    results = []
    if request.method == "POST":
        urls = request.form.get("urls", "").splitlines()  # Obtener las URLs del formulario
        pattern = r"/\d{8}/(\d{7,8})/"  # Expresión regular para encontrar matrículas
        for url in urls:
            matches = re.findall(pattern, url)  # Busca todas las coincidencias en cada URL
            if matches:
                results.extend(matches)  # Agrega las matrículas encontradas a los resultados
    return render_template_string(html_template, results=results)

# Configuración de ejecución
if __name__ == "__main__":
    # En Render, se utiliza el puerto definido por la variable de entorno PORT
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
