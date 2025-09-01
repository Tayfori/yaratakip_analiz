#!/usr/bin/env python3
"""
FastAPI Backend - Yara Analizi API Servisi
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import base64
import io
import uvicorn
from wound_analysis_model import analyze_wound_api, WoundAnalysisModel
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="🏥 HealTrack API",
    description="Ameliyat Sonrası Yara Takibi ve Analizi API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Prod'da specific domain'ler kullan
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance
model = WoundAnalysisModel()

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

@app.get("/", response_model=HealthCheckResponse)
async def health_check():
    """Sistem durumu kontrolü"""
    return HealthCheckResponse(
        status="healthy",
        message="HealTrack API çalışıyor",
        model_loaded=True
    )

@app.post("/api/analyze-wound", response_model=ImageAnalysisResponse)
async def analyze_wound_endpoint(request: ImageAnalysisRequest):
    """
    Yara görüntüsü analizi endpoint
    """
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
        result = analyze_wound_api(image_data)
        
        return JSONResponse(content={
            "success": True,
            "filename": file.filename,
            "analysis": result
        })
        
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
        "processing_time": "~2-5 saniye"
    }

@app.get("/api/metrics")
async def get_system_metrics():
    """Sistem metrikleri"""
    import psutil
    import platform
    
    return {
        "system": {
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "memory_total": f"{psutil.virtual_memory().total // (1024**3)} GB",
            "memory_available": f"{psutil.virtual_memory().available // (1024**3)} GB"
        },
        "api": {
            "status": "running",
            "model_loaded": True
        }
    }

if __name__ == "__main__":
    print("🚀 HealTrack API başlatılıyor...")
    print("📋 Swagger UI: http://localhost:8000/docs")
    print("🔗 API Base URL: http://localhost:8000")
    
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
