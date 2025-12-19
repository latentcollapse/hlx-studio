#!/usr/bin/env python3
"""
2-Phase Training Script for HLX Specialists
Phase 1: General foundation (50-100 epochs)
Phase 2: Deep specialization (200-300 epochs)
"""

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
import os
import sys
import json
import time
from pathlib import Path

# ============================================================================
# Configuration
# ============================================================================

if len(sys.argv) < 2:
    print("Usage: python3 train_2phase_specialist.py [ascii|runic]")
    sys.exit(1)

specialist_type = sys.argv[1]  # 'ascii' or 'runic'

if specialist_type not in ['ascii', 'runic']:
    print("Error: specialist must be 'ascii' or 'runic'")
    sys.exit(1)

# Paths
phase1_corpus = "corpus_phase1_general.jsonl"
phase2_corpus = f"corpus_phase2_{specialist_type}_specialist.jsonl"
output_dir = f"/home/matt/hlx-dev-studio/models/qwen3_1_7b_{specialist_type}_specialist"
final_model_path = f"{output_dir}/final_model"
phase1_checkpoint = f"{output_dir}/phase1_checkpoint"
metrics_file = f"{output_dir}/training_metrics.jsonl"

# Training config
phase1_epochs = 75  # 50-100 range
phase2_epochs = 250  # 200-300 range

print("="*80)
print(f"2-Phase Training: {specialist_type.upper()} Specialist")
print("="*80)
print(f"Phase 1: {phase1_epochs} epochs on general HLX foundation")
print(f"Phase 2: {phase2_epochs} epochs on {specialist_type} specialization")
print("="*80)

# ============================================================================
# Load Base Model
# ============================================================================

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

print("\nLoading Qwen3-1.7B base model in 4-bit...")
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-1.7B",
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

