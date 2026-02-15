"""
Prompt Optimizer - Main Gradio Application
Generates improved prompt variants and evaluates them
"""

import gradio as gr
import os
from dotenv import load_dotenv
from prompt_optimizer import PromptOptimizer
from evaluator import PromptEvaluator

# Load environment variables
load_dotenv()

# Initialize components
optimizer = PromptOptimizer()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please create a .env file.")

evaluator = PromptEvaluator(api_key)

def optimize_and_evaluate(original_prompt: str, test_prompts: bool = True):
    """
    Main function that generates variants and optionally tests them
    """
    if not original_prompt or len(original_prompt.strip()) < 10:
        return "❌ Please enter a prompt with at least 10 characters.", "", ""
    
    # Generate variants
    variants = optimizer.generate_variants(original_prompt)
    
    # Format variants for display
    variants_output = "## 📝 Generated Prompt Variants\n\n"
    for i, (technique, data) in enumerate(variants.items(), 1):
        variants_output += f"### {i}. {data['technique']}\n"
        variants_output += f"*{data['description']}*\n\n"
        variants_output += f"```\n{data['prompt']}\n```\n\n"
        variants_output += "---\n\n"
    
    # If user wants to test prompts
    if test_prompts:
        results_output = "## 🎯 Evaluation Results\n\n"
        results_output += "*Testing all variants with GPT-4o-mini...*\n\n"
        
        eval_results = evaluator.evaluate_all_variants(variants)
        
        # Sort by score
        sorted_results = sorted(
            eval_results["results"].items(),
            key=lambda x: x[1].get("overall_score", 0),
            reverse=True
        )
        
        # Display results
        for rank, (technique, result) in enumerate(sorted_results, 1):
            if result["success"]:
                medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."
                results_output += f"### {medal} {variants[technique]['technique']}\n"
                results_output += f"**Overall Score: {result['overall_score']}/10**\n\n"
                
                # Scores breakdown
                results_output += "**Scores:**\n"
                for metric, score in result["scores"].items():
                    results_output += f"- {metric.title()}: {score:.1f}/10\n"
                
                # Metrics
                results_output += f"\n**Metrics:**\n"
                results_output += f"- Tokens: {result['metrics']['total_tokens']}\n"
                results_output += f"- Cost: ${result['metrics']['cost_usd']:.6f}\n"
                results_output += f"- Time: {result['metrics']['execution_time']}s\n"
                
                # Sample response
                results_output += f"\n**Sample Response Preview:**\n"
                preview = result["response"][:200] + "..." if len(result["response"]) > 200 else result["response"]
                results_output += f"```\n{preview}\n```\n\n"
                results_output += "---\n\n"
        
        # Summary
        summary = f"""## 💰 Cost Summary
        
**Total Cost:** ${eval_results['summary']['total_cost_usd']:.6f}

**🏆 Best Performing Variant:** {variants[eval_results['summary']['best_variant']]['technique']}
**Best Score:** {eval_results['summary']['best_score']}/10

*Note: Scores are heuristic-based. For production, use LLM-as-judge for more accurate evaluation.*
"""
        
        return variants_output, results_output, summary
    
    else:
        return variants_output, "*(Evaluation skipped - toggle 'Test Prompts' to see results)*", ""


# Custom CSS for better styling
custom_css = """
.gradio-container {
    font-family: 'Inter', sans-serif;
}
.output-markdown h2 {
    color: #2563eb;
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 8px;
}
.output-markdown h3 {
    color: #4b5563;
}
"""

# Build Gradio Interface
with gr.Blocks(css=custom_css, title="Prompt Optimizer") as demo:
    gr.Markdown("""
    # 🚀 Prompt Optimizer
    
    **Transform basic prompts into optimized versions using proven techniques**
    
    This tool generates 5 improved variants of your prompt using different optimization techniques:
    - Few-Shot Learning
    - Chain-of-Thought Reasoning
    - Structured Output
    - Role-Based Prompting
    - Concise Prompting
    
    Optionally test each variant with GPT-4o-mini to see which performs best!
    """)
    
    with gr.Row():
        with gr.Column():
            original_prompt = gr.Textbox(
                label="Enter Your Original Prompt",
                placeholder="e.g., 'Write a blog post about AI'",
                lines=5
            )
            
            test_toggle = gr.Checkbox(
                label="Test prompts with OpenAI API (costs ~$0.001-0.005 per test)",
                value=True
            )
            
            optimize_btn = gr.Button("🎯 Generate & Evaluate", variant="primary", size="lg")
            
            gr.Markdown("""
            ### 💡 Tips:
            - Start with a simple, basic prompt
            - The tool will enhance it using 5 different techniques
            - Testing shows which technique works best for your use case
            """)
    
    with gr.Column():
        variants_display = gr.Markdown(label="Generated Variants")
    
    with gr.Row():
        with gr.Column():
            results_display = gr.Markdown(label="Evaluation Results")
        with gr.Column():
            summary_display = gr.Markdown(label="Summary")
    
    # Event handler
    optimize_btn.click(
        fn=optimize_and_evaluate,
        inputs=[original_prompt, test_toggle],
        outputs=[variants_display, results_display, summary_display]
    )
    
    gr.Markdown("""
    ---
    
    ### 📊 How to Use This for Your Portfolio:
    
    1. **Screenshot results** showing before/after prompts with scores
    2. **Share on LinkedIn** with insights about which techniques work best
    3. **Explain the engineering**: variant generation, API orchestration, evaluation metrics
    4. **Show cost optimization**: Compare token usage across techniques
    
    **Built with:** OpenAI API, Gradio, Python
    """)

# Launch the app
if __name__ == "__main__":
    demo.launch(share=False)
