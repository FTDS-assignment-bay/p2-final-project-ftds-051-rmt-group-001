import streamlit as st
import json
import joblib
import pandas as pd
import os
import __main__
from dotenv import load_dotenv

load_dotenv()

MODEL_FILENAME = os.getenv("MODEL_FILENAME")
MODEL_PATH = "src/DS"

MODEL_FILE = f"{MODEL_PATH}/high_risk_predictor_1.pkl"
SCHEMA_FILE = f"{MODEL_PATH}/model_schema.json"

# ================================
# Load Model
# ================================
@st.cache_resource
def load_model():
    try:
        model = joblib.load(MODEL_FILE)
        return model

    except Exception as e:
        st.error(f"❌ Failed to load model. {e}")
        st.text(str(e))
        return None


# ================================
# Load Schema
# ================================

def load_schema():

    if not os.path.exists(SCHEMA_FILE):
        st.warning("⚠️ model_schema.json not found. Prediction UI cannot be generated.")
        return None

    try:
        with open(SCHEMA_FILE) as f:
            schema = json.load(f)

        return schema

    except json.JSONDecodeError:
        st.error("❌ model_schema.json is invalid JSON.")
        return None


# ================================
# Generate Inputs Dynamically
# ================================

def generate_inputs(schema):

    inputs = {}
    
    col1, col2 = st.columns(2)

    for i, feature in enumerate(schema["features"]):

        if feature.get("hidden"):
            continue

        container = col1 if i % 2 == 0 else col2
        
        with container:
            name = feature["name"]
            label = feature.get("label", name)
            ftype = feature["type"]

            # Integer
            if ftype == "int":

                min_val = feature.get("min")
                max_val = feature.get("max")

                default = feature.get("default")

                if default is None:
                    if min_val is not None:
                        default = min_val
                    else:
                        default = 0

                params = {
                    "label": label,
                    "value": int(default),
                    "step": int(feature.get("step", 1))
                }

                if min_val is not None:
                    params["min_value"] = int(min_val)

                if max_val is not None:
                    params["max_value"] = int(max_val)

                inputs[name] = st.number_input(**params)

            # Float
            elif ftype == "float":

                min_val = feature.get("min")
                max_val = feature.get("max")

                default = feature.get("default")

                if default is None:
                    if min_val is not None:
                        default = min_val
                    else:
                        default = 0.0

                params = {
                    "label": label,
                    "value": float(default),
                    "step": float(feature.get("step", 0.01))
                }

                if min_val is not None:
                    params["min_value"] = float(min_val)

                if max_val is not None:
                    params["max_value"] = float(max_val)

                inputs[name] = st.number_input(**params)

            # Categorical
            elif ftype == "categorical":

                options = feature["options"]
                default = feature.get("default", None)

                # Case 1: label/value format
                if isinstance(options[0], dict):

                    labels = [opt["label"] for opt in options]
                    values = [opt["value"] for opt in options]

                    label_to_value = {opt["label"]: opt["value"] for opt in options}

                    # default handling
                    if default and default in values:
                        default_index = values.index(default)
                    else:
                        default_index = 0

                    selected_label = st.selectbox(
                        label,
                        options=labels,
                        index=default_index
                    )

                    inputs[name] = label_to_value[selected_label]

                # Case 2: simple list
                else:

                    if default and default in options:
                        default_index = options.index(default)
                    else:
                        default_index = 0

                    inputs[name] = st.selectbox(
                        label,
                        options=options,
                        index=default_index
                    )

            # String
            elif ftype == "string":

                inputs[name] = st.text_input(
                    label,
                    placeholder=feature.get("placeholder", "")
                )

            # Boolean
            elif ftype == "boolean":

                inputs[name] = st.checkbox(
                    label,
                    value=feature.get("default", False)
                )

            # Datetime
            elif ftype == "datetime":
                
                datetime_value = st.datetime_input(
                    f"{label}",
                    value=None
                )

                # col1, col2 = st.columns(2)

                # with col1:
                #     date_value = st.date_input(
                #         f"{label} Date",
                #         value=None
                #     )

                # with col2:
                #     time_value = st.time_input(
                #         f"{label} Time",
                #         value=None
                #     )

                if datetime_value:
                    inputs[name] = datetime_value
                else:
                    inputs[name] = None

    return inputs


# ================================
# Prediction Page
# ================================

def prediction_page():

    st.title("Order Cancellation Prediction")

    schema = load_schema()
    model = load_model()
    
    if schema is None or model is None:

        st.info(
            f"""
                Prediction is currently unavailable.

                Required files:
                • model_schema.json  
                • {MODEL_FILENAME}
            """
        )

        return

    st.write(schema.get("description", ""))

    st.divider()

    inputs = generate_inputs(schema)
    
    # st.caption(
    #     "This tool predicts the probability that an order will be cancelled based on order, payment, and customer information."
    # )

    if st.button("Predict"):

        df = pd.DataFrame([inputs])
    
        # For DEBUG
        # st.write("Input Data")
        # st.dataframe(pd.DataFrame([inputs]))
        
        # If model need ordered features
        # if hasattr(model, "feature_names_in_"):
        #     df = df[model.feature_names_in_]

        try:
            # Check required fields
            missing_fields = [k for k, v in inputs.items() if v is None]

            if missing_fields:
                st.warning("⚠️ Please fill all required fields before prediction.")
                st.stop()
                
            prediction = model.predict(df)[0]
        except Exception as e:
            st.error(f"Prediction failed. {e}")
            st.text(str(e))
            return

        if hasattr(model, "predict_proba"):
            probability = model.predict_proba(df)[0][1]
        else:
            probability = None
            
        threshold = 0.3579
        st.subheader("Prediction Result")

        st.metric("Cancellation Risk Score", f"{probability:.2%}")
        st.caption(f"Decision Threshold: {threshold:.2%}")

        st.progress(probability)

        if probability >= threshold:
            st.error("⚠️ High risk of order cancellation")
            st.info(
                f"The predicted risk ({probability:.2%}) exceeds the decision threshold ({threshold:.2%}). "
                "This order may require additional verification or restrictions."
            )
        else:
            st.success("✅ Order likely to be completed")
            st.info(
                f"The predicted risk ({probability:.2%}) is below the decision threshold ({threshold:.2%}). "
                "This order is considered low risk."
            )
            
if __name__ == '__main__':
    prediction_page()