from deepeval.metrics import ToxicityMetric, BiasMetric
from deepeval.test_case import LLMTestCase
from deepeval.models import AzureOpenAI
from config import settings
from typing import List, Dict, Any

class Moderator:
    def __init__(self):
        self.azure_model = AzureOpenAI(
            deployment_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            api_key=settings.AZURE_OPENAI_API_KEY,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_version=settings.AZURE_OPENAI_API_VERSION
        )
        
    def _create_input_metrics(self) -> List:
        return [
            ToxicityMetric(
                threshold=0.5,
                model=self.azure_model,
                include_reason=True
            ),
            BiasMetric(
                threshold=0.5,
                model=self.azure_model,
                include_reason=True
            )
        ]
    
    def _create_output_metrics(self) -> List:
        return [
            ToxicityMetric(
                threshold=0.5,
                model=self.azure_model,
                include_reason=True
            ),
            BiasMetric(
                threshold=0.5,
                model=self.azure_model,
                include_reason=True
            )
        ]
    
    def moderate_input(self, user_input: str) -> Dict[str, Any]:
        metrics = self._create_input_metrics()
        test_case = LLMTestCase(
            input=user_input,
            actual_output=""
        )
        
        results = []
        overall_passed = True
        
        for metric in metrics:
            metric.measure(test_case)
            
            result = {
                "passed": metric.score <= metric.threshold,
                "score": metric.score,
                "metric_name": metric.__class__.__name__,
                "reason": metric.reason if hasattr(metric, 'reason') else ""
            }
            results.append(result)
            
            if not result["passed"]:
                overall_passed = False
        
        return {
            "results": results,
            "overall_passed": overall_passed,
            "details": {
                "input": user_input,
                "metrics_evaluated": len(metrics)
            }
        }
    
    def moderate_output(self, ai_response: str) -> Dict[str, Any]:
        metrics = self._create_output_metrics()
        test_case = LLMTestCase(
            input="",
            actual_output=ai_response
        )
        
        results = []
        overall_passed = True
        
        for metric in metrics:
            metric.measure(test_case)
            
            result = {
                "passed": metric.score <= metric.threshold,
                "score": metric.score,
                "metric_name": metric.__class__.__name__,
                "reason": metric.reason if hasattr(metric, 'reason') else ""
            }
            results.append(result)
            
            if not result["passed"]:
                overall_passed = False
        
        return {
            "results": results,
            "overall_passed": overall_passed,
            "details": {
                "output": ai_response,
                "metrics_evaluated": len(metrics)
            }
        }
