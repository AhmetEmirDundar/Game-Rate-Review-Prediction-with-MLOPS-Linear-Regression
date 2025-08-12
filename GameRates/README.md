# 🎮 Game Rating Predictor

Bu uygulama, oyun özelliklerini analiz ederek tahmini bir puan veren bir web uygulamasıdır.

## 🚀 Kurulum

### Gereksinimler
- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)

### Adımlar

1. **Sanal ortam oluşturun (önerilen):**
   ```bash
   python -m venv .venv
   ```

2. **Sanal ortamı aktifleştirin:**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

3. **Gerekli paketleri yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Çalıştırma

### Yöntem 1: Python script ile
```bash
python app.py
```

### Yöntem 2: Flask ile doğrudan
```bash
flask run --host=0.0.0.0 --port=8000
```

## 🌐 Kullanım

1. Tarayıcınızda `http://localhost:8000` adresine gidin
2. Oyun özelliklerini doldurun:
   - Hedef yaş grubu
   - Fiyat
   - Platform
   - Özel cihaz gereksinimi
   - Tür
   - Çok oyunculu özelliği
   - Oyun süresi
   - Grafik kalitesi
   - Müzik kalitesi
   - Hikaye kalitesi
   - Oyun modu
   - Minimum oyuncu sayısı
3. "Tahmin Et" butonuna tıklayın
4. Sonucu görüntüleyin

## 📁 Dosya Yapısı

```
GameRates3/
├── app.py                 # Ana Flask uygulaması
├── requirements.txt       # Python bağımlılıkları
├── game_rating_model.pkl  # Eğitilmiş model
├── templates/
│   └── index.html        # Web arayüzü
├── static/               # Statik dosyalar
└── README.md            # Bu dosya
```

## 🔧 Teknik Detaylar

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **ML Model**: Scikit-learn
- **Template Engine**: Jinja2

## 🐛 Sorun Giderme

### Model yüklenemiyor
- `game_rating_model.pkl` dosyasının mevcut olduğundan emin olun
- Model dosyasının bozuk olmadığını kontrol edin

### Paket yükleme hataları
- Python sürümünüzün 3.8+ olduğundan emin olun
- Sanal ortamın aktif olduğunu kontrol edin

### Port hatası
- 8000 portunun başka bir uygulama tarafından kullanılmadığından emin olun
- Farklı bir port kullanmak için `--port 8080` parametresini ekleyin

## 📝 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.
