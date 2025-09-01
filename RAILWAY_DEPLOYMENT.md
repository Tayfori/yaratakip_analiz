# 🚄 Railway Deployment Kılavuzu

## Neden Railway?
- ✅ Render'dan daha az kısıtlı
- ✅ Python packaging sorunları daha az
- ✅ GitHub integration kolay
- ✅ Free tier mevcut

## Deployment Adımları:

### 1. Railway.app'e Git
👉 https://railway.app

### 2. GitHub ile Giriş Yap
- "Login with GitHub" tıklayın
- GitHub hesabınızla oturum açın

### 3. New Project Oluştur
- "New Project" butonuna tıklayın
- "Deploy from GitHub repo" seçin
- `Tayfori/yaratakip_analiz` repository'yi seçin

### 4. Otomatik Deploy
- Railway otomatik olarak detect edecek:
  - `requirements.txt` bulacak
  - `Procfile` okuyacak
  - Python environment setup yapacak

### 5. Environment Variables (Opsiyonel)
PORT değişkeni otomatik set edilir.

### 6. Deploy Complete
- 3-5 dakikada tamamlanır
- URL verilir: `https://yaratakip-analiz-production.up.railway.app`

### 7. Domain Generate Et
- Settings > Networking > Generate Domain
- Public URL alın

## Avantajları:
- ✅ Daha az build hatası
- ✅ Python package management daha iyi
- ✅ Memory limiti daha yüksek
- ✅ Otomatik HTTPS
- ✅ GitHub sync

## Test URL'leri:
Deploy sonrası şu URL'ler çalışmalı:
- `/` → API info
- `/health` → Health check
- `/api/analyze-wound` → AI analysis
- `/docs` → API documentation

---
*Railway Render'dan daha stable olabilir bu tip minimal API'lar için*
