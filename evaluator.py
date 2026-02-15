"""
Evaluator - Tests prompt variants and scores them on multiple dimensions
"""

from openai import OpenAI
import time

class PromptEvaluator:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.test_question = "Explain the concept of machine learning to a beginner."
        
    def evaluate_prompt(self, prompt_text: str, technique_name: str) -> dict:
        """
        Test a prompt variant and return scores + metrics
        """
        start_time = time.time()
        
        try:
            # Get response from the prompt
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using mini for cost efficiency
                messages=[
                    {"role": "user", "content": prompt_text}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            execution_time = time.time() - start_time
            response_text = response.choices[0].message.content
            
            # Calculate costs (approximate for gpt-4o-mini)
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            cost = (input_tokens * 0.00015 / 1000) + (output_tokens * 0.0006 / 1000)
            
            # Score the response quality
            scores = self._score_response(response_text, prompt_text)
            
            return {
                "success": True,
                "response": response_text,
                "scores": scores,
                "metrics": {
                    "execution_time": round(execution_time, 2),
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens,
                    "cost_usd": round(cost, 6),
                    "technique": technique_name
                },
                "overall_score": round(sum(scores.values()) / len(scores), 1)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "scores": {},
                "metrics": {},
                "overall_score": 0
            }
    
    def _score_response(self, response: str, prompt: str) -> dict:
        """
        Score response on multiple dimensions (0-10 scale)
        This is a simplified heuristic-based scoring. 
        For production, you'd use another LLM to judge quality.
        """
        scores = {}
        
        # Quality score (based on length and structure)
        word_count = len(response.split())
        if 50 <= word_count <= 300:
            scores["quality"] = 9.0
        elif word_count < 50:
            scores["quality"] = 6.0
        else:
            scores["quality"] = 7.5
        
        # Clarity score (presence of structure indicators)
        clarity_indicators = ["first", "second", "example", ":", "-", "1.", "2."]
        clarity_count = sum(1 for indicator in clarity_indicators if indicator.lower() in response.lower())
        scores["clarity"] = min(10.0, 6.0 + clarity_count * 0.8)
        
        # Completeness score (response length relative to prompt complexity)
        prompt_length = len(prompt.split())
        completeness_ratio = word_count / max(prompt_length, 10)
        scores["completeness"] = min(10.0, 5.0 + completeness_ratio * 2)
        
        # Relevance score (simple keyword matching)
        # For a real implementation, use semantic similarity
        scores["relevance"] = 8.5  # Simplified
        
        return scores
    
    def evaluate_all_variants(self, variants: dict) -> dict:
        """
        Evaluate all prompt variants and return comprehensive results
        """
        results = {}
        total_cost = 0
        
        for technique_name, variant_data in variants.items():
            print(f"Evaluating {technique_name}...")
            result = self.evaluate_prompt(
                variant_data["prompt"], 
                variant_data["technique"]
            )
            results[technique_name] = result
            
            if result["success"]:
                total_cost += result["metrics"].get("cost_usd", 0)
        
        # Find the best performing variant
        best_variant = max(
            results.items(),
            key=lambda x: x[1].get("overall_score", 0)
        )
        
        return {
            "results": results,
            "summary": {
                "total_cost_usd": round(total_cost, 6),
                "best_variant": best_variant[0],
                "best_score": best_variant[1].get("overall_score", 0)
            }
        }
