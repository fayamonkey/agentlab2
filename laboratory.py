import os
from typing import Dict, Any, Optional
from agents import LiteratureReviewAgent, ExperimentationAgent, ReportWritingAgent

class AgentLaboratory:
    def __init__(self, api_key: str, model_name: str = "gpt-4o"):
        """Initialize the Agent Laboratory with the specified model."""
        os.environ["OPENAI_API_KEY"] = api_key
        self.model_name = model_name
        
        # Initialize agents
        self.literature_agent = LiteratureReviewAgent(model_name)
        self.experiment_agent = ExperimentationAgent(model_name)
        self.report_agent = ReportWritingAgent(model_name)
        
        # Store research artifacts
        self.research_review = None
        self.experiment_results = None
        self.final_report = None
    
    def conduct_research(self, research_topic: str, task_notes: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute the complete research workflow."""
        print(f"Starting research on: {research_topic}")
        
        # Phase 1: Literature Review
        print("\nPhase 1: Conducting Literature Review...")
        self.research_review = self.literature_agent.execute(research_topic)
        
        # Phase 2: Experimentation
        print("\nPhase 2: Planning and Executing Experiments...")
        research_plan = {
            "topic": research_topic,
            "literature_review": self.research_review,
            "task_notes": task_notes
        }
        self.experiment_results = self.experiment_agent.execute(research_plan)
        
        # Phase 3: Report Writing
        print("\nPhase 3: Generating Research Report...")
        self.final_report = self.report_agent.execute({
            "topic": research_topic,
            "literature_review": self.research_review,
            "experiment_results": self.experiment_results,
            "task_notes": task_notes
        })
        
        return {
            "topic": research_topic,
            "literature_review": self.research_review,
            "experiment_results": self.experiment_results,
            "final_report": self.final_report
        }
    
    def get_research_status(self) -> Dict[str, bool]:
        """Get the current status of research phases."""
        return {
            "literature_review_complete": self.research_review is not None,
            "experiments_complete": self.experiment_results is not None,
            "report_complete": self.final_report is not None
        } 