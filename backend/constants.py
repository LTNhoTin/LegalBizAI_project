from configs.paths import relative_path


DEFAULT_EMBEDDING_MODEL = "BAAI/bge-m3"

PATHS = {
    "CHUNK": relative_path(r"LegalBizAI_project\backend\data\all_chunks_by_clauseWarticle.json"),
    "INDEXED_VECTOR_STORE": relative_path(r"LegalBizAI_project\backend\data\faiss_index"),
    "MODEL_EMBEDDING": relative_path(r"LegalBizAI_project\backend\models\embedding"),
    "PROMPT_TEMPLATE": relative_path(r"LegalBizAI_project\backend\prompt_template (1).txt"),
    "VISTRAL_7B_MODEL": relative_path(r"LegalBizAI_project\backend\models\VISTRAL_7B_MODEL"),
}
