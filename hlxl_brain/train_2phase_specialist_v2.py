#!/usr/bin/env python3
"""
2-Phase Training Script for HLX Specialists with Early Stopping
Phase 1: General foundation (50-100 epochs)
Phase 2: Deep specialization with early stopping to prevent overfitting
"""

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    TrainerCallback,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
import os
import sys
import json
import time
from pathlib import Path
import shutil

# ============================================================================
# Early Stopping Callback
# ============================================================================

class EarlyStoppingCallback(TrainerCallback):
    """
    Early stopping with checkpoint reversion to prevent overfitting.
    Monitors training loss and reverts to best checkpoint if no improvement.
    """
    def __init__(self, patience=10, min_delta=0.0001, checkpoint_dir=None):
        self.patience = patience  # Epochs without improvement before stopping
        self.min_delta = min_delta  # Minimum change to count as improvement
        self.best_loss = float('inf')
        self.best_checkpoint = None
        self.epochs_without_improvement = 0
        self.checkpoint_dir = checkpoint_dir
        self.stopped_epoch = None

    def on_epoch_end(self, args, state, control, **kwargs):
        """Check if we should stop and revert to best checkpoint"""
        current_loss = state.log_history[-1].get('loss', float('inf'))
        epoch = state.epoch

        # Check if this is an improvement
        if current_loss < (self.best_loss - self.min_delta):
            # New best! Save checkpoint
            improvement = self.best_loss - current_loss
            self.best_loss = current_loss
            self.epochs_without_improvement = 0

            # Save this checkpoint as best
            if self.checkpoint_dir:
                best_path = f"{self.checkpoint_dir}/best_checkpoint"
                if os.path.exists(best_path):
                    shutil.rmtree(best_path)

                # Save current model state
                model = kwargs.get('model')
                if model:
                    model.save_pretrained(best_path)
                    print(f"\n🎯 New best! Epoch {epoch:.1f}, Loss {current_loss:.4f} (↓{improvement:.4f})")
                    self.best_checkpoint = best_path
        else:
            # No improvement
            self.epochs_without_improvement += 1
            print(f"\n📊 Epoch {epoch:.1f}, Loss {current_loss:.4f} (no improvement for {self.epochs_without_improvement} epochs)")

        # Check if we should stop
        if self.epochs_without_improvement >= self.patience:
            print(f"\n⚠️  Early stopping triggered!")
            print(f"   No improvement for {self.patience} epochs")
            print(f"   Best loss: {self.best_loss:.4f} (epoch {epoch - self.patience:.1f})")
            print(f"   Current loss: {current_loss:.4f} (epoch {epoch:.1f})")
            print(f"   Performance degradation: {((current_loss - self.best_loss) / self.best_loss * 100):.2f}%")

            self.stopped_epoch = epoch
            control.should_training_stop = True

        return control

    def load_best_checkpoint(self, model):
        """Load the best checkpoint back into the model"""
        if self.best_checkpoint and os.path.exists(self.best_checkpoint):
            print(f"\n✅ Reverting to best checkpoint: {self.best_checkpoint}")
            print(f"   Best loss: {self.best_loss:.4f}")

            # Load best weights
            from peft import PeftModel
            model = PeftModel.from_pretrained(
                model.base_model.model,
                self.best_checkpoint
            )
            return model
        else:
            print(f"\n⚠️  No best checkpoint found, keeping current model")
            return model

# ============================================================================
# Configuration
# ============================================================================

if len(sys.argv) < 2:
    print("Usage: python3 train_2phase_specialist_v2.py [ascii|runic]")
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
phase2_epochs = 250  # Maximum - will stop early if overfitting

# Early stopping config
early_stopping_patience = 10  # Stop if no improvement for 10 epochs
early_stopping_min_delta = 0.0001  # Minimum improvement threshold

