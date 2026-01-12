"""
AI Coding Assistant Evaluation Test Script

Compares code generation quality across:
- Claude Code
- ChatGPT (GPT-4)
- Grok
- Perplexity
- Your Local Instance

Usage:
    python evaluation_test.py --run-all
    python evaluation_test.py --prompt "Write a function to reverse a string"
    python evaluation_test.py --category simple
"""

import json
import time
from datetime import datetime
from typing import List, Dict, Any
import argparse
import os

# API clients (install: pip install openai anthropic requests)
try:
    import anthropic
    from openai import OpenAI
    import requests
except ImportError:
    print("Installing required packages...")
    os.system("pip install anthropic openai requests")
    import anthropic
    from openai import OpenAI
    import requests


# ============================================================================
# TEST PROMPTS
# ============================================================================

TEST_PROMPTS = {
    "simple": [
        {
            "id": "S1",
            "prompt": "Write a Python function to check if a number is prime. Include error handling and type hints.",
            "category": "Code Generation",
            "expected_features": ["function", "type hints", "error handling", "edge cases"]
        },
        {
            "id": "S2",
            "prompt": "Create a function to reverse a string without using built-in reverse functions.",
            "category": "Code Generation",
            "expected_features": ["function", "custom logic", "no built-ins"]
        },
        {
            "id": "S3",
            "prompt": "Write a function to calculate factorial with recursion and iteration examples.",
            "category": "Code Generation",
            "expected_features": ["two implementations", "comparison"]
        },
        {
            "id": "S4",
            "prompt": "Explain what this code does:\n```python\ndef mystery(n):\n    return n if n <= 1 else n * mystery(n-1)\n```",
            "category": "Code Explanation",
            "expected_features": ["identifies recursion", "explains factorial"]
        },
        {
            "id": "S5",
            "prompt": "Write a docstring for this function:\n```python\ndef process_data(data, filter_func=None):\n    result = []\n    for item in data:\n        if filter_func is None or filter_func(item):\n            result.append(item * 2)\n    return result\n```",
            "category": "Documentation",
            "expected_features": ["Args", "Returns", "description"]
        }
    ],

    "medium": [
        {
            "id": "M1",
            "prompt": "Create a Python class for a shopping cart that supports adding items, removing items, calculating total, and applying discount codes.",
            "category": "Code Generation",
            "expected_features": ["class", "methods", "error handling", "docstrings"]
        },
        {
            "id": "M2",
            "prompt": "Implement a rate limiter decorator that allows maximum N calls per M seconds.",
            "category": "Code Generation",
            "expected_features": ["decorator", "time tracking", "thread-safe"]
        },
        {
            "id": "M3",
            "prompt": "Write a function to merge two sorted lists into one sorted list without using built-in sort.",
            "category": "Code Generation",
            "expected_features": ["merge logic", "efficiency", "type hints"]
        },
        {
            "id": "M4",
            "prompt": "Create a context manager for database connections with automatic rollback on errors.",
            "category": "Code Generation",
            "expected_features": ["__enter__", "__exit__", "error handling"]
        },
        {
            "id": "M5",
            "prompt": "Refactor this code to be more Pythonic:\n```python\nresult = []\nfor i in range(len(numbers)):\n    if numbers[i] % 2 == 0:\n        result.append(numbers[i] * 2)\nreturn result\n```",
            "category": "Refactoring",
            "expected_features": ["list comprehension", "explanation"]
        }
    ],

    "complex": [
        {
            "id": "C1",
            "prompt": "Implement a LRU (Least Recently Used) cache in Python with O(1) get and put operations.",
            "category": "Code Generation",
            "expected_features": ["OrderedDict or custom", "O(1) complexity", "explanation"]
        },
        {
            "id": "C2",
            "prompt": "Create a REST API client class for GitHub that handles authentication, rate limiting, and retries.",
            "category": "Code Generation",
            "expected_features": ["class", "auth", "error handling", "retries"]
        },
        {
            "id": "C3",
            "prompt": "Design and implement a task queue system with priority support using Python.",
            "category": "Code Generation",
            "expected_features": ["priority queue", "threading", "error handling"]
        },
        {
            "id": "C4",
            "prompt": "Write a function to detect cycles in a directed graph. Include explanation of the algorithm.",
            "category": "Code Generation",
            "expected_features": ["DFS", "visited tracking", "algorithm explanation"]
        },
        {
            "id": "C5",
            "prompt": "Create a README.md for a Python project that includes: description, installation, usage, examples, and API documentation.",
            "category": "Documentation",
            "expected_features": ["markdown", "sections", "examples"]
        }
    ],

    "debugging": [
        {
            "id": "D1",
            "prompt": "Find the bug in this code:\n```python\ndef get_average(numbers):\n    total = 0\n    for num in numbers:\n        total += num\n    return total / len(numbers)\n```",
            "category": "Debugging",
            "expected_features": ["identifies empty list issue", "provides fix"]
        },
        {
            "id": "D2",
            "prompt": "Why is this code slow and how can it be optimized?\n```python\ndef find_duplicates(lst):\n    duplicates = []\n    for i in range(len(lst)):\n        for j in range(i+1, len(lst)):\n            if lst[i] == lst[j] and lst[i] not in duplicates:\n                duplicates.append(lst[i])\n    return duplicates\n```",
            "category": "Debugging",
            "expected_features": ["identifies O(n²)", "suggests set/dict", "provides optimized code"]
        },
        {
            "id": "D3",
            "prompt": "This code has a memory leak. Identify and fix it:\n```python\nclass DataProcessor:\n    cache = []\n    \n    def process(self, data):\n        self.cache.append(data)\n        return len(self.cache)\n```",
            "category": "Debugging",
            "expected_features": ["identifies class variable issue", "suggests instance variable"]
        }
    ],

    "nhs_specific": [
        {
            "id": "N1",
            "prompt": "Create a Python function to validate NHS numbers (10 digits with check digit validation).",
            "category": "Code Generation",
            "expected_features": ["validation logic", "check digit algorithm", "error handling"]
        },
        {
            "id": "N2",
            "prompt": "Write a function to parse and validate FHIR Patient resources according to the FHIR R4 specification.",
            "category": "Code Generation",
            "expected_features": ["FHIR knowledge", "validation", "error messages"]
        }
    ]
}


