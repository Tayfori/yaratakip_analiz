# 🚀 HealTrack AI - Deployment Paketi

Bu klasör, HealTrack AI sisteminizi web'e yüklemek için gereken tüm dosyaları içerir.

## 📦 İçerik

### 📱 Frontend (`frontend/`)
- `index.html` - Ana web sayfası (tek dosya, hemen kullanıma hazır)

### 🔧 Backend (`backend/`)
- `main.py` - FastAPI server (production ready)
- `wound_analysis_model.py` - AI analiz modeli
- `requirements.txt` - Python bağımlılıkları
- `Procfile` - Heroku deployment config
- `runtime.txt` - Python version
- `.env.example` - Environment variables template

## ⚡ Hızlı Deployment (5 Dakika)

### 1. Frontend Yükleme
**Netlify (Ücretsiz):**
1. `frontend/index.html` dosyasını netlify.com'da drag-drop
2. Otomatik URL alın: `https://random-name.netlify.app`

**Alternatif:** Herhangi bir web hosting'e `index.html` yükle

### 2. Backend Yükleme  
**Heroku (Ücretsiz):**
1. Heroku hesabı oluştur
2. `backend/` klasörünü Git repository'si yap
3. Heroku'ya push et
4. URL'nizi alın: `https://your-app.herokuapp.com`

### 3. Bağlantı Kurma
`index.html` dosyasında şu satırı bulun:
```javascript
const API_BASE_URL = 'https://your-api-domain.com';
```

Heroku URL'nizi yazın:
```javascript
const API_BASE_URL = 'https://your-app.herokuapp.com';
```

## 🎯 Test Etme
1. Frontend URL'sini açın
2. Fotoğraf yükleyin
3. "Analizi Başlat" butonuna tıklayın
4. AI sonuçlarını görün!

## 💰 Maliyet
- **Ücretsiz Plan**: $0 (Netlify + Heroku)
- **Professional**: ~$25/ay (Domain + Premium hosting)

## 📞 Destek
Deployment sorunları için `README.md` dosyasına bakın.

---
**✅ Sistem Hazır! Web'e çıkın ve AI destekli yara analizinizi dünyayla paylaşın!** 🏥✨
