import os

from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import BM25Retriever
from haystack.nodes import PromptNode, PromptTemplate, AnswerParser
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
            prompt="""Synthesize a comprehensive answer from the following text for the given question.
                                     Provide a clear and concise response that summarizes the key points and information presented in the text.
                                     Your answer should be in your own words and be no longer than 50 words.
                                     \n\n Related text: {join(documents)} \n\n Question: {query} \n\n Answer:""",
            output_parser=AnswerParser(),
        )

        prompt_node = PromptNode(model_name_or_path="google/flan-t5-large", default_prompt_template=lfqa_prompt)

        elaboration_prompt = PromptTemplate(
            prompt="""Elaborate on the answer to the following question given the related texts.
                                     Provide additional details to the answer in your own words.
                                     The final response should be between 100-200 words.
                                     \n\n Related text: {join(documents)} \n\n Question: {query} \n\n Answer: {prompt_node}""",
            output_parser=AnswerParser(),
        )
        elaboration_node = PromptNode(model_name_or_path="google/flan-t5-large", default_prompt_template=elaboration_prompt)

        self.pipe = Pipeline()
        self.pipe.add_node(component=retriever, name="retriever", inputs=["Query"])
        self.pipe.add_node(component=prompt_node, name="prompt_node", inputs=["retriever"])
        #self.pipe.add_node(component=elaboration_node, name="elaboration_node", inputs=["Query", "retriever", "prompt_node"])




    def generate(self, query):
        prediction = self.pipe.run(query=query)

        return prediction
