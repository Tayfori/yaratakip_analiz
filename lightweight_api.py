"""
Lightweight API Server - Render Free Tier (512MB) için optimize edilmiş
Memory kullanımı: ~80-150MB
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from lightweight_model import analyze_wound_api
import os

# FastAPI app
app = FastAPI(
    title="Wound Analysis API - Lightweight",
    description="Memory-optimized wound analysis for free hosting",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageData(BaseModel):
    image: str

class AnalysisResponse(BaseModel):
    inflammation_score: float
    swelling_score: float
    closure_score: float
    overall_status: str
    recommendations: list
    confidence: float
    processed_regions: str

@app.get("/")
async def root():
    """API bilgileri"""
    return {
        "message": "Wound Analysis API - Lightweight Version",
        "status": "active",
        "version": "1.0.0",
        "memory_optimized": True,
        "endpoints": {
            "health": "/health",
            "analyze": "/api/analyze-wound"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "lightweight-1.0",
        "memory_optimized": True
    }

@app.post("/api/analyze-wound", response_model=AnalysisResponse)
async def analyze_wound(data: ImageData):
    """Yara analizi endpoint - memory optimized"""
    try:
        if not data.image:
            raise HTTPException(status_code=400, detail="Image data is required")
        
        # Lightweight analysis
        result = analyze_wound_api(data.image)
        
        return AnalysisResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}"
        )

@app.get("/api/status")
async def api_status():
    """API durumu"""
    import psutil
    import sys
    
    try:
        # Memory usage info
        process = psutil.Process(os.getpid())
        memory_mb = process.memory_info().rss / 1024 / 1024
        
        return {
            "status": "running",
            "memory_usage_mb": round(memory_mb, 2),
            "python_version": sys.version,
            "model": "lightweight",
            "render_compatible": memory_mb < 400
        }
    except:
        return {
            "status": "running",
            "memory_usage_mb": "unknown",
            "model": "lightweight"
        }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "lightweight_api:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload to save memory
        access_log=False  # Disable access logs to save memory
    )
