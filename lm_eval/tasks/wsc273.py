import json
import random
import os
from lm_eval.base import Dataset
from ..utils import sh


class WinogradSchemaChallenge273(Dataset):    
    def __init__(self):
        super().__init__()

    def download(self):
        if not os.path.exists('data/wsc273'):
            sh("""
                mkdir -p data/wsc273 
                wget https://git.cse.msu.edu/bakerb15/nlp-final-project/raw/master/Winogard/reproduce/commonsense_test/wsc273.json -O data/wsc273/wsc273.json
                """)

    def has_training_docs(self):
        return False

    def has_validation_docs(self):
        return False

    def has_test_docs(self):
        return True

    def training_docs(self):
        return []

    def validation_docs(self):
        return []

    def test_docs(self):
        myjson = json.load(open('data/wsc273/wsc273.json'))
        return self.load_doc(myjson)
    
    def fewshot_description(self):
        # TODO: redo description
        return "Winograd schema sentence with correct continuation. True. Winograd schema sentence with incorrect continuation. False."

    def load_doc(self, myjson):
        docs = []
        for i in range(0, 273 * 2, 2):
            item1 = myjson[i]
            item2 = myjson[i+1]

            if item1['question_id'] != item2['question_id']:
                raise ValueError("WSC273 has missing completion pair.")

            question_id = item1['question_id']

            if item1['correctness'] == True:
                doc = {
                    'id': question_id,
                    'completions': {
                        'T': item1['substitution'],
                        'F': item2['substitution'],
                    },
                }
                
            if item2['correctness'] == True:
                doc = {
                    'id': question_id,
                    'completions': {
                        'F': item1['substitution'],
                        'T': item2['substitution'],
                    },
                }

            docs.append(doc)
 
        return docs
    
    def doc_to_text(self, doc, include_target=True):
        # WSC273 is currently only writing out full examples. Partial evaluation needs implementing.
        text = doc['completions']['T'] + ' True. ' + doc['completions']['F'] + ' False.'
        return text


    def construct_requests(self, doc, ctx):
        """ Uses RequestFactory to construct Requests and returns an iterable of 
        Requests which will be sent to the LM.

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param ctx: str
            The context string, generated by fewshot_context. This includes the natural 
            language description, as well as the few shot examples, and the question
            part of the document for `doc`. 
        """
        # TODO: implement evaluation.
        raise NotImplementedError('Evaluation not implemented')
    
    def process_results(self, doc, results):
        """Take a single document and the LM results and evaluates, returning a 
        dict where keys are the names of submetrics and values are the values of 
        the metric for that one document

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param results:
            The results of the requests created in construct_requests.
        """
        # TODO: implement evaluation.
        raise NotImplementedError('Evaluation not implemented')

    def aggregation(self):
        """
        :returns: {str: [float] -> float}
            A dictionary where keys are the names of submetrics and values are 
            functions that aggregate a list of metrics
        """
        # TODO: implement evaluation.
        raise NotImplementedError('Evaluation not implemented')

    def higher_is_better(self):
        """
        :returns: {str: bool}
            A dictionary where keys are the names of submetrics and values are 
            whether a higher value of the submetric is better
        """
        # TODO: implement evaluation.
        raise NotImplementedError('Evaluation not implemented')
