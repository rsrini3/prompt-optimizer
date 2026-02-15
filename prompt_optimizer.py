"""
Prompt Optimizer - Generates improved versions of user prompts using different techniques
"""

class PromptOptimizer:
    def __init__(self):
        self.techniques = {
            "few_shot": self._apply_few_shot,
            "chain_of_thought": self._apply_chain_of_thought,
            "structured_output": self._apply_structured_output,
            "role_based": self._apply_role_based,
            "concise": self._apply_concise
        }
    
    def generate_variants(self, original_prompt: str) -> dict:
        """Generate 5 improved prompt variants using different techniques"""
        variants = {}
        
        for technique_name, technique_func in self.techniques.items():
            variants[technique_name] = {
                "prompt": technique_func(original_prompt),
                "technique": technique_name.replace("_", " ").title(),
                "description": self._get_technique_description(technique_name)
            }
        
        return variants
    
    def _apply_few_shot(self, prompt: str) -> str:
        """Add few-shot examples to the prompt"""
        return f"""I'll show you some examples first, then you can apply the same pattern.

Example 1:
Input: Write a product description
Output: "Introducing the SmartWatch Pro - where cutting-edge technology meets timeless elegance..."

Example 2:
Input: Summarize this article
Output: "This article discusses three key points: 1) Market trends, 2) Consumer behavior, 3) Future predictions..."

Now, here's your task:
{prompt}

Please follow the same detailed, structured approach shown in the examples above."""
    
    def _apply_chain_of_thought(self, prompt: str) -> str:
        """Add chain-of-thought reasoning"""
        return f"""{prompt}

Please think through this step-by-step:
1. First, analyze what the task is asking for
2. Then, identify the key components needed
3. Next, organize your thoughts logically
4. Finally, provide a comprehensive response

Walk me through your reasoning process before giving the final answer."""
    
    def _apply_structured_output(self, prompt: str) -> str:
        """Request structured, formatted output"""
        return f"""{prompt}

Please provide your response in the following structured format:

**Overview:**
[Brief summary]

**Key Points:**
- Point 1: [Details]
- Point 2: [Details]
- Point 3: [Details]

**Conclusion:**
[Final thoughts]

Ensure each section is clearly labeled and well-organized."""
    
    def _apply_role_based(self, prompt: str) -> str:
        """Add expert role context"""
        return f"""You are an expert professional with deep knowledge in this domain. You have years of experience and are known for providing insightful, accurate, and well-reasoned responses.

Task: {prompt}

As an expert, please provide a thorough response that demonstrates:
- Deep understanding of the subject matter
- Practical, actionable insights
- Clear explanations that are easy to follow
- Professional-level detail and accuracy"""
    
    def _apply_concise(self, prompt: str) -> str:
        """Make the prompt more direct and concise"""
        return f"""{prompt}

Be direct and concise. Provide only the most important information without unnecessary elaboration. Focus on clarity and brevity."""
    
    def _get_technique_description(self, technique: str) -> str:
        """Get description of each technique"""
        descriptions = {
            "few_shot": "Provides examples to guide the model's response pattern",
            "chain_of_thought": "Encourages step-by-step reasoning before answering",
            "structured_output": "Requests organized, formatted responses",
            "role_based": "Assigns expert persona for authoritative answers",
            "concise": "Optimizes for brevity and directness"
        }
        return descriptions.get(technique, "")
