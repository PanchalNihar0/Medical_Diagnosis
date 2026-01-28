"""
Train All Models Script.
Trains all disease models in sequence.
"""
import subprocess
import sys
from pathlib import Path


def main():
    """Train all disease models."""
    training_dir = Path(__file__).parent
    
    scripts = [
        "train_diabetes.py",
        "train_heart.py",
        "train_kidney.py",
        "train_liver.py",
        "train_breast_cancer.py",
        # Image models require separate GPU setup
        # "train_malaria.py",
        # "train_pneumonia.py",
    ]
    
    print("=" * 60)
    print("TRAINING ALL MODELS")
    print("=" * 60)
    
    results = {}
    
    for script in scripts:
        script_path = training_dir / script
        if script_path.exists():
            print(f"\n{'='*60}")
            print(f"Running {script}...")
            print("=" * 60)
            result = subprocess.run([sys.executable, str(script_path)], cwd=str(training_dir))
            results[script] = "SUCCESS" if result.returncode == 0 else "FAILED"
        else:
            print(f"Skipping {script} (not found)")
            results[script] = "SKIPPED"
    
    print("\n" + "=" * 60)
    print("TRAINING SUMMARY")
    print("=" * 60)
    for script, status in results.items():
        print(f"  {script}: {status}")
    print("=" * 60)


if __name__ == "__main__":
    main()
