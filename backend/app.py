import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# The model file sits next to app.py inside the container
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "superkart_sales_forecast_model_v0.joblib")
model = joblib.load(MODEL_PATH)

# The exact 10 columns the model was trained on
FEATURES = [
    "Product_Weight", "Product_Sugar_Content", "Product_Allocated_Area",
    "Product_MRP", "Store_Size", "Store_Location_City_Type", "Store_Type",
    "Store_Age_Years", "Product_Type_Category", "Product_Id_char",
]
NUMERIC = ["Product_Weight", "Product_Allocated_Area", "Product_MRP", "Store_Age_Years"]


def prepare(df):
    missing = [c for c in FEATURES if c not in df.columns]
    if missing:
        raise ValueError(f"Missing fields: {missing}")
    df = df[FEATURES].copy()
    for col in NUMERIC:
        df[col] = pd.to_numeric(df[col])
    return df


@app.get("/")
def home():
    return "Welcome to the SuperKart Sales Prediction API!"


@app.post("/v1/predict")
def predict_sales():
    try:
        data = request.get_json(force=True)
        df = prepare(pd.DataFrame([data]))
        pred = float(model.predict(df)[0])
        return jsonify({"Predicted_Sales": pred})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {e}"}), 500


@app.post("/v1/predictbatch")
def predict_sales_batch():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded (expected form field 'file')"}), 400
        df = prepare(pd.read_csv(request.files["file"]))
        preds = model.predict(df).tolist()
        return jsonify({str(i): p for i, p in enumerate(preds)})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Batch prediction failed: {e}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=True)
