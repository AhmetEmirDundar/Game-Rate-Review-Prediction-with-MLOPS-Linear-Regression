from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import os
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

model_path = "game_rating_model.pkl"

# Global variables for model components
model = None
preprocessor = None
scaler = None
feature_names = []

def load_model():
    """Load the trained model and related components"""
    global model, preprocessor, scaler, feature_names
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model dosyası bulunamadı: {model_path}")
    
    try:
        with open(model_path, "rb") as f:
            saved_data = pickle.load(f)
            model = saved_data.get("model")
            preprocessor = saved_data.get("preprocessor")
            scaler = saved_data.get("scaler")
            
            if not all([model, preprocessor, scaler]):
                raise ValueError("Pickle dosyasında model, preprocessor veya scaler bulunamadı.")
            
            # Get feature names safely
            try:
                feature_names = preprocessor.get_feature_names_out()
            except AttributeError:
                # Fallback for older scikit-learn versions
                if hasattr(scaler, 'mean_'):
                    feature_names = [f"feature_{i}" for i in range(len(scaler.mean_))]
                else:
                    feature_names = [f"feature_{i}" for i in range(100)]  # Default fallback
                    
            logger.info("Model başarıyla yüklendi")
            
            # Debug: Print encoder categories
            try:
                for i, transformer in enumerate(preprocessor.transformers_):
                    if hasattr(transformer[1], 'categories_'):
                        logger.info(f"Transformer {i} ({transformer[0]}): {transformer[1].categories_}")
            except Exception as e:
                logger.warning(f"Encoder kategorileri yazdırılamadı: {e}")
            
    except Exception as e:
        logger.error(f"Model yükleme hatası: {str(e)}")
        raise

# Load model on startup
try:
    load_model()
except Exception as e:
    logger.error(f"Uygulama başlatılamadı: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if model is loaded
        if model is None or preprocessor is None or scaler is None:
            return render_template('index.html', error="Model yüklenemedi. Lütfen tekrar deneyin.")
        
        # Get form data with error handling
        try:
            input_dict = {
                "Age Group Targeted": request.form.get('Age_Group_Targeted'),
                "Price": float(request.form.get('Price', 0)),
                "Platform": request.form.get('Platform'),
                "Requires Special Device": request.form.get('Requires_Special_Device'),
                "Genre": request.form.get('Genre'),
                "Multiplayer": request.form.get('Multiplayer'),
                "Game Length (Hours)": float(request.form.get('Game_Length_Hours', 0)),
                "Graphics Quality": request.form.get('Graphics_Quality'),
                "Soundtrack Quality": request.form.get('Soundtrack_Quality'),
                "Story Quality": request.form.get('Story_Quality'),
                "Game Mode": request.form.get('Game_Mode'),
                "Min Number of Players": int(request.form.get('Min_Number_of_Players', 1)),
            }
        except (ValueError, TypeError) as e:
            return render_template('index.html', error=f"Form verilerinde hata: {str(e)}")

        # Check if all required fields are present
        required_fields = ['Age_Group_Targeted', 'Platform', 'Requires_Special_Device', 'Genre', 
                         'Multiplayer', 'Graphics_Quality', 'Soundtrack_Quality', 'Story_Quality', 'Game_Mode']
        
        missing_fields = [field for field in required_fields if not request.form.get(field)]
        if missing_fields:
            return render_template('index.html', error=f"Eksik alanlar: {', '.join(missing_fields)}")

        input_df = pd.DataFrame([input_dict])
        logger.info(f"Input data: {input_dict}")

        # Apply preprocessing
        transformed = preprocessor.transform(input_df)
        scaled = scaler.transform(transformed)

        # Create final dataframe with correct feature names
        if len(feature_names) == scaled.shape[1]:
            final_df = pd.DataFrame(scaled, columns=feature_names)
        else:
            # Fallback if feature names don't match
            final_df = pd.DataFrame(scaled)

        prediction = model.predict(final_df)[0]
        prediction = max(0, min(10, prediction))

        # Determine rating message
        if prediction >= 8:
            message = "Mükemmel bir oyun! Kesinlikle oynamaya değer."
        elif prediction >= 6:
            message = "İyi bir oyun. Oynamaya değer."
        elif prediction >= 4:
            message = "Orta seviyede bir oyun. Dikkatli olun."
        else:
            message = "Düşük puanlı oyun. Önerilmez."

        logger.info(f"Prediction successful: {prediction}")
        return render_template('index.html', result=round(prediction, 1), message=message)
        
    except Exception as e:
        logger.error(f"Tahmin hatası: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return render_template('index.html', error=f"Tahmin sırasında hata oluştu: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