print("="*80)
print(f"2-Phase Training: {specialist_type.upper()} Specialist (with Early Stopping)")
print("="*80)
print(f"Phase 1: {phase1_epochs} epochs on general HLX foundation")
print(f"Phase 2: Up to {phase2_epochs} epochs on {specialist_type} specialization")
print(f"Early Stopping: Patience={early_stopping_patience}, Min Delta={early_stopping_min_delta}")
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
# PHASE 2: Deep Specialization with Early Stopping
# ============================================================================

print("\n" + "="*80)
print(f"PHASE 2: {specialist_type.upper()} Specialization Training (with Early Stopping)")
print("="*80)

print(f"\nLoading Phase 2 corpus: {phase2_corpus}")
dataset_phase2 = load_dataset('json', data_files=phase2_corpus, split='train')
print(f"Loaded {len(dataset_phase2)} examples")

tokenized_phase2 = dataset_phase2.map(tokenize_function, batched=True, remove_columns=dataset_phase2.column_names)

# Create early stopping callback
early_stopping_callback = EarlyStoppingCallback(
    patience=early_stopping_patience,
    min_delta=early_stopping_min_delta,
    checkpoint_dir=f"{output_dir}/phase2"
)

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
    save_steps=5,  # Save more frequently for early stopping
    save_total_limit=3,  # Keep more checkpoints
    fp16=True,
    optim="paged_adamw_8bit",
    gradient_checkpointing=True,
    gradient_checkpointing_kwargs={"use_reentrant": False},
    max_grad_norm=0.3,
    weight_decay=0.01,
    report_to="none",
    dataloader_num_workers=0,
    load_best_model_at_end=False,  # We handle this manually
)

trainer_phase2 = Trainer(
    model=model,
    args=training_args_phase2,
    train_dataset=tokenized_phase2,
    tokenizer=tokenizer,
    callbacks=[early_stopping_callback]
)

print("\n" + "="*80)
print("Starting Phase 2 Training...")
print(f"Will stop early if no improvement for {early_stopping_patience} epochs")
print("="*80 + "\n")

start_time = time.time()

try:
    train_result = trainer_phase2.train()
    phase2_time = time.time() - start_time

    # Revert to best checkpoint
    print("\n" + "="*80)
    print("Training Complete - Loading Best Checkpoint")
    print("="*80)

    model = early_stopping_callback.load_best_checkpoint(model)

    print(f"\nPhase 2 Complete! Time: {phase2_time/60:.1f} minutes")
    if early_stopping_callback.stopped_epoch:
        print(f"Early stopping at epoch {early_stopping_callback.stopped_epoch:.1f}")
        print(f"Best loss: {early_stopping_callback.best_loss:.4f}")
        actual_epochs = early_stopping_callback.stopped_epoch - early_stopping_patience
        print(f"Actual optimal epochs: ~{actual_epochs:.0f}")

    # Save final model (with best checkpoint loaded)
    print(f"\nSaving final model to: {final_model_path}")
    os.makedirs(final_model_path, exist_ok=True)
    model.save_pretrained(final_model_path)
    tokenizer.save_pretrained(final_model_path)

    log_metrics("phase2", phase2_epochs, {
        "loss": early_stopping_callback.best_loss,
        "stopped_at_epoch": early_stopping_callback.stopped_epoch or phase2_epochs,
        "time_minutes": phase2_time/60
    })

    print("\n" + "="*80)
    print(f"{specialist_type.upper()} Specialist Training Complete!")
    print("="*80)
    print(f"Phase 1: {phase1_time/60:.1f} minutes")
    print(f"Phase 2: {phase2_time/60:.1f} minutes")
    print(f"Total: {(phase1_time + phase2_time)/60:.1f} minutes")
    print(f"Final model: {final_model_path}")
    print(f"Best loss achieved: {early_stopping_callback.best_loss:.4f}")
    print("="*80)

except Exception as e:
    print(f"\n❌ Phase 2 Training Failed: {e}")
    print(f"Phase 1 checkpoint saved at: {phase1_checkpoint}")
    sys.exit(1)
