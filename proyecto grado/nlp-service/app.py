from flask import Flask, request, jsonify
import joblib
import re
import unicodedata

app = Flask(__name__)

# ==========================
# CARGAR MODELO Y MÉTRICAS
# ==========================

model = joblib.load("modelo.pkl")
metricas = joblib.load("metricas.pkl")
print("=== MÉTRICAS DEL MODELO ===")
print(metricas)


# ==========================
# RECOMENDACIONES
# ==========================

recomendaciones = {

    "infeccion gastrointestinal":
    "Mantener hidratación, dieta blanda y acudir al veterinario si los síntomas continúan.",

    "infeccion respiratoria":
    "Mantener al animal en reposo, evitar cambios bruscos de temperatura y acudir al veterinario.",

    "alergia":
    "Evitar alimentos o sustancias que puedan causar alergias y consultar al veterinario.",

    "lesion muscular":
    "Evitar actividad física intensa y permitir reposo mientras es evaluado por un veterinario.",

    "infeccion viral":
    "Mantener hidratación, aislamiento preventivo y seguimiento veterinario.",

    "gastritis":
    "Controlar la alimentación, evitar comidas irritantes y mantener hidratación.",

    "resfriado":
    "Mantener al animal en un ambiente cálido y observar evolución de los síntomas.",

    "dermatitis":
    "Mantener higiene adecuada de la piel y evitar agentes irritantes.",

    "bronquitis":
    "Evitar exposición al frío o humo y acudir al veterinario para evaluación.",

    "diabetes":
    "Realizar control veterinario y seguimiento de alimentación y niveles de glucosa.",

    "otitis":
    "Limpiar cuidadosamente los oídos y consultar tratamiento veterinario.",

    "parvovirus":
    "Acudir inmediatamente al veterinario y evitar contacto con otros animales.",

    "conjuntivitis":
    "Mantener limpieza ocular y evitar manipular los ojos del animal.",

    "artritis":
    "Reducir actividad física intensa y realizar control veterinario periódico.",

    "neumonia":
    "Buscar atención veterinaria inmediata y mantener reposo."
}

# ==========================
# LIMPIEZA DE TEXTO NLP
# ==========================

def limpiar_texto(texto):

    # minúsculas
    texto = texto.lower()

    # eliminar tildes
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

    # eliminar caracteres especiales
    texto = re.sub(r'[^a-zñ\s]', ' ', texto)

    # eliminar espacios repetidos
    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto

# ==========================
# API PRINCIPAL
# ==========================

@app.route("/analizar", methods=["POST"])
def analizar():

    try:

        data = request.json

        sintomas = data.get("sintomas", "")

        if not sintomas:

            return jsonify({
                "error": "No se enviaron síntomas"
            }), 400

        # ==========================
        # PREPROCESAMIENTO NLP
        # ==========================

        texto_limpio = limpiar_texto(sintomas)

        # ==========================
        # PREDICCIÓN
        # ==========================

        pred = model.predict([texto_limpio])[0]

        # ==========================
        # CONFIANZA
        # ==========================

        proba = max(
            model.predict_proba([texto_limpio])[0]
        ) * 100

        # ==========================
        # RECOMENDACIÓN
        # ==========================

        recomendacion = recomendaciones.get(
            pred.lower(),
            "Consultar con un veterinario."
        )

        # ==========================
        # RESPUESTA
        # ==========================

        return jsonify({

            "diagnostico": pred,

            "texto_original": sintomas,

            "texto_limpio": texto_limpio,

            "confianza": round(proba, 2),

            "accuracy": round(metricas["accuracy"], 2),

            "precision": round(metricas["precision"], 2),

            "recall": round(metricas["recall"], 2),

            "recomendacion": recomendacion

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(port=5000)