# ============================================================================
# AI SYSTEM INTERFACES
# ============================================================================

class AISystemInterface:
    """Base class for AI system interfaces"""

    def __init__(self, name: str):
        self.name = name

    def query(self, prompt: str) -> Dict[str, Any]:
        """Send prompt and return response with metadata"""
        raise NotImplementedError


class ClaudeCodeInterface(AISystemInterface):
    """Interface for Claude Code (Anthropic API)"""

    def __init__(self):
        super().__init__("Claude Code")
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("⚠️  ANTHROPIC_API_KEY not set. Skipping Claude Code.")
            self.client = None
        else:
            self.client = anthropic.Anthropic(api_key=api_key)

    def query(self, prompt: str) -> Dict[str, Any]:
        if not self.client:
            return {"response": "SKIPPED - No API key", "tokens": 0, "time": 0}

        start_time = time.time()
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_time = time.time() - start_time

            return {
                "response": message.content[0].text,
                "tokens": message.usage.input_tokens + message.usage.output_tokens,
                "time": response_time,
                "model": "claude-sonnet-4"
            }
        except Exception as e:
            return {"response": f"ERROR: {str(e)}", "tokens": 0, "time": 0}


class ChatGPTInterface(AISystemInterface):
    """Interface for ChatGPT (OpenAI API)"""

    def __init__(self):
        super().__init__("ChatGPT")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️  OPENAI_API_KEY not set. Skipping ChatGPT.")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)

    def query(self, prompt: str) -> Dict[str, Any]:
        if not self.client:
            return {"response": "SKIPPED - No API key", "tokens": 0, "time": 0}

        start_time = time.time()
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000
            )

            response_time = time.time() - start_time

            return {
                "response": response.choices[0].message.content,
                "tokens": response.usage.total_tokens,
                "time": response_time,
                "model": "gpt-4-turbo"
            }
        except Exception as e:
            return {"response": f"ERROR: {str(e)}", "tokens": 0, "time": 0}


