"""
Root wrapper for Fatigue Model Accuracy Test & Evaluation Suite.
Delegates to recovery_backend/evaluate_model_accuracy.py.
"""
import os
import sys

backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recovery_backend")
sys.path.insert(0, backend_dir)

if __name__ == "__main__":
    from recovery_backend.evaluate_model_accuracy import main
    main()
