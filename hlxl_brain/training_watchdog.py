#!/usr/bin/env python3
"""
Training Watchdog Monitor
Monitors training progress and alerts on failures.

Usage:
    # In one terminal, start training:
    python3 train_100m_production.py --phase 1 --epochs 200

    # In another terminal, start watchdog:
    python3 training_watchdog.py --check-interval 60

The watchdog will:
- Monitor training_status.json every 60 seconds
- Alert if training stalls
- Alert if loss diverges
- Alert if quality gates fail
- Provide ETA updates
"""

import argparse
import json
import time
import sys
from pathlib import Path
from datetime import datetime, timedelta


class TrainingWatchdog:
    """Monitors training and alerts on failures."""

    def __init__(self, status_file: str = "training_status.json", check_interval: int = 60):
        self.status_file = status_file
        self.check_interval = check_interval
        self.last_epoch = 0
        self.last_check_time = time.time()
        self.stall_count = 0
        self.running = True

    def load_status(self):
        """Load current training status."""
        if not Path(self.status_file).exists():
            return None

        try:
            with open(self.status_file, "r") as f:
                return json.load(f)
        except:
            return None

    def format_time(self, seconds):
        """Format seconds to human-readable time."""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}m"
        else:
            return f"{seconds/3600:.1f}h"

    def check_status(self):
        """Check training status and alert on issues."""
        status = self.load_status()

        if status is None:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ⏳ Waiting for training to start...")
            return True

        timestamp = datetime.fromisoformat(status["timestamp"].replace("Z", "+00:00"))
        epoch = status["epoch"]
        total_epochs = status["total_epochs"]
        train_loss = status["train_loss"]
        val_loss = status.get("val_loss")
        progress_pct = status["progress_pct"]
        eta_hours = status.get("eta_hours", 0)
        training_status = status.get("status", "training")

        # Status display
        print("\n" + "="*80)
        print(f"TRAINING WATCHDOG - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        print(f"Status: {training_status.upper()}")
        print(f"Progress: {epoch}/{total_epochs} epochs ({progress_pct:.1f}%)")
        print(f"Train Loss: {train_loss:.4f}")
        if val_loss:
            print(f"Val Loss: {val_loss:.4f}")
        print(f"ETA: {self.format_time(eta_hours * 3600)}")
        print(f"Last update: {(datetime.now() - timestamp.replace(tzinfo=None)).total_seconds():.0f}s ago")

        # Check for completed training
        if training_status == "completed":
            print("\n✓ TRAINING COMPLETED SUCCESSFULLY")
            print("="*80)
            return False  # Stop monitoring

        # Check for aborted training
        if training_status == "aborted":
            print("\n❌ TRAINING ABORTED")
            print("="*80)
            return False

        # Check for quality failure
        if training_status == "quality_failed":
            print("\n❌ TRAINING FAILED: Quality gate failure")
            print("="*80)
            return False

        # Check for stalled training (no progress in 5 minutes)
        time_since_update = (datetime.now() - timestamp.replace(tzinfo=None)).total_seconds()
        if time_since_update > 300:  # 5 minutes
            print(f"\n⚠ WARNING: Training may have stalled!")
            print(f"  Last update was {self.format_time(time_since_update)} ago")

        # Check if epoch advanced
        if epoch > self.last_epoch:
            self.last_epoch = epoch
            self.stall_count = 0
        elif epoch == self.last_epoch and time_since_update > 180:
            self.stall_count += 1
            if self.stall_count >= 3:
                print(f"\n❌ ALERT: Training appears stalled at epoch {epoch}")
                print(f"  No progress for {self.stall_count} checks ({self.stall_count * self.check_interval}s)")

        # Check for loss divergence
        if train_loss > 15.0:
            print(f"\n❌ ALERT: Training loss diverged ({train_loss:.4f})")

        # Check for suspiciously low loss
        if epoch < 10 and train_loss < 0.001:
            print(f"\n❌ ALERT: Loss collapsed too early (epoch {epoch}, loss {train_loss:.4f})")

        print("="*80)
        return True

    def run(self):
        """Main monitoring loop."""
        print("="*80)
        print("TRAINING WATCHDOG STARTED")
        print("="*80)
        print(f"Monitoring: {self.status_file}")
        print(f"Check interval: {self.check_interval}s")
        print("Press Ctrl+C to stop")
        print("="*80)

        try:
            while self.running:
                should_continue = self.check_status()

                if not should_continue:
                    break

                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            print("\n\n✓ Watchdog stopped by user")

        print("\n" + "="*80)
        print("WATCHDOG MONITORING ENDED")
        print("="*80)


def main():
    parser = argparse.ArgumentParser(description="Training watchdog monitor")
    parser.add_argument("--status-file", type=str, default="training_status.json",
                        help="Training status file to monitor")
    parser.add_argument("--check-interval", type=int, default=60,
                        help="Check interval in seconds (default: 60)")

    args = parser.parse_args()

    watchdog = TrainingWatchdog(
        status_file=args.status_file,
        check_interval=args.check_interval,
    )

    watchdog.run()


if __name__ == "__main__":
    main()