class LocalInstanceInterface(AISystemInterface):
    """Interface for your local AI instance"""

    def __init__(self):
        super().__init__("Local Instance")
        self.base_url = os.getenv("LOCAL_AI_URL", "http://localhost:8000")

    def query(self, prompt: str) -> Dict[str, Any]:
        start_time = time.time()
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={"message": prompt},
                timeout=120
            )

            response_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                return {
                    "response": data.get("response", ""),
                    "tokens": 0,  # Add if your API returns token count
                    "time": response_time,
                    "model": "local-mistral"
                }
            else:
                return {"response": f"ERROR: HTTP {response.status_code}", "tokens": 0, "time": 0}

        except Exception as e:
            return {"response": f"ERROR: {str(e)}", "tokens": 0, "time": 0}


class GrokInterface(AISystemInterface):
    """Interface for Grok (X.AI API)"""

    def __init__(self):
        super().__init__("Grok")
        # Grok API - update when available
        print("⚠️  Grok API interface not implemented yet")
        self.client = None

    def query(self, prompt: str) -> Dict[str, Any]:
        return {"response": "SKIPPED - API not available", "tokens": 0, "time": 0}


class PerplexityInterface(AISystemInterface):
    """Interface for Perplexity"""

    def __init__(self):
        super().__init__("Perplexity")
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            print("⚠️  PERPLEXITY_API_KEY not set. Skipping Perplexity.")
            self.api_key = None
        else:
            self.api_key = api_key

    def query(self, prompt: str) -> Dict[str, Any]:
        if not self.api_key:
            return {"response": "SKIPPED - No API key", "tokens": 0, "time": 0}

        start_time = time.time()
        try:
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-sonar-large-128k-online",
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=120
            )

            response_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                return {
                    "response": data["choices"][0]["message"]["content"],
                    "tokens": data.get("usage", {}).get("total_tokens", 0),
                    "time": response_time,
                    "model": "sonar-large"
                }
            else:
                return {"response": f"ERROR: HTTP {response.status_code}", "tokens": 0, "time": 0}

        except Exception as e:
            return {"response": f"ERROR: {str(e)}", "tokens": 0, "time": 0}


# ============================================================================
# EVALUATION RUNNER
# ============================================================================

