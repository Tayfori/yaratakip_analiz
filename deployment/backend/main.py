#!/usr/bin/env python3
"""
FastAPI Backend - Yara Analizi API Servisi
Production Ready Deployment Version
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import base64
import io
import uvicorn
import os
from wound_analysis_model import analyze_wound_api, WoundAnalysisModel
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="🏥 HealTrack AI API",
    description="Ameliyat Sonrası Yara Takibi ve Analizi API - Production Version",
    version="1.0.0",
    docs_url="/api/docs",  # Production'da docs URL'sini değiştir
    redoc_url="/api/redoc"
)

# CORS middleware - Production'da specific origins kullan
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da: ["https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Statik dosyalar (frontend için)
# app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# Global model instance
try:
    model = WoundAnalysisModel()
    logger.info("✅ AI Model başarıyla yüklendi")
except Exception as e:
    logger.error(f"❌ Model yükleme hatası: {e}")
    model = None

# Pydantic models
class ImageAnalysisRequest(BaseModel):
    image_data: str  # Base64 encoded image
    patient_id: Optional[str] = None
    notes: Optional[str] = None

class ImageAnalysisResponse(BaseModel):
    success: bool
    inflammation_score: float
    swelling_score: float
    closure_score: float
    overall_status: str
    recommendations: List[str]
    confidence: float
    processed_regions: dict
    timestamp: str

class HealthCheckResponse(BaseModel):
    status: str
    message: str
    model_loaded: bool
    version: str

@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint - Production için"""
    return {"message": "HealTrack AI API - v1.0.0", "docs": "/api/docs"}

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Sistem durumu kontrolü"""
    return HealthCheckResponse(
        status="healthy" if model else "model_error",
        message="HealTrack AI API çalışıyor" if model else "Model yüklenemedi",
        model_loaded=model is not None,
        version="1.0.0"
    )

@app.post("/api/analyze-wound", response_model=ImageAnalysisResponse)
async def analyze_wound_endpoint(request: ImageAnalysisRequest):
    """
    Yara görüntüsü analizi endpoint
    """
    if not model:
        raise HTTPException(
            status_code=503,
            detail="AI Model henüz yüklenmedi. Lütfen daha sonra tekrar deneyin."
        )
    
    try:
        logger.info(f"Yara analizi başlatıldı - Patient ID: {request.patient_id}")
        
        # Görüntü formatı kontrolü
        if not request.image_data.startswith('data:image/'):
            raise HTTPException(
                status_code=400, 
                detail="Geçersiz görüntü formatı. Base64 encoded image gerekli."
            )
        
        # Model analizi
        result = analyze_wound_api(request.image_data)
        
        # Timestamp ekle
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        
        logger.info(f"Analiz tamamlandı - Status: {result['overall_status']}")
        
        return ImageAnalysisResponse(
            success=True,
            inflammation_score=result["inflammation_score"],
            swelling_score=result["swelling_score"],
            closure_score=result["closure_score"],
            overall_status=result["overall_status"],
            recommendations=result["recommendations"],
            confidence=result["confidence"],
            processed_regions=result["processed_regions"],
            timestamp=timestamp
        )
        
    except Exception as e:
        logger.error(f"Analiz hatası: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analiz sırasında hata oluştu: {str(e)}"
        )

@app.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """
    Alternatif dosya upload endpoint
    """
    try:
        # Dosya tipi kontrolü
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="Sadece görüntü dosyaları kabul edilir"
            )
        
        # Dosya boyutu kontrolü (5MB limit)
        content = await file.read()
        if len(content) > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="Dosya boyutu 5MB'dan büyük olamaz"
            )
        
        # Base64'e çevir
        base64_data = base64.b64encode(content).decode('utf-8')
        image_data = f"data:{file.content_type};base64,{base64_data}"
        
        # Analiz et
        if model:
            result = analyze_wound_api(image_data)
            return JSONResponse(content={
                "success": True,
                "filename": file.filename,
                "analysis": result
            })
        else:
            raise HTTPException(
                status_code=503,
                detail="AI Model henüz hazır değil"
            )
        
    except Exception as e:
        logger.error(f"Upload hatası: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Upload sırasında hata oluştu: {str(e)}"
        )

@app.get("/api/model-info")
async def get_model_info():
    """Model bilgileri"""
    return {
        "model_name": "WoundAnalysisModel v1.0",
        "capabilities": [
            "Kızarıklık tespiti",
            "Şişlik analizi", 
            "Kapanma durumu değerlendirmesi"
        ],
        "supported_formats": ["JPG", "PNG", "JPEG"],
        "max_file_size": "5MB",
        "processing_time": "~2-5 saniye",
        "model_loaded": model is not None
    }

@app.get("/api/metrics")
async def get_system_metrics():
    """Sistem metrikleri"""
    try:
        import psutil
        import platform
        
        return {
            "system": {
                "platform": platform.system(),
                "python_version": platform.python_version(),
                "cpu_count": psutil.cpu_count(),
                "memory_total": f"{psutil.virtual_memory().total // (1024**3)} GB",
                "memory_available": f"{psutil.virtual_memory().available // (1024**3)} GB",
                "cpu_percent": psutil.cpu_percent()
            },
            "api": {
                "status": "running",
                "model_loaded": model is not None
            }
        }
    except ImportError:
        return {
            "system": {
                "platform": "unknown",
                "python_version": "unknown"
            },
            "api": {
                "status": "running",
                "model_loaded": model is not None
            }
        }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint bulunamadı", "docs": "/api/docs"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "İç sunucu hatası", "message": str(exc)}
    )

if __name__ == "__main__":
    print("🚀 HealTrack AI API başlatılıyor...")
    print("📋 API Docs: http://localhost:8000/api/docs")
    print("🔗 Health Check: http://localhost:8000/health")
    print("🌐 Frontend: Frontend dosyalarını ayrı host edin")
    
    # Production ayarları
    uvicorn.run(
        "main:app",  # Production'da dosya adı main.py olacak
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=False,  # Production'da False
        log_level="info",
        workers=1  # CPU sayısına göre artırın
    )
