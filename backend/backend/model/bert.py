import os

from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import AnswerParser, BM25Retriever,  PromptNode, PromptTemplate
from haystack.pipelines import Pipeline, TextIndexingPipeline




class Bert:

    def __init__(self, data_path):
        print("Initializing model...")
        doc_dir = data_path
        document_store = InMemoryDocumentStore(use_bm25=True)

        files_to_index = [os.path.join(doc_dir, f) for f in os.listdir(doc_dir)]
        indexing_pipeline = TextIndexingPipeline(document_store)
        indexing_pipeline.run_batch(file_paths=files_to_index)

        print("Done indexing")

        retriever = BM25Retriever(document_store=document_store, top_k=1)

        lfqa_prompt = PromptTemplate(
            prompt=
"""
Synthesize a comprehensive answer from the following most relevant paragraphs and the given question.
Provide a clear response that summarizes the key points and any relevant information presented in the paragraphs.
\n\nQuestion: {query}\n\nParagraphs: {join(documents)}\n\nAnswer:
""",
        )



        lfqa_node = PromptNode(model_name_or_path="google/flan-t5-large", default_prompt_template=lfqa_prompt)
        self.pipe = Pipeline()
        self.pipe.add_node(component=retriever, name="retriever", inputs=["Query"])
        self.pipe.add_node(component=lfqa_node, name="lfqa_node", inputs=["retriever"])

        elaboration_prompt = PromptTemplate(
            prompt=
"""
Synthesize a single supporting sentence that provides additional details about the statement from the following most relevant paragraphs.
\n\nStatement: {query}\n\nParagraphs: {join(documents)}\n\nAnswer:
"""
        )

        elaboration_node = PromptNode(
            model_name_or_path="google/flan-t5-large",
            default_prompt_template=elaboration_prompt,
        )

        self.elaboration_pipeline = Pipeline()
        self.elaboration_pipeline.add_node(component=retriever, name="retriever", inputs=["Query"])
        self.elaboration_pipeline.add_node(component=elaboration_node, name="elaboration", inputs=["retriever"])

        summarization_prompt = PromptTemplate(
            prompt=
"""
Summarize the following paragraph into a more clear and concise answer while maintaining all of the key information.
\n\nParagraph: {query}\n\nAnswer:
"""
        )

        summarization_node = PromptNode(
            model_name_or_path="google/flan-t5-large",
            default_prompt_template=summarization_prompt,
        )

        self.summarization_pipeline = Pipeline()
        self.summarization_pipeline.add_node(component=retriever, name="retriever", inputs=["Query"])
        self.summarization_pipeline.add_node(component=summarization_node, name="summarization", inputs=["retriever"])

        paraphrasing_prompt = PromptTemplate(
            prompt=
"""
Paraphrase the following statement in your own words while keeping the same length and retaining all key information.
\n\nStatement: {query}\n\nAnswer:
"""
        )

        paraphrasing_node = PromptNode(
            model_name_or_path="google/flan-t5-large",
            default_prompt_template=paraphrasing_prompt,
        )

        self.paraphrasing_pipeline = Pipeline()
        self.paraphrasing_pipeline.add_node(component=retriever, name="retriever", inputs=["Query"])
        self.paraphrasing_pipeline.add_node(component=paraphrasing_node, name="paraphrasing", inputs=["retriever"])





    def generate(self, query):
        print(f"Answering question: [{query}]...")
        lfqa = self.pipe.run(query=query)

        answer = lfqa['results'][0]



        if len(answer) < 100:
            print(f"Elaborating on: [{answer}]...")
            elaboration = self.elaboration_pipeline.run(query=answer)
            answer = elaboration['results'][0]


        return answer

