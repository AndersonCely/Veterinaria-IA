import pandas as pd
import joblib
import nltk

from nltk.corpus import stopwords

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Descargar stopwords
nltk.download('stopwords')

# Stopwords en español
stop_words = stopwords.words('spanish')

for palabra in ["no", "sin", "ni"]:
    if palabra in stop_words:
        stop_words.remove(palabra)

# Cargar dataset
df = pd.read_csv("dataset.csv")

X = df["sintomas"]
y = df["diagnostico"]

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Pipeline NLP mejorado
pipeline = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            stop_words=stop_words,
            ngram_range=(1,3), 
            max_features=5000
        )
    ),
    (
        "model",
        LogisticRegression(
            max_iter=1000,
            class_weight='balanced'
        )
    )
])

# Entrenar
pipeline.fit(X_train, y_train)

# Evaluar
y_pred = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='macro')
recall = recall_score(y_test, y_pred, average='macro')

print("Accuracy:", round(accuracy, 2))
print("Precision:", round(precision, 2))
print("Recall:", round(recall, 2))

# Guardar modelo
joblib.dump(pipeline, "modelo.pkl")

# Guardar métricas
metricas = {
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall
}

joblib.dump(metricas, "metricas.pkl")

print("Modelo entrenado correctamente ✅")