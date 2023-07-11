import os

from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import AnswerParser, BM25Retriever, BaseComponent, PromptNode, PromptTemplate, Shaper
from haystack.schema import Answer, Document, List
from haystack.pipelines import Pipeline, TextIndexingPipeline




class Bert:
    pipe = None

    def __init__(self, data_path):
        print("Initializing model...")
        doc_dir = data_path
        document_store = InMemoryDocumentStore(use_bm25=True)

        files_to_index = [os.path.join(doc_dir, f) for f in os.listdir(doc_dir)]
        indexing_pipeline = TextIndexingPipeline(document_store)
        indexing_pipeline.run_batch(file_paths=files_to_index)

        print("Done indexing")

        retriever = BM25Retriever(document_store=document_store, top_k=2)

        lfqa_prompt = PromptTemplate(
            prompt="Synthesize a comprehensive answer from the following text for the given question."
                   "Provide any additional information that may be relevant in your own words."
                   "\n\n Related text: {join(documents)} \n\n Question: {query} \n\n Answer:",
            output_parser=AnswerParser(),
        )

        lfqa_node = PromptNode(model_name_or_path="google/flan-t5-large", default_prompt_template=lfqa_prompt)
        self.pipe = Pipeline()
        self.pipe.add_node(component=retriever, name="retriever", inputs=["Query"])
        self.pipe.add_node(component=lfqa_node, name="lfqa_node", inputs=["retriever"])




    def generate(self, query):
        prediction = self.pipe.run(query=query)

        return prediction