tokenizer = AutoTokenizer.from_pretrained(
    "Qwen/Qwen3-1.7B",
    trust_remote_code=True
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print("✓ Model loaded")

# Prepare for training
model.gradient_checkpointing_enable()
model = prepare_model_for_kbit_training(model)

# LoRA config
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
total_params = sum(p.numel() for p in model.parameters())
print(f"Trainable parameters: {trainable_params:,} ({100*trainable_params/total_params:.2f}%)")

# ============================================================================
# Tokenization Function
# ============================================================================

def tokenize_function(examples):
    inputs = [inp + out for inp, out in zip(examples['input'], examples['output'])]
    model_inputs = tokenizer(
        inputs,
        max_length=384,
        truncation=True,
        padding="max_length"
    )
    model_inputs["labels"] = model_inputs["input_ids"].copy()
    return model_inputs

# ============================================================================
# Metrics Logging
# ============================================================================

def log_metrics(phase, epoch, metrics):
    """Log training metrics to file"""
    os.makedirs(output_dir, exist_ok=True)
    entry = {
        "phase": phase,
        "epoch": epoch,
        "timestamp": time.time(),
        **metrics
    }
    with open(metrics_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')

# ============================================================================
# PHASE 1: General HLX Foundation
# ============================================================================

print("\n" + "="*80)
print("PHASE 1: General HLX Foundation Training")
print("="*80)

print(f"\nLoading Phase 1 corpus: {phase1_corpus}")
dataset_phase1 = load_dataset('json', data_files=phase1_corpus, split='train')
print(f"Loaded {len(dataset_phase1)} examples")

tokenized_phase1 = dataset_phase1.map(tokenize_function, batched=True, remove_columns=dataset_phase1.column_names)

training_args_phase1 = TrainingArguments(
    output_dir=f"{output_dir}/phase1",
    num_train_epochs=phase1_epochs,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.1,
    logging_steps=5,
    save_strategy="epoch",
    save_steps=10,
    save_total_limit=2,
    fp16=True,
    optim="paged_adamw_8bit",
    gradient_checkpointing=True,
    gradient_checkpointing_kwargs={"use_reentrant": False},
    max_grad_norm=0.3,
    weight_decay=0.01,
    report_to="none",
    dataloader_num_workers=0,
)

trainer_phase1 = Trainer(
    model=model,
    args=training_args_phase1,
    train_dataset=tokenized_phase1,
    tokenizer=tokenizer
)

print("\n" + "="*80)
print("Starting Phase 1 Training...")
print("="*80 + "\n")

start_time = time.time()

try:
    train_result = trainer_phase1.train()
    phase1_time = time.time() - start_time

    print(f"\nPhase 1 Complete! Time: {phase1_time/60:.1f} minutes")

    # Save Phase 1 checkpoint
    print(f"Saving Phase 1 checkpoint to: {phase1_checkpoint}")
    os.makedirs(phase1_checkpoint, exist_ok=True)
    model.save_pretrained(phase1_checkpoint)
    tokenizer.save_pretrained(phase1_checkpoint)

    log_metrics("phase1", phase1_epochs, {
        "loss": train_result.training_loss,
        "time_minutes": phase1_time/60
    })

except Exception as e:
    print(f"\n❌ Phase 1 Training Failed: {e}")
    sys.exit(1)

# ============================================================================
# PHASE 2: Deep Specialization
# ============================================================================

print("\n" + "="*80)
print(f"PHASE 2: {specialist_type.upper()} Specialization Training")
print("="*80)

print(f"\nLoading Phase 2 corpus: {phase2_corpus}")
dataset_phase2 = load_dataset('json', data_files=phase2_corpus, split='train')
print(f"Loaded {len(dataset_phase2)} examples")

tokenized_phase2 = dataset_phase2.map(tokenize_function, batched=True, remove_columns=dataset_phase2.column_names)

training_args_phase2 = TrainingArguments(
    output_dir=f"{output_dir}/phase2",
    num_train_epochs=phase2_epochs,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=1e-4,  # Lower LR for fine-tuning
    lr_scheduler_type="cosine",
    warmup_ratio=0.05,  # Less warmup
    logging_steps=5,
    save_strategy="epoch",
    save_steps=25,
    save_total_limit=2,
    fp16=True,
    optim="paged_adamw_8bit",
    gradient_checkpointing=True,
    gradient_checkpointing_kwargs={"use_reentrant": False},
    max_grad_norm=0.3,
    weight_decay=0.01,
    report_to="none",
    dataloader_num_workers=0,
)

trainer_phase2 = Trainer(
    model=model,
    args=training_args_phase2,
    train_dataset=tokenized_phase2,
    tokenizer=tokenizer
)

print("\n" + "="*80)
print("Starting Phase 2 Training...")
print("="*80 + "\n")

start_time = time.time()

try:
    train_result = trainer_phase2.train()
    phase2_time = time.time() - start_time

    print(f"\nPhase 2 Complete! Time: {phase2_time/60:.1f} minutes")

    # Save final model
    print(f"Saving final model to: {final_model_path}")
    os.makedirs(final_model_path, exist_ok=True)
    model.save_pretrained(final_model_path)
    tokenizer.save_pretrained(final_model_path)

    log_metrics("phase2", phase2_epochs, {
        "loss": train_result.training_loss,
        "time_minutes": phase2_time/60
    })

    print("\n" + "="*80)
    print(f"{specialist_type.upper()} Specialist Training Complete!")
    print("="*80)
    print(f"Phase 1: {phase1_time/60:.1f} minutes")
    print(f"Phase 2: {phase2_time/60:.1f} minutes")
    print(f"Total: {(phase1_time + phase2_time)/60:.1f} minutes")
    print(f"Final model: {final_model_path}")
    print("="*80)

except Exception as e:
    print(f"\n❌ Phase 2 Training Failed: {e}")
    print(f"Phase 1 checkpoint saved at: {phase1_checkpoint}")
    sys.exit(1)
