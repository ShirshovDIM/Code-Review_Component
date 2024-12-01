import torch
from transformers import pipeline
from application.models.context_model.summarization_model import summarize_files


class AdapterQAModel:

    def __init__(self):

        self.pipe_qa = pipeline("question-answering", model="google-bert/bert-large-uncased-whole-word-masking-finetuned-squad", device=0)

        self._context ="""
        Identifying an Adapter:
        Purpose: Adapters act as a bridge between incompatible interfaces or systems. Look for code that translates, formats, or mediates data between components.
        No Core Logic: Adapters typically do not implement business logic; they focus on communication or transformation.
        Input/Output Mapping: Watch for methods that primarily convert one data format to another (e.g., DTOs to domain objects).
        External Dependency Interaction: Adapters often wrap third-party APIs, databases, or external services.
        Layer-Specific: Adapters are commonly part of the infrastructure or application layers in layered architectures.
        Signals of Business Logic:
        Core Rules and Policies: The code applies domain-specific rules or validations.
        Decisions: Contains conditional logic or calculations specific to the domain (e.g., "if a user is premium, apply a 10% discount").
        Side Effects: Modifies domain state or triggers domain-specific events (e.g., updating order status).
        Reusability: Business logic is often reusable across various adapters or services.
        Key Distinction:
        If the snippet manipulates how data is moved or converted without applying domain-specific rules, it's likely an adapter. If it defines what should happen according to the domain's requirements, it's business logic.
        """

        self._question = 'is there any sign of adapter pattern matching?'
        
        self.results = {}

        self._map_dict = {
            "it's likely an adapter": 1,
            "without applying domain-specific rules": 0, 
            "no core logic": -1
        }

    
    def _mapper(self, answer):
        try: 
            answer = sum([self._map_dict[ans.strip()] for ans in answer.lower().replace(".", "").split(",")])

        except KeyError:
            answer=0

        return answer


    def get_answer(self, file, answer):    
        with torch.no_grad():
            final = self.pipe_qa(question = self._question  + answer,
                                    context=self._context)
        
        
        self.results[file] = self._mapper(final["answer"])

        print(self.results)

        torch.cuda.empty_cache()
    

def adapter_qa_checks(project_files):
    summaries = summarize_files(project_files)
    model = AdapterQAModel()

    adapter_qa_report = {}

    for file, answer in summaries.items():
        model.get_answer(file, answer)


    for file, answer in model.results.items():
        if "adapters" in file and answer != 1:
            adapter_qa_report[file] = "Нарушение взаимодействия компонент в гексагональной архитектуре"

    return adapter_qa_report
