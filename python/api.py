from fastapi import FastAPI, HTTPException
import json
import os

app = FastAPI(title="Mercedes-Benz Sales API")

DATA_PATH = "data/processed/mercedes_sales_demo.json"
QUALITY_PATH = "data/processed/data_quality_report.json"
SUMMARY_PATH = "data/processed/etl_summary.json"

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/overview")
def get_overview():
    try:
        with open(DATA_PATH, 'r') as f:
            data = json.load(f)
        total_revenue = sum(item.get('sale_price_inr', 0) for item in data)
        return {
            "total_records": len(data),
            "total_revenue": total_revenue,
            "avg_price": total_revenue / len(data) if len(data) > 0 else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data-quality")
def get_quality():
    try:
        if not os.path.exists(QUALITY_PATH):
            return {"status": "Not Generated"}
        with open(QUALITY_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/pipeline/status")
def get_pipeline_status():
    try:
        if not os.path.exists(SUMMARY_PATH):
            return {"status": "Not Executed"}
        with open(SUMMARY_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
