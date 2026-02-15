# 🚀 Prompt Optimizer

An intelligent tool that generates and evaluates improved prompt variants using different optimization techniques.

## 📋 What It Does

Takes your basic prompt and generates **5 optimized versions** using proven techniques:

1. **Few-Shot Learning** - Adds examples to guide response patterns
2. **Chain-of-Thought** - Encourages step-by-step reasoning
3. **Structured Output** - Requests organized, formatted responses
4. **Role-Based** - Assigns expert persona for authoritative answers
5. **Concise** - Optimizes for brevity and directness

Then **tests each variant** with OpenAI's API and shows you:
- Quality scores (quality, clarity, completeness, relevance)
- Performance metrics (tokens, cost, execution time)
- Which technique works best for your use case

## 🎯 Skills Demonstrated

- **LLM Orchestration**: Multiple API calls with different prompts
- **Prompt Engineering**: 5 different optimization techniques
- **Evaluation Systems**: Automated scoring and comparison
- **Cost Optimization**: Token tracking and cost analysis
- **UI Development**: Clean Gradio interface

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.8+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### 2. Installation

```bash
# Clone or download this project
cd prompt-optimizer

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
cp .env.example .env
```

### 3. Configure API Key

Edit `.env` file and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 4. Run the App

```bash
python app.py
```

The app will launch at `http://127.0.0.1:7860`

## 💻 Usage

1. **Enter your basic prompt** (e.g., "Write a blog post about AI")
2. **Toggle "Test prompts"** if you want to evaluate with real API calls
3. **Click "Generate & Evaluate"**
4. **Review results**:
   - See all 5 optimized variants
   - View scores and rankings
   - Check cost breakdown

## 💰 Cost Estimate

- Each full test costs approximately **$0.001-0.005** (using GPT-4o-mini)
- Testing 5 variants: ~$0.005-0.025 per run
- Very affordable for development and demos!

## 🔧 Technical Architecture

```
app.py                  # Gradio UI and orchestration
├── prompt_optimizer.py # Generates 5 variant techniques
├── evaluator.py        # Tests variants and scores results
└── requirements.txt    # Dependencies
```

**Key Components:**
- `PromptOptimizer`: Applies 5 different prompt engineering techniques
- `PromptEvaluator`: Tests each variant via OpenAI API and scores results
- Gradio Interface: Clean UI with real-time results


## 📝 License

MIT License - Feel free to use this in your portfolio!