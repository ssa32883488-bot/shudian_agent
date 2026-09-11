"""应用配置：全部从环境变量读取，禁止硬编码密钥。"""

from functools import lru_cache
from pathlib import Path
from typing import Literal, Self

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BACKEND_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "数电教育智能体"
    debug: bool = True
    log_level: str = "INFO"

    # PostgreSQL（正式）；本地无库时可临时 sqlite:///./data/shudian_agent.db
    database_url: str = (
        "postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/shudian_agent"
    )

    # ChromaDB
    chroma_persist_dir: str = str(BACKEND_ROOT / "data" / "chroma")
    chroma_collection_questions: str = "question_bank"

    # LLM（OpenAI 兼容；对外环境变量优先 DEEPSEEK_KEY，仍兼容旧名 MIMO_API_KEY）
    mimo_api_base: str = "https://api.deepseek.com/v1"
    deepseek_key: str = ""
    mimo_api_key: str = ""  # 兼容旧环境变量；与 deepseek_key 合并
    mimo_model: str = "deepseek-v4-flash-vision-exp"
    mimo_ocr_model: str = "deepseek-v4-flash-vision-exp"
    mimo_mock: bool = True

    # BGE（默认轻量；大内存可换 bge-m3 并把 bge_rerank_via_embed=False）
    bge_embedding_model: str = "BAAI/bge-small-zh-v1.5"
    bge_reranker_model: str = "BAAI/bge-small-zh-v1.5"
    bge_use_real_model: bool = True
    bge_rerank_via_embed: bool = True  # True=用向量余弦精排，省 CrossEncoder 内存
    bge_device: str = "cpu"

    # Neo4j（默认关；本机 Docker 易占内存。开启前请先起 neo4j 并 sync）
    neo4j_enabled: bool = False
    neo4j_uri: str = "bolt://127.0.0.1:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "shudian123"

    # 业务阈值
    # 题库原题：向量分 ≥ 此值才进入同题校验；通过则权威直出
    hit_score_threshold: float = 0.95
    # 智能体判定「与用户题同一道」的最低分
    match_accept_threshold: float = 0.75
    # 教材 RAG /「教材相关图」展示：向量+精排综合分须 ≥ 该值才返回
    textbook_rag_score_threshold: float = 0.95
    reflow_mode: Literal["manual", "auto"] = "manual"
    # 自主解题后的权威评审（是否可回流题库）
    authority_validate_threshold: float = 0.7
    # 决策者：是否用 LLM 细化规划（mock 或 false 时走启发式）
    decision_maker_use_llm: bool = True
    # 意图识别与智能路由：是否用 LLM 拆题/拦截（mock 或 false 时走启发式）
    intent_router_use_llm: bool = True

    # 逻辑图门符号：iec=国标矩形轮廓（GB/T 4728.12 / IEC 60617：&、≥1、1）；ansi=特定外形
    logic_gate_style: Literal["ansi", "iec"] = "iec"

    # 认证（无短信）；生产须 auth_disabled=false
    auth_salt: str = "shudian-agent-p1-dev-salt"
    # false=强制 Bearer Token；true 时可用 X-Dev-Persona 演示身份（仅本地调试）
    auth_disabled: bool = False
    demo_class_code: str = "DEMO01"

    # Redis：会话状态 / LangGraph checkpointer（不存聊天原文）
    redis_url: str = "redis://127.0.0.1:6379/0"

    # 记忆层参数（写死；管理端不可热改）
    memory_summary_every_n: int = 20
    memory_keep_recent_k: int = 60

    # Agent 防死循环断路器（ReAct / 直出）
    agent_max_iterations: int = 8
    # 含多次 LLM + 波形/网表出图重试，默认给满 3 分钟
    agent_wall_timeout_sec: float = 180.0
    agent_direct_wall_timeout_sec: float = 180.0
    # 仅约束「无事件空转」；工具执行中不计入 idle（见 tutor_react）
    agent_idle_timeout_sec: float = 90.0
    agent_max_output_chars: int = 4500
    agent_max_draw_calls: int = 3
    agent_max_retrieve_calls: int = 2
    agent_max_search_calls: int = 2
    agent_repeat_action_limit: int = 3
    # 整卷/多小题：只详解前 N 道并提示用户分题上传
    multi_question_answer_limit: int = 2
    multi_question_char_threshold: int = 1800

    # MinerU 文档解析（Word/PDF/PPT 等）
    mineru_token: str = ""
    mineru_mode: Literal["flash", "precision"] = "precision"
    mineru_timeout_sec: int = 600
    mineru_max_file_mb: int = 25

    # MinIO / 教材图片公网前缀
    # MEDIA_BASE_URL 供浏览器访问，部署到服务器时改为域名，例如 https://cdn.example.com/shudian-textbook
    minio_endpoint: str = "127.0.0.1:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "shudian-textbook"
    minio_secure: bool = False
    media_base_url: str = "http://127.0.0.1:9000/shudian-textbook"

    @model_validator(mode="after")
    def _coalesce_deepseek_key(self) -> Self:
        key = (self.deepseek_key or self.mimo_api_key or "").strip()
        self.deepseek_key = key
        self.mimo_api_key = key
        return self


def _resolve_under_backend(path: str) -> str:
    """相对路径一律落到 backend/，避免 cwd 不同导致 Chroma 写错目录。"""
    p = Path(path)
    if not p.is_absolute():
        p = BACKEND_ROOT / p
    return str(p.resolve())


@lru_cache
def get_settings() -> Settings:
    s = Settings()
    s.chroma_persist_dir = _resolve_under_backend(s.chroma_persist_dir)
    # sqlite 相对路径同理
    if s.database_url.startswith("sqlite:///./"):
        rel = s.database_url.replace("sqlite:///./", "", 1)
        s.database_url = f"sqlite:///{_resolve_under_backend(rel)}"
    return s
