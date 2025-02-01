from abc import ABC, abstractmethod
import os
from typing import List, Dict, Any
import openai
from dotenv import load_dotenv

load_dotenv()

class BaseAgent(ABC):
    def __init__(self, model_name: str = "gpt-4o"):
        self.model_name = model_name
        self.client = openai.OpenAI(
            api_key=os.environ["OPENAI_API_KEY"]
        )
        
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
    
    def _get_completion(self, messages: List[Dict[str, str]]) -> str:
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error getting completion: {e}")
            return ""

class LiteratureReviewAgent(BaseAgent):
    def execute(self, research_topic: str) -> Dict[str, Any]:
        """Conduct literature review on the given research topic."""
        messages = [
            {"role": "system", "content": "You are a research assistant conducting a literature review."},
            {"role": "user", "content": f"Please analyze the current state of research on: {research_topic}"}
        ]
        review = self._get_completion(messages)
        return {"topic": research_topic, "review": review}

class ExperimentationAgent(BaseAgent):
    def execute(self, research_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute experiments based on the research plan."""
        messages = [
            {"role": "system", "content": "You are a research assistant conducting experiments."},
            {"role": "user", "content": f"Please design and execute experiments for: {research_plan}"}
        ]
        results = self._get_completion(messages)
        return {"plan": research_plan, "results": results}

class ReportWritingAgent(BaseAgent):
    def execute(self, experiment_results: Dict[str, Any]) -> str:
        """Generate a research report based on experiment results."""
        messages = [
            {"role": "system", "content": "You are a research assistant writing a scientific report."},
            {"role": "user", "content": f"Please write a research report based on these results: {experiment_results}"}
        ]
        report = self._get_completion(messages)
        return report 