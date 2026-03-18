import pydantic

class RAGChunkAndSrc(pydantic.BaseModel):
    chunks: list[str]
    source_id: str | None = None

class RAGUpserResult(pydantic.BaseModel):
    ingested: int

class RAGSearchResult(pydantic.BaseModel):
    context : list[str]
    source : list[str]

class RAGQuerResult(pydantic.BaseModel):
    answer : str
    sources: list[str]
    num_contexts: int