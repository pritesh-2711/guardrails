from fastapi import FastAPI, HTTPException
from models import InputModerationRequest, OutputModerationRequest, ModerationResponse
from moderator import Moderator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Content Moderation API", version="1.0.0")

moderator = Moderator()

@app.get("/")
def root():
    return {
        "message": "Content Moderation API",
        "endpoints": {
            "input_moderation": "/moderate/input",
            "output_moderation": "/moderate/output"
        }
    }

@app.post("/moderate/input", response_model=ModerationResponse)
async def moderate_input(request: InputModerationRequest):
    try:
        logger.info(f"Moderating input: {request.user_input[:50]}...")
        result = moderator.moderate_input(request.user_input)
        return ModerationResponse(**result)
    except Exception as e:
        logger.error(f"Error moderating input: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/moderate/output", response_model=ModerationResponse)
async def moderate_output(request: OutputModerationRequest):
    try:
        logger.info(f"Moderating output: {request.ai_response[:50]}...")
        result = moderator.moderate_output(request.ai_response)
        return ModerationResponse(**result)
    except Exception as e:
        logger.error(f"Error moderating output: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
