import torch
from transformers import pipeline


class DescriptionModel:

    def __init__(self):

        self.pipe_summ = pipeline("summarization", model="sagard21/python-code-explainer", device=0)

        self._prompt_summ = ('summarize the python code below with a very detailed and extensive description of '
                            'the algorithm, input and output data in English text format '
                            'if if there is no code, output empty code')
        
        self.results = {}


    def get_description(self, file):    
        if file.endswith(".py") and "__init__" not in file:
            with open(file, 'r', encoding='utf-8') as file:
                code = file.read()
            with torch.no_grad():
                answer = self.pipe_summ(self._prompt_summ + code)[0]['summary_text']
            

            self.results[file.name] = answer

            torch.cuda.empty_cache()
    

def summarize_files(project_files):
    model = DescriptionModel()

    for file in project_files:
        model.get_description(file)

    return model.results