class EvaluationRunner:
    """Runs evaluation tests across all AI systems"""

    def __init__(self):
        self.systems = [
            ClaudeCodeInterface(),
            ChatGPTInterface(),
            GrokInterface(),
            PerplexityInterface(),
            LocalInstanceInterface()
        ]

        self.results = []

    def run_single_test(self, test_case: Dict[str, Any]):
        """Run a single test across all systems"""
        print(f"\n{'='*80}")
        print(f"Test ID: {test_case['id']}")
        print(f"Category: {test_case['category']}")
        print(f"Prompt: {test_case['prompt'][:100]}...")
        print(f"{'='*80}\n")

        test_result = {
            "test_id": test_case["id"],
            "prompt": test_case["prompt"],
            "category": test_case["category"],
            "timestamp": datetime.now().isoformat(),
            "responses": {}
        }

        for system in self.systems:
            print(f"🤖 Testing {system.name}...")
            response = system.query(test_case["prompt"])
            test_result["responses"][system.name] = response

            # Preview response
            preview = response["response"][:200].replace("\n", " ")
            print(f"   Response: {preview}...")
            print(f"   Time: {response['time']:.2f}s\n")

            # Rate limiting delay
            time.sleep(2)

        self.results.append(test_result)
        return test_result

    def run_category(self, category: str):
        """Run all tests in a category"""
        if category not in TEST_PROMPTS:
            print(f"❌ Unknown category: {category}")
            print(f"Available: {list(TEST_PROMPTS.keys())}")
            return

        print(f"\n🚀 Running {category.upper()} tests...")

        for test_case in TEST_PROMPTS[category]:
            self.run_single_test(test_case)

    def run_all(self):
        """Run all tests"""
        print("\n🚀 Running ALL evaluation tests...")
        print(f"Total tests: {sum(len(tests) for tests in TEST_PROMPTS.values())}")

        for category in TEST_PROMPTS.keys():
            self.run_category(category)

    def save_results(self, filename: str = None):
        """Save results to JSON file"""
        if filename is None:
            filename = f"evaluation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "total_tests": len(self.results),
                    "systems": [s.name for s in self.systems]
                },
                "results": self.results
            }, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Results saved to: {filename}")
        return filename

    def generate_report(self):
        """Generate markdown report"""
        report_lines = [
            "# AI Coding Assistant Evaluation Report",
            f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"\n**Total Tests:** {len(self.results)}",
            "\n---\n"
        ]

        for result in self.results:
            report_lines.append(f"\n## Test {result['test_id']}: {result['category']}")
            report_lines.append(f"\n**Prompt:**\n```\n{result['prompt']}\n```\n")

            for system_name, response in result['responses'].items():
                report_lines.append(f"\n### {system_name}")

                if response['response'].startswith("ERROR") or response['response'].startswith("SKIPPED"):
                    report_lines.append(f"\n⚠️ {response['response']}\n")
                else:
                    report_lines.append(f"\n**Response:**\n```python\n{response['response'][:500]}...\n```\n")
                    report_lines.append(f"**Time:** {response['time']:.2f}s | **Tokens:** {response['tokens']}\n")

            report_lines.append("\n**Manual Evaluation:** (Score each 1-5)")
            report_lines.append("\n| System | Correctness | Quality | Completeness | Context | Explanation | Total |")
            report_lines.append("\n|--------|-------------|---------|--------------|---------|-------------|-------|")

            for system_name in result['responses'].keys():
                report_lines.append(f"\n| {system_name} | - | - | - | - | - | - |")

            report_lines.append("\n\n---\n")

        report_filename = f"evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))

        print(f"✅ Report generated: {report_filename}")
        return report_filename


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="AI Coding Assistant Evaluation")
    parser.add_argument("--run-all", action="store_true", help="Run all tests")
    parser.add_argument("--category", type=str, help="Run tests for specific category")
    parser.add_argument("--prompt", type=str, help="Test a custom prompt")
    parser.add_argument("--list-categories", action="store_true", help="List available categories")

    args = parser.parse_args()

    if args.list_categories:
        print("\n📋 Available test categories:")
        for category, tests in TEST_PROMPTS.items():
            print(f"  - {category}: {len(tests)} tests")
        return

    runner = EvaluationRunner()

    if args.run_all:
        runner.run_all()
    elif args.category:
        runner.run_category(args.category)
    elif args.prompt:
        test_case = {
            "id": "CUSTOM",
            "prompt": args.prompt,
            "category": "Custom",
            "expected_features": []
        }
        runner.run_single_test(test_case)
    else:
        print("❌ No action specified. Use --help for options")
        return

    # Save results
    runner.save_results()
    runner.generate_report()

    print("\n✅ Evaluation complete!")
    print("\nNext steps:")
    print("1. Open the generated Markdown report")
    print("2. Manually score each response (1-5)")
    print("3. Calculate total scores")
    print("4. Identify areas for improvement")


if __name__ == "__main__":
    main()
