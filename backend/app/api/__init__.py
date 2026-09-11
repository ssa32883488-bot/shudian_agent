from app.api.admin_bank import router as admin_bank_router
from app.api.admin_classes import router as admin_classes_router
from app.api.admin_config import router as admin_config_router
from app.api.admin_learning import router as admin_learning_router
from app.api.admin_reflow import router as admin_reflow_router
from app.api.admin_traces import router as admin_traces_router
from app.api.auth import router as auth_router
from app.api.media import router as media_router
from app.api.memory import router as memory_router
from app.api.student import router as student_router
from app.api.student_mistakes import router as student_mistakes_router
from app.api.student_plan import router as student_plan_router
from app.api.student_practice import router as student_practice_router
from app.api.student_profile import router as student_profile_router
from app.api.student_threads import router as student_threads_router
from app.api.student_parse import router as student_parse_router
from app.api.student_kg import router as student_kg_router

from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(media_router)
api_router.include_router(memory_router)
api_router.include_router(student_router)
api_router.include_router(student_parse_router)
api_router.include_router(student_threads_router)
api_router.include_router(student_plan_router)
api_router.include_router(student_mistakes_router)
api_router.include_router(student_profile_router)
api_router.include_router(student_practice_router)
api_router.include_router(student_kg_router)
api_router.include_router(admin_bank_router)
api_router.include_router(admin_reflow_router)
api_router.include_router(admin_learning_router)
api_router.include_router(admin_classes_router)
api_router.include_router(admin_config_router)
api_router.include_router(admin_traces_router)
