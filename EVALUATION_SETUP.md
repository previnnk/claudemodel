# Evaluation Test Setup Guide

Complete guide to running the AI coding assistant evaluation tests.

---

## 📋 Prerequisites

### 1. Python 3.11+
```bash
python --version
# Should show Python 3.11 or higher
```

### 2. Install Dependencies
```bash
cd D:\workspace\NHS\ClaudeModel
pip install anthropic openai requests
```

---

## 🔑 API Keys Setup

You need API keys to test against commercial AI systems.

### Get API Keys

| Service | Where to Get | Environment Variable |
|---------|--------------|---------------------|
| **Claude Code** | https://console.anthropic.com/ | `ANTHROPIC_API_KEY` |
| **ChatGPT** | https://platform.openai.com/ | `OPENAI_API_KEY` |
| **Perplexity** | https://www.perplexity.ai/settings/api | `PERPLEXITY_API_KEY` |
| **Grok** | Not yet available | N/A |
| **Local Instance** | Your deployment | `LOCAL_AI_URL` |

### Set Environment Variables

#### Windows (PowerShell)
```powershell
# Set for current session
$env:ANTHROPIC_API_KEY="sk-ant-..."
$env:OPENAI_API_KEY="sk-..."
$env:PERPLEXITY_API_KEY="pplx-..."
$env:LOCAL_AI_URL="http://localhost:8000"

# Set permanently
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-...", "User")
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-...", "User")
[Environment]::SetEnvironmentVariable("PERPLEXITY_API_KEY", "pplx-...", "User")
[Environment]::SetEnvironmentVariable("LOCAL_AI_URL", "http://localhost:8000", "User")
```

#### Windows (Command Prompt)
```batch
setx ANTHROPIC_API_KEY "sk-ant-..."
setx OPENAI_API_KEY "sk-..."
setx PERPLEXITY_API_KEY "pplx-..."
setx LOCAL_AI_URL "http://localhost:8000"
```

#### Linux/Mac
```bash
# Add to ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export PERPLEXITY_API_KEY="pplx-..."
export LOCAL_AI_URL="http://localhost:8000"

# Reload
source ~/.bashrc
```

### Create .env File (Alternative)
```bash
# Create .env file
cat > .env << EOF
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
PERPLEXITY_API_KEY=pplx-...
LOCAL_AI_URL=http://localhost:8000
EOF

# Load in Python script (requires python-dotenv)
pip install python-dotenv
```

---

## 🚀 Running Tests

### List Available Tests
```bash
python evaluation_test.py --list-categories
```

**Output:**
```
📋 Available test categories:
  - simple: 5 tests
  - medium: 5 tests
  - complex: 5 tests
  - debugging: 3 tests
  - nhs_specific: 2 tests
```

### Run All Tests
```bash
python evaluation_test.py --run-all
```

**This will:**
- Run 20 test prompts across all AI systems
- Save results to JSON
- Generate a Markdown report
- Take ~40-60 minutes (rate limiting)

### Run Specific Category
```bash
# Run only simple tests (fastest)
python evaluation_test.py --category simple

# Run medium complexity tests
python evaluation_test.py --category medium

# Run complex tests
python evaluation_test.py --category complex

# Run debugging tests
python evaluation_test.py --category debugging

# Run NHS-specific tests
python evaluation_test.py --category nhs_specific
```

### Test Custom Prompt
```bash
python evaluation_test.py --prompt "Write a Python function to reverse a string"
```

---

## 📊 Understanding Results

### Output Files

After running tests, you'll get:

1. **`evaluation_results_YYYYMMDD_HHMMSS.json`**
   - Raw data with all responses
   - Token counts, timing
   - Can be processed programmatically

2. **`evaluation_report_YYYYMMDD_HHMMSS.md`**
   - Formatted Markdown report
   - Side-by-side comparisons
   - Manual scoring template

### Sample Report Structure

