# NHS Healthcare Data Fine-tuning Guide

Complete guide for fine-tuning LLMs on NHS healthcare and clinical equipment data.

---

## ⚠️ Important Legal and Ethical Considerations

### Data Compliance
- **GDPR** compliance required
- **NHS Data Security Standards** must be met
- **Patient data** must be anonymized/de-identified
- **Data Processing Agreement** (DPA) required
- **Information Governance** approval needed

### Recommended Approach
1. Use **synthetic medical data** for initial testing
2. Use **publicly available medical knowledge** bases
3. For real NHS data: work with Information Governance team
4. Ensure **audit trails** for all data processing

---

## Overview

```
Data Sources → Preprocessing → Fine-tuning → Evaluation → Deployment
```

---

## Table of Contents
1. [Data Sources](#data-sources)
2. [Data Preprocessing](#data-preprocessing)
3. [Fine-tuning Methods](#fine-tuning-methods)
4. [Training Setup](#training-setup)
5. [Evaluation](#evaluation)
6. [Deployment](#deployment)

---

## Data Sources

### 1. Public Medical Knowledge Bases (Recommended for Starting)

#### Medical Documentation
- **PubMed Central**: Open access medical literature
- **MIMIC-III/IV**: De-identified ICU data (requires credentialing)
- **UK Biobank**: Health research data (application required)

#### Clinical Guidelines
- **NICE Guidelines**: https://www.nice.org.uk/guidance
- **NHS Digital Standards**: Public documentation
- **Medical Device Information**: MHRA public database

#### Code Examples
```python
# Download NICE guidelines
import requests
from bs4 import BeautifulSoup

def download_nice_guidelines():
    # Example: scrape public NICE guidelines
    url = "https://www.nice.org.uk/guidance/published"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Parse and save guidelines
    pass
```

### 2. NHS Internal Data (Requires Approval)

#### Clinical Notes (De-identified)
- Progress notes
- Discharge summaries
- Consultation records

#### Equipment Documentation
- Maintenance logs
- User manuals
- Troubleshooting guides
- Safety protocols

#### Structured Data
- ICD-10 codes
- SNOMED CT codes
- Equipment inventory
- Service records

### 3. Synthetic Medical Data (For Testing)

```python
# Generate synthetic medical data
from faker import Faker
from faker_medical import MedicalProvider

fake = Faker()
fake.add_provider(MedicalProvider)

def generate_synthetic_record():
    return {
        "patient_id": fake.uuid4(),
        "diagnosis": fake.icd10_code(),
        "procedure": fake.procedure(),
        "equipment": fake.random_element([
            "MRI Scanner",
            "CT Scanner",
            "Ventilator",
            "ECG Monitor"
        ]),
        "notes": fake.clinical_note()
    }
```

---

## Data Preprocessing

### 1. Data Collection Script

```python
# scripts/collect_nhs_data.py
import os
import json
from pathlib import Path
from typing import List, Dict

class NHSDataCollector:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def collect_clinical_guidelines(self) -> List[Dict]:
        """Collect clinical guidelines"""
        guidelines = []
        # Implementation for collecting guidelines
        return guidelines

    def collect_equipment_docs(self) -> List[Dict]:
        """Collect equipment documentation"""
        docs = []
        # Implementation for equipment docs
        return docs

    def anonymize_data(self, data: List[Dict]) -> List[Dict]:
        """Anonymize patient data"""
        # Remove PII: names, NHS numbers, addresses, etc.
        anonymized = []
        for record in data:
            # Implement anonymization logic
            pass
        return anonymized

    def save_dataset(self, data: List[Dict], filename: str):
        """Save processed dataset"""
        output_path = self.data_dir / filename
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
```

### 2. Data Format for Fine-tuning

#### Instruction Format (Recommended)
```jsonl
{"instruction": "What is the maintenance protocol for CT scanners?", "input": "", "output": "Regular maintenance of CT scanners includes:\n1. Daily: Check image quality\n2. Weekly: Clean gantry and patient table\n3. Monthly: Calibration checks\n..."}
{"instruction": "Explain hypertension treatment guidelines", "input": "Patient: 65 years, BP 150/95", "output": "According to NICE guidelines:\n1. Lifestyle advice\n2. Consider ACE inhibitor\n..."}
```

#### Conversational Format
```jsonl
{"conversations": [{"from": "human", "value": "What equipment is needed for intubation?"}, {"from": "assistant", "value": "Essential equipment for intubation includes:\n1. Laryngoscope\n2. Endotracheal tubes (various sizes)\n3. Stylet\n..."}]}
```

### 3. Preprocessing Script

```python
# scripts/preprocess_nhs_data.py
import json
import re
from typing import List, Dict

class NHSDataPreprocessor:
    def __init__(self):
        self.pii_patterns = {
            'nhs_number': r'\b\d{3}[-\s]?\d{3}[-\s]?\d{4}\b',
            'name': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
            'postcode': r'\b[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}\b',
        }

    def remove_pii(self, text: str) -> str:
        """Remove personally identifiable information"""
        for pii_type, pattern in self.pii_patterns.items():
            text = re.sub(pattern, f'[{pii_type.upper()}]', text)
        return text

    def create_instruction_pairs(
        self,
        documents: List[Dict]
    ) -> List[Dict]:
        """Convert documents to instruction-following format"""
        pairs = []
        for doc in documents:
            # Extract Q&A pairs from documentation
            if doc['type'] == 'clinical_guideline':
                pairs.extend(self._extract_guideline_pairs(doc))
            elif doc['type'] == 'equipment_manual':
                pairs.extend(self._extract_equipment_pairs(doc))
        return pairs

    def _extract_guideline_pairs(self, doc: Dict) -> List[Dict]:
        """Extract instruction pairs from clinical guidelines"""
        # Implementation
        return []

    def _extract_equipment_pairs(self, doc: Dict) -> List[Dict]:
        """Extract instruction pairs from equipment manuals"""
        # Implementation
        return []

    def save_training_data(self, pairs: List[Dict], output_file: str):
        """Save in JSONL format for training"""
        with open(output_file, 'w') as f:
            for pair in pairs:
                f.write(json.dumps(pair) + '\n')
```

---

## Fine-tuning Methods

### Option 1: LoRA (Recommended for Most Cases)

**Advantages:**
- ✅ Parameter-efficient (only ~1% of parameters)
- ✅ Fast training
- ✅ Can be merged or swapped
- ✅ Works on single GPU

```python
# train_lora.py
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, TaskType
import torch

# Load base model
model_name = "mistralai/Mistral-7B-Instruct-v0.2"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# LoRA configuration
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,  # LoRA rank
    lora_alpha=32,
    lora_dropout=0.1,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
)

# Apply LoRA
model = get_peft_model(model, lora_config)
print(f"Trainable parameters: {model.print_trainable_parameters()}")
```

### Option 2: QLoRA (For Limited GPU Memory)

**Advantages:**
- ✅ Even more memory-efficient
- ✅ 4-bit quantization
- ✅ Can train 70B models on 24GB GPU

```python
# train_qlora.py
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model
import torch

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

# Load quantized model
model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.2",
    quantization_config=bnb_config,
    device_map="auto"
)

# Apply LoRA
lora_config = LoraConfig(
    r=64,
    lora_alpha=128,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
```

### Option 3: Full Fine-tuning (Requires Significant Resources)

**Requirements:**
- 🔴 Multiple high-end GPUs
- 🔴 Large memory (200GB+ for 34B model)
- 🔴 Days of training time

Only recommended if you have extensive resources and data.

---

## Training Setup

### 1. Environment Setup

```bash
# Create training environment
python -m venv nhs-training-env
source nhs-training-env/bin/activate  # Linux/Mac
# nhs-training-env\Scripts\activate  # Windows

# Install dependencies
pip install torch transformers accelerate peft bitsandbytes
pip install datasets trl wandb  # Optional but recommended
```

### 2. Training Script

```python
# train_nhs_model.py
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
)
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, TaskType
import torch

def train_nhs_model():
    # Configuration
    model_name = "mistralai/Mistral-7B-Instruct-v0.2"
    dataset_path = "data/nhs_training_data.jsonl"
    output_dir = "models/nhs-medical-assistant"

    # Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    # LoRA configuration
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=16,
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    )

    model = get_peft_model(model, lora_config)

    # Load dataset
    dataset = load_dataset('json', data_files=dataset_path)

    def tokenize_function(examples):
        # Format: instruction + input + output
        texts = []
        for instruction, input_text, output in zip(
            examples['instruction'],
            examples['input'],
            examples['output']
        ):
            if input_text:
                prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n{output}"
            else:
                prompt = f"### Instruction:\n{instruction}\n\n### Response:\n{output}"
            texts.append(prompt)

        return tokenizer(
            texts,
            padding="max_length",
            truncation=True,
            max_length=2048
        )

    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=dataset["train"].column_names
    )

    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        fp16=True,
        save_steps=100,
        logging_steps=10,
        save_total_limit=3,
        warmup_steps=100,
        weight_decay=0.01,
        report_to="wandb",  # Optional: for experiment tracking
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        tokenizer=tokenizer,
    )

    # Train
    trainer.train()

    # Save final model
    model.save_pretrained(f"{output_dir}/final")
    tokenizer.save_pretrained(f"{output_dir}/final")

if __name__ == "__main__":
    train_nhs_model()
```

### 3. Run Training

```bash
# Single GPU
python train_nhs_model.py

# Multi-GPU with accelerate
accelerate config  # One-time setup
accelerate launch train_nhs_model.py

# With specific GPU
CUDA_VISIBLE_DEVICES=0 python train_nhs_model.py
```

### 4. Monitor Training

```bash
# Install tensorboard
pip install tensorboard

# View training progress
tensorboard --logdir=models/nhs-medical-assistant/runs
```

---

## Evaluation

### 1. Evaluation Script

```python
# evaluate_nhs_model.py
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch
import json

def evaluate_model(model_path, test_data_path):
    # Load model
    base_model = AutoModelForCausalLM.from_pretrained(
        "mistralai/Mistral-7B-Instruct-v0.2",
        torch_dtype=torch.float16,
        device_map="auto"
    )
    model = PeftModel.from_pretrained(base_model, model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # Load test data
    with open(test_data_path, 'r') as f:
        test_cases = [json.loads(line) for line in f]

    # Evaluate
    results = []
    for case in test_cases:
        prompt = f"### Instruction:\n{case['instruction']}\n\n### Response:\n"

        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
        outputs = model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.7,
            do_sample=True
        )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        results.append({
            "instruction": case['instruction'],
            "expected": case['output'],
            "generated": response
        })

    return results

# Run evaluation
results = evaluate_model(
    "models/nhs-medical-assistant/final",
    "data/nhs_test_data.jsonl"
)

# Save results
with open("evaluation_results.json", 'w') as f:
    json.dump(results, f, indent=2)
```

### 2. Medical Accuracy Evaluation

Create a test set with verified answers:

```python
# Test clinical knowledge
test_cases = [
    {
        "instruction": "What is the first-line treatment for hypertension in a 45-year-old patient?",
        "expected_keywords": ["ACE inhibitor", "lifestyle", "NICE guidelines"]
    },
    {
        "instruction": "List the components needed for a chest drain insertion",
        "expected_keywords": ["chest drain", "local anaesthetic", "suture", "drainage bottle"]
    }
]

def evaluate_medical_accuracy(results, test_cases):
    scores = []
    for result, test in zip(results, test_cases):
        # Check if expected keywords are in response
        keywords_found = sum(
            1 for kw in test['expected_keywords']
            if kw.lower() in result['generated'].lower()
        )
        accuracy = keywords_found / len(test['expected_keywords'])
        scores.append(accuracy)

    return sum(scores) / len(scores)
```

---

## Deployment

### 1. Export Fine-tuned Model

```python
# export_model.py
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Load LoRA model
base_model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.2",
    device_map="auto"
)
model = PeftModel.from_pretrained(
    base_model,
    "models/nhs-medical-assistant/final"
)

# Merge LoRA weights into base model
model = model.merge_and_unload()

# Save merged model
model.save_pretrained("models/nhs-medical-assistant-merged")
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
tokenizer.save_pretrained("models/nhs-medical-assistant-merged")
```

### 2. Deploy with vLLM

```bash
# Copy model to Kubernetes PVC
kubectl cp models/nhs-medical-assistant-merged \
  ai-assistant/vllm-models-pvc:/models/nhs-finetuned

# Deploy vLLM service (already configured in k8s/production/vllm-gpu.yaml)
kubectl apply -f k8s/production/vllm-gpu.yaml

# Verify deployment
kubectl logs -n ai-assistant -l app=vllm-nhs -f
```

### 3. Update Backend Configuration

```python
# services/backend/config.py
NHS_MODEL_ENDPOINT = "http://vllm-nhs:8000/v1"

# Route NHS-specific queries to NHS model
def get_llm_endpoint(query: str) -> str:
    if is_nhs_query(query):
        return NHS_MODEL_ENDPOINT
    return DEFAULT_MODEL_ENDPOINT

def is_nhs_query(query: str) -> bool:
    nhs_keywords = [
        "patient", "clinical", "treatment", "diagnosis",
        "equipment", "medical device", "NHS", "NICE"
    ]
    return any(kw in query.lower() for kw in nhs_keywords)
```

---

## Training Resources Required

### Local Training (LoRA)
```
Single NVIDIA RTX 4090 (24GB):
- Model: Mistral 7B with LoRA
- Batch size: 4
- Training time: 6-12 hours (1000 examples)
- Memory: ~18GB

Single NVIDIA A100 (40GB):
- Model: Llama-2-13B with LoRA
- Batch size: 8
- Training time: 8-16 hours (1000 examples)
- Memory: ~32GB
```

### Production Training (Full/LoRA)
```
2x NVIDIA A100 (80GB):
- Model: CodeLlama 34B with LoRA
- Batch size: 16 (total across GPUs)
- Training time: 24-48 hours (10,000 examples)
- Memory: ~60GB per GPU
```

---

## Sample Training Dataset Structure

```
nhs-training-data/
├── clinical_guidelines/
│   ├── cardiology.jsonl
│   ├── respiratory.jsonl
│   └── emergency.jsonl
├── equipment_manuals/
│   ├── imaging_equipment.jsonl
│   ├── monitoring_devices.jsonl
│   └── life_support.jsonl
├── procedures/
│   ├── surgical_procedures.jsonl
│   └── diagnostic_procedures.jsonl
└── metadata.json
```

---

## Continuous Improvement

### 1. Collect User Feedback

```python
# Implement feedback collection in backend
@app.post("/api/feedback")
async def collect_feedback(
    session_id: str,
    message_id: str,
    rating: int,  # 1-5
    feedback: str
):
    # Store feedback for model improvement
    # Can be used to identify failure cases
    pass
```

### 2. Regular Retraining

Schedule periodic retraining with updated data:
- Monthly: Review feedback and add new examples
- Quarterly: Full retraining with expanded dataset
- Yearly: Consider upgrading base model

---

## Compliance and Audit

### 1. Model Cards

Create a model card documenting:
- Training data sources
- Intended use cases
- Known limitations
- Evaluation results
- Bias testing results

### 2. Audit Trail

Log all training runs:
```python
training_metadata = {
    "model_version": "nhs-assistant-v1.0",
    "base_model": "mistralai/Mistral-7B-Instruct-v0.2",
    "training_date": "2026-01-10",
    "data_sources": ["NICE guidelines", "equipment manuals"],
    "num_examples": 5000,
    "evaluation_accuracy": 0.87,
    "approver": "NHS Information Governance",
    "approval_date": "2026-01-15"
}
```

---

## Next Steps

1. ✅ Understand fine-tuning process
2. 📊 **Collect and preprocess NHS data** (with IG approval)
3. 🔧 **Train LoRA model** on desktop GPU
4. 📈 **Evaluate model accuracy**
5. 🚀 **Deploy to production** Kubernetes cluster
6. 🔄 **Set up feedback loop** for continuous improvement

---

## Resources

- **Hugging Face PEFT**: https://github.com/huggingface/peft
- **LoRA Paper**: https://arxiv.org/abs/2106.09685
- **Medical NLP Resources**: https://github.com/topics/medical-nlp
- **NHS Digital Standards**: https://digital.nhs.uk/
- **NICE Guidelines**: https://www.nice.org.uk/guidance
