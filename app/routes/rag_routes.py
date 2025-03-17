from app.services import pdf_processor, rag_service
from fastapi import APIRouter, Query, UploadFile, File, Depends, HTTPException
from app.prompts.system_prompt import engaging_prompt
from app.gpt_response.generate_gpt_response import get_gpt_response_query
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decode_token
from app.models.user import User as UserModel
from app.models.resource import AppResource
from app.oso_rbac.oso_policy import oso

router = APIRouter(prefix="/rag", tags=["RAG"])

@router.post("/upload")
def upload_pdf(file: UploadFile = File(...), token: str = Depends(JWTBearer())):
    payload = decode_token(token)
    user_obj = UserModel(username=payload["sub"], role=payload["role"])
    
    if not oso.is_allowed(user_obj, "manage", AppResource("rag_upload")):
        raise HTTPException(status_code=403, detail="Only admins can upload PDFs")

    with open(f"temp_{file.filename}", "wb") as f:
        f.write(file.file.read())
    chunks = pdf_processor.process_pdf(f.name)
    rag_service.store_chunks(chunks)
    return {"message": "PDF processed and chunks stored"}

@router.get("/query")
def query_rag(question: str = Query(..., description="User query"), token: str = Depends(JWTBearer())):
    payload = decode_token(token)
    user_obj = UserModel(username=payload["sub"], role=payload["role"])

    if not oso.is_allowed(user_obj, "read", AppResource("rag_query")):
        raise HTTPException(status_code=403, detail="You are not allowed to query the documents")

    chunks = rag_service.retrieve_chunks(question)
    context = "\n".join(chunks)
    prompt_with_context = f"{engaging_prompt}\n\nContext:\n{context}"
    answer = get_gpt_response_query(query=question, prompt=prompt_with_context)
    return {"answer": answer}