```markdown
# AI Coding Assistant Evaluation Report

**Generated:** 2026-01-10 14:30:00
**Total Tests:** 5

---

## Test S1: Code Generation

**Prompt:**
Write a Python function to check if a number is prime...

### Claude Code
**Response:**
```python
def is_prime(n: int) -> bool:
    ...
```
**Time:** 2.3s | **Tokens:** 450

### ChatGPT
**Response:**
```python
def is_prime(n):
    ...
```
**Time:** 1.8s | **Tokens:** 380

### Your Local Instance
**Response:**
```python
def check_prime(num):
    ...
```
**Time:** 3.5s | **Tokens:** N/A

**Manual Evaluation:**
| System | Correctness | Quality | Completeness | Context | Explanation | Total |
|--------|-------------|---------|--------------|---------|-------------|-------|
| Claude Code | - | - | - | - | - | - |
| ChatGPT | - | - | - | - | - | - |
| Local Instance | - | - | - | - | - | - |
```

---

## 📝 Manual Scoring

### Step 1: Open the Report
```bash
# Open in VS Code
code evaluation_report_20260110_143000.md

# Or use notepad
notepad evaluation_report_20260110_143000.md
```

### Step 2: Score Each Response

For each test, fill in scores (1-5) in the table:

**Correctness** (30% weight)
- 5: Perfect, handles all edge cases
- 4: Good, minor issues
- 3: Works for basic cases
- 2: Has bugs
- 1: Doesn't work

**Quality** (25% weight)
- 5: Production-ready code
- 4: Good code style
- 3: Acceptable
- 2: Needs refactoring
- 1: Poor quality

**Completeness** (20% weight)
- 5: Full implementation with docs
- 4: Complete with good docs
- 3: Complete, basic docs
- 2: Partial implementation
- 1: Incomplete

**Context Understanding** (15% weight)
- 5: Perfect understanding
- 4: Good understanding
- 3: Adequate understanding
- 2: Misunderstood some parts
- 1: Didn't understand

**Explanation Quality** (10% weight)
- 5: Excellent explanation
- 4: Good explanation
- 3: Basic explanation
- 2: Minimal explanation
- 1: No explanation

### Step 3: Calculate Total Scores

```python
# Formula
Total = (Correctness × 0.30) +
        (Quality × 0.25) +
        (Completeness × 0.20) +
        (Context × 0.15) +
        (Explanation × 0.10)
```

**Example:**
```
Claude Code:
- Correctness: 5
- Quality: 5
- Completeness: 5
- Context: 5
- Explanation: 4

Total = (5×0.30) + (5×0.25) + (5×0.20) + (5×0.15) + (4×0.10)
      = 1.5 + 1.25 + 1.0 + 0.75 + 0.4
      = 4.9 / 5.0 ⭐⭐⭐⭐⭐
```

---

## 📈 Analyzing Results

### Create Summary Table

| AI System | Avg Correctness | Avg Quality | Avg Complete | Avg Context | Avg Explain | **Overall** | Rank |
|-----------|----------------|-------------|--------------|-------------|-------------|-------------|------|
| Claude Code | 4.8 | 4.9 | 4.7 | 5.0 | 4.5 | **4.82** | 🥇 1 |
| ChatGPT | 4.5 | 4.6 | 4.3 | 4.7 | 4.8 | **4.56** | 🥈 2 |
| Perplexity | 4.2 | 4.0 | 3.8 | 4.0 | 4.5 | **4.08** | 🥉 3 |
| Local Instance | 3.8 | 3.5 | 3.2 | 3.5 | 3.0 | **3.46** | 4 |
| Grok | N/A | N/A | N/A | N/A | N/A | N/A | - |

### Identify Gaps

**Example Analysis:**
```
Your Local Instance vs Claude Code:

Strengths:
✅ Reasonable correctness (3.8/5)
✅ Handles basic cases well

Weaknesses:
❌ Code quality needs improvement (-1.4 points)
❌ Missing comprehensive documentation (-1.5 points)
❌ Explanations are basic (-1.5 points)

Action Items:
1. Improve prompt engineering for better code quality
2. Add system prompt for documentation generation
3. Fine-tune on examples with detailed explanations
```

