# This file was auto-generated by Fern from our API Definition.

import typing
from .open_ai_vectorizer_text_embedding_3_small import OpenAiVectorizerTextEmbedding3Small
from .open_ai_vectorizer_text_embedding_3_large import OpenAiVectorizerTextEmbedding3Large
from .open_ai_vectorizer_text_embedding_ada_002 import OpenAiVectorizerTextEmbeddingAda002
from .basic_vectorizer_intfloat_multilingual_e_5_large import BasicVectorizerIntfloatMultilingualE5Large
from .basic_vectorizer_sentence_transformers_multi_qa_mpnet_base_cos_v_1 import (
    BasicVectorizerSentenceTransformersMultiQaMpnetBaseCosV1,
)
from .basic_vectorizer_sentence_transformers_multi_qa_mpnet_base_dot_v_1 import (
    BasicVectorizerSentenceTransformersMultiQaMpnetBaseDotV1,
)
from .hkunlp_instructor_xl_vectorizer import HkunlpInstructorXlVectorizer
from .google_vertex_ai_vectorizer_text_embedding_004 import GoogleVertexAiVectorizerTextEmbedding004
from .google_vertex_ai_vectorizer_text_multilingual_embedding_002 import (
    GoogleVertexAiVectorizerTextMultilingualEmbedding002,
)

IndexingConfigVectorizer = typing.Union[
    OpenAiVectorizerTextEmbedding3Small,
    OpenAiVectorizerTextEmbedding3Large,
    OpenAiVectorizerTextEmbeddingAda002,
    BasicVectorizerIntfloatMultilingualE5Large,
    BasicVectorizerSentenceTransformersMultiQaMpnetBaseCosV1,
    BasicVectorizerSentenceTransformersMultiQaMpnetBaseDotV1,
    HkunlpInstructorXlVectorizer,
    GoogleVertexAiVectorizerTextEmbedding004,
    GoogleVertexAiVectorizerTextMultilingualEmbedding002,
]