---

## 🔧 Improving Your Local Instance

### Based on Evaluation Results

#### If Correctness is Low (<4.0)
```python
# Improve base prompt
system_prompt = """
You are an expert programmer. Always:
1. Write correct, bug-free code
2. Handle edge cases (empty input, None, negative numbers)
3. Add error handling
4. Test your logic before responding
"""
```

#### If Quality is Low (<4.0)
```python
# Add code quality guidelines
system_prompt += """
Code Quality Requirements:
- Use type hints (Python)
- Follow PEP 8 style guide
- Clear variable names
- No magic numbers
- DRY principle
"""
```

#### If Completeness is Low (<4.0)
```python
# Enforce documentation
system_prompt += """
Always include:
1. Docstrings (Args, Returns, Raises)
2. Inline comments for complex logic
3. Usage examples
"""
```

### Fine-tuning Strategy

If your local instance scores < 3.5:

1. **Collect Training Data**
   ```bash
   # Extract high-scoring examples from Claude/ChatGPT
   python extract_training_data.py evaluation_results_*.json
   ```

2. **Fine-tune Model**
   ```bash
   # Use LoRA fine-tuning (see NHS_FINETUNING.md)
   python train_lora.py --data training_data.jsonl
   ```

3. **Re-test**
   ```bash
   # Run evaluation again
   python evaluation_test.py --run-all
   ```

---

## 🎯 Target Scores

### Minimum Viable (MVP)
- Overall: ≥ 3.5
- Correctness: ≥ 4.0
- Quality: ≥ 3.0

### Production Ready
- Overall: ≥ 4.0
- Correctness: ≥ 4.5
- All categories: ≥ 3.5

### Claude Code Parity
- Overall: ≥ 4.5
- All categories: ≥ 4.0

---

## 📅 Recommended Testing Schedule

### Initial Deployment
- ✅ Day 1: Run all tests, establish baseline
- ✅ Day 2-3: Analyze results, identify gaps
- ✅ Day 4-7: Improve prompts, test again

### Ongoing
- **Weekly**: Run 5 new custom prompts
- **Monthly**: Full evaluation (all categories)
- **Quarterly**: Compare against updated AI systems

---

## 🛠️ Troubleshooting

### "API Key Invalid"
```bash
# Check environment variables
echo $ANTHROPIC_API_KEY  # Linux/Mac
echo %ANTHROPIC_API_KEY%  # Windows CMD
$env:ANTHROPIC_API_KEY   # Windows PowerShell

# Verify key format
# Anthropic: sk-ant-...
# OpenAI: sk-...
# Perplexity: pplx-...
```

### "Local Instance Not Responding"
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check docker containers
docker-compose ps

# View logs
docker-compose logs backend
```

### "Tests Taking Too Long"
```bash
# Run smaller category first
python evaluation_test.py --category simple

# Or test single prompt
python evaluation_test.py --prompt "Write hello world"
```

---

## 💡 Tips

1. **Start Small**: Run `--category simple` first (5 tests, ~10 min)
2. **API Costs**: Claude/ChatGPT charge per token (~$0.50 for full test suite)
3. **Rate Limits**: Script includes 2s delays between requests
4. **Save Results**: Keep all JSON files for historical comparison
5. **Document Changes**: Note prompt changes, model updates in results

---

## 📚 Next Steps

1. ✅ Set up API keys
2. ✅ Run first evaluation: `python evaluation_test.py --category simple`
3. ✅ Manually score results
4. ✅ Calculate averages
5. ✅ Identify improvement areas
6. ✅ Implement improvements
7. 🔄 Re-test and compare

---

**Ready to start?**

```bash
# Quick test (1 prompt)
python evaluation_test.py --prompt "Write a function to reverse a string"

# Full simple category (5 prompts, 10 min)
python evaluation_test.py --category simple

# Everything (20 prompts, 60 min)
python evaluation_test.py --run-all
```

Good luck! 🚀
