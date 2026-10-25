"""
Model Accuracy Test & Evaluation Suite for Autonomic Fatigue Detection.

Generates:
1. Epoch-by-epoch Learning Curves:
   - Training Loss vs Validation Loss ('loss' vs 'val_loss')
   - Training Accuracy vs Validation Accuracy ('accuracy' vs 'val_accuracy')
2. Confusion Matrix Heatmap (GREEN, YELLOW, RED)
3. Multi-Class ROC Curves with AUC per class
4. Per-Subject Generalization Analysis across 15 WESAD subjects
5. Comprehensive Accuracy Metrics Report (JSON + Terminal Dashboard)
"""

import os
import sys
import json
import argparse
from typing import Dict, Any, Tuple, List

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Headless backend
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GroupKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_curve,
    auc,
    classification_report,
)
from sklearn.preprocessing import label_binarize
from xgboost import XGBClassifier
import joblib

# Paths
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BACKEND_DIR, "data", "wesad_extracted_features.csv")
REPORTS_DIR = os.path.join(BACKEND_DIR, "reports")

FEATURE_NAMES = [
    "hr_mean",
    "hr_std",
    "rr_mean",
    "sdnn",
    "rmssd",
    "pnn50",
    "pnn20",
    "cv_rr",
    "sd1",
    "sd2",
    "sd1_sd2_ratio",
    "stress_index",
    "lf_power",
    "hf_power",
    "lf_hf_ratio",
    "total_power",
    "perfusion_index",
    "pulse_rise_time_ms",
]

CLASS_NAMES = ["GREEN", "YELLOW", "RED"]
CLASS_LABELS = {
    0: "GREEN (Rested / High HRV)",
    1: "YELLOW (Moderate Strain / Mild Depletion)",
    2: "RED (Exhaustion / Acute Stress)",
}


def load_dataset(csv_path: str = DATA_PATH) -> pd.DataFrame:
    if not os.path.exists(csv_path):
        # Check root
        root_path = os.path.join(os.path.dirname(BACKEND_DIR), "recovery_backend", "data", "wesad_extracted_features.csv")
        if os.path.exists(root_path):
            csv_path = root_path
        else:
            raise FileNotFoundError(f"Feature dataset not found at {csv_path}. Please run train_fatigue_model.py first.")
    
    df = pd.read_csv(csv_path)
    return df


def run_accuracy_test(
    df: pd.DataFrame,
    n_epochs: int = 150,
    learning_rate: float = 0.05,
    max_depth: int = 5,
    test_size: float = 0.20,
    random_state: int = 42,
    output_dir: str = REPORTS_DIR,
) -> Dict[str, Any]:
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "=" * 75)
    print("      ACTIVE RECOVERY SUITE - MODEL ACCURACY EVALUATION TEST      ")
    print("=" * 75)
    print(f"[Dataset] Total samples: {len(df)} across {df['subject'].nunique()} WESAD subjects")
    print(f"[Configuration] Iterations/Epochs: {n_epochs} | Learning Rate: {learning_rate} | Max Depth: {max_depth}")

    X = df[FEATURE_NAMES].values.astype(np.float32)
    y = df["target"].values.astype(int)
    subjects = df["subject"].values

    # Preprocessing: Sanitize any infs
    col_medians = np.nanmedian(X, axis=0)
    for i in range(X.shape[1]):
        mask = np.isnan(X[:, i]) | np.isinf(X[:, i])
        X[mask, i] = col_medians[i]

    # Stratified Train/Validation split
    X_train, X_val, y_train, y_val, subj_train, subj_val = train_test_split(
        X, y, subjects, test_size=test_size, random_state=random_state, stratify=y
    )

    # Standardize features (strictly fit on train)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)

    # Instantiate XGBoost with multi:softprob and multi-metric tracking
    eval_set = [(X_train_scaled, y_train), (X_val_scaled, y_val)]
    model = XGBClassifier(
        n_estimators=n_epochs,
        max_depth=max_depth,
        learning_rate=learning_rate,
        subsample=0.85,
        colsample_bytree=0.85,
        objective="multi:softprob",
        num_class=3,
        eval_metric=["mlogloss", "merror"],
        random_state=random_state,
        n_jobs=-1,
    )

    print(f"\n[Training] Training model with per-iteration evaluation tracking...")
    model.fit(
        X_train_scaled,
        y_train,
        eval_set=eval_set,
        verbose=False,
    )

    # Extract iteration history
    results = model.evals_result()
    train_loss = results["validation_0"]["mlogloss"]
    val_loss = results["validation_1"]["mlogloss"]
    train_merror = results["validation_0"]["merror"]
    val_merror = results["validation_1"]["merror"]

    # Convert error to accuracy: accuracy = 1 - error
    train_acc = [1.0 - err for err in train_merror]
    val_acc = [1.0 - err for err in val_merror]
    epochs = list(range(1, len(train_loss) + 1))

    # Evaluate Final Predictions on Validation Set
    val_preds = model.predict(X_val_scaled)
    val_probs = model.predict_proba(X_val_scaled)

    final_acc = accuracy_score(y_val, val_preds)
    final_macro_f1 = f1_score(y_val, val_preds, average="macro")
    final_weighted_f1 = f1_score(y_val, val_preds, average="weighted")
    final_prec = precision_score(y_val, val_preds, average="macro")
    final_rec = recall_score(y_val, val_preds, average="macro")

    # One-vs-Rest AUC
    y_val_bin = label_binarize(y_val, classes=[0, 1, 2])
    fpr, tpr, roc_auc_dict = {}, {}, {}
    for i in range(3):
        fpr[i], tpr[i], _ = roc_curve(y_val_bin[:, i], val_probs[:, i])
        roc_auc_dict[CLASS_NAMES[i]] = float(auc(fpr[i], tpr[i]))
    macro_auc = float(np.mean(list(roc_auc_dict.values())))

    cm = confusion_matrix(y_val, val_preds, labels=[0, 1, 2])
    clf_report = classification_report(
        y_val, val_preds, target_names=CLASS_NAMES, output_dict=True
    )

    # ----------------------------------------------------
    # PLOT 1: LEARNING CURVES (LOSS & ACCURACY) - MATCHES SCREENSHOT
    # ----------------------------------------------------
    print(f"[Plotting] Generating evaluation learning curves (Loss & Accuracy)...")
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, (ax_acc, ax_loss) = plt.subplots(1, 2, figsize=(14, 5), dpi=300)

    # Panel 1: Accuracy vs Val Accuracy
    ax_acc.plot(epochs, train_acc, label="accuracy", color="#1f77b4", linewidth=2.0)
    ax_acc.plot(epochs, val_acc, label="val_accuracy", color="#ff7f0e", linewidth=2.0)
    ax_acc.set_title("Training and Validation Accuracy", fontsize=14, fontweight="bold", pad=12)
    ax_acc.set_xlabel("Epoch / Iteration", fontsize=12)
    ax_acc.set_ylabel("Accuracy", fontsize=12)
    ax_acc.set_ylim([0.45, 1.02])
    ax_acc.grid(True, linestyle="--", alpha=0.5)
    ax_acc.legend(loc="lower right", frameon=True, fontsize=11)

    # Highlight peak val accuracy
    best_epoch = int(np.argmax(val_acc)) + 1
    best_val_acc = float(np.max(val_acc))
    ax_acc.scatter([best_epoch], [best_val_acc], color="#2ca02c", s=70, zorder=5)
    ax_acc.annotate(
        f"Peak Val Acc: {best_val_acc * 100:.1f}%\n(Epoch {best_epoch})",
        xy=(best_epoch, best_val_acc),
        xytext=(best_epoch - 35, best_val_acc - 0.08),
        arrowprops=dict(facecolor="#2ca02c", shrink=0.05, width=1.5, headwidth=6),
        fontsize=10,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#e8f5e9", edgecolor="#2ca02c", alpha=0.9),
    )

    # Panel 2: Loss vs Val Loss
    ax_loss.plot(epochs, train_loss, label="loss", color="#1f77b4", linewidth=2.0)
    ax_loss.plot(epochs, val_loss, label="val_loss", color="#ff7f0e", linewidth=2.0)
    ax_loss.set_title("Training and Validation Loss", fontsize=14, fontweight="bold", pad=12)
    ax_loss.set_xlabel("Epoch / Iteration", fontsize=12)
    ax_loss.set_ylabel("Loss (Multi-class Log-Loss)", fontsize=12)
    ax_loss.set_ylim([0.0, max(max(train_loss), max(val_loss)) * 1.1])
    ax_loss.grid(True, linestyle="--", alpha=0.5)
    ax_loss.legend(loc="upper right", frameon=True, fontsize=11)

    min_loss_epoch = int(np.argmin(val_loss)) + 1
    min_val_loss = float(np.min(val_loss))
    ax_loss.scatter([min_loss_epoch], [min_val_loss], color="#d62728", s=70, zorder=5)
    ax_loss.annotate(
        f"Min Val Loss: {min_val_loss:.3f}\n(Epoch {min_loss_epoch})",
        xy=(min_loss_epoch, min_val_loss),
        xytext=(min_loss_epoch + 10, min_val_loss + 0.15),
        arrowprops=dict(facecolor="#d62728", shrink=0.05, width=1.5, headwidth=6),
        fontsize=10,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffebee", edgecolor="#d62728", alpha=0.9),
    )

    plt.tight_layout()
    curves_path = os.path.join(output_dir, "evaluation_curves.png")
    plt.savefig(curves_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  -> Saved Learning Curves to: {curves_path}")

    # ----------------------------------------------------
    # PLOT 2: CONFUSION MATRIX HEATMAP
    # ----------------------------------------------------
    fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
    cm_percent = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis] * 100.0
    labels = np.asarray([
        f"{count}\n({pct:.1f}%)" for count, pct in zip(cm.flatten(), cm_percent.flatten())
    ]).reshape(3, 3)

    sns.heatmap(
        cm_percent,
        annot=labels,
        fmt="",
        cmap="Blues",
        cbar=True,
        xticklabels=CLASS_NAMES,
        yticklabels=CLASS_NAMES,
        ax=ax,
        annot_kws={"fontsize": 12, "fontweight": "bold"},
    )
    ax.set_title("Fatigue Classification Confusion Matrix", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Predicted Autonomic Tier", fontsize=11, fontweight="bold")
    ax.set_ylabel("True Condition State", fontsize=11, fontweight="bold")
    plt.tight_layout()
    cm_path = os.path.join(output_dir, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  -> Saved Confusion Matrix to: {cm_path}")

    # ----------------------------------------------------
    # PLOT 3: MULTI-CLASS ROC CURVES
    # ----------------------------------------------------
    fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
    colors = ["#2ca02c", "#ff7f0e", "#d62728"]
    for i in range(3):
        ax.plot(
            fpr[i],
            tpr[i],
            color=colors[i],
            lw=2.5,
            label=f"{CLASS_NAMES[i]} (AUC = {roc_auc_dict[CLASS_NAMES[i]]:.3f})",
        )
    ax.plot([0, 1], [0, 1], "k--", lw=1.5, alpha=0.6, label="Chance Level (AUC = 0.500)")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel("False Positive Rate (1 - Specificity)", fontsize=11)
    ax.set_ylabel("True Positive Rate (Sensitivity)", fontsize=11)
    ax.set_title(f"Multi-Class ROC Curves (Macro AUC = {macro_auc:.3f})", fontsize=13, fontweight="bold", pad=12)
    ax.legend(loc="lower right", frameon=True, fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    roc_path = os.path.join(output_dir, "roc_curves.png")
    plt.savefig(roc_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  -> Saved ROC Curves to: {roc_path}")

    # ----------------------------------------------------
    # PLOT 4: PER-SUBJECT GENERALIZATION BREAKDOWN
    # ----------------------------------------------------
    print(f"[Validation] Evaluating per-subject generalization across 15 WESAD subjects...")
    gkf = GroupKFold(n_splits=5)
    subject_accs = {}
    for fold, (train_idx, test_idx) in enumerate(gkf.split(X, y, groups=subjects), 1):
        X_tr, X_te = X[train_idx], X[test_idx]
        y_tr, y_te = y[train_idx], y[test_idx]
        test_subjs = subjects[test_idx]
        
        sc = StandardScaler()
        X_tr_sc = sc.fit_transform(X_tr)
        X_te_sc = sc.transform(X_te)
        
        clf = XGBClassifier(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.06,
            objective="multi:softprob",
            num_class=3,
            random_state=42,
            n_jobs=-1,
        )
        clf.fit(X_tr_sc, y_tr)
        preds = clf.predict(X_te_sc)
        
        for subj in np.unique(test_subjs):
            mask = test_subjs == subj
            subj_acc = float(accuracy_score(y_te[mask], preds[mask]))
            subject_accs[subj] = round(subj_acc * 100.0, 1)

    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    sorted_subjs = sorted(subject_accs.keys(), key=lambda s: int(s[1:]) if s[1:].isdigit() else s)
    acc_vals = [subject_accs[s] for s in sorted_subjs]
    mean_val = float(np.mean(acc_vals))

    bars = ax.bar(sorted_subjs, acc_vals, color="#3b82f6", edgecolor="#1d4ed8", alpha=0.85, width=0.6)
    ax.axhline(mean_val, color="#ef4444", linestyle="--", linewidth=2.0, label=f"Mean Subject Accuracy: {mean_val:.1f}%")
    ax.set_ylim([0, 105])
    ax.set_xlabel("WESAD Subject ID", fontsize=11, fontweight="bold")
    ax.set_ylabel("Classification Accuracy (%)", fontsize=11, fontweight="bold")
    ax.set_title("Cross-Subject Generalization Accuracy (GroupKFold Zero Leakage)", fontsize=13, fontweight="bold", pad=12)
    ax.legend(loc="lower right", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.4, axis="y")

    for bar, val in zip(bars, acc_vals):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval + 1.5, f"{val:.0f}%", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    plt.tight_layout()
    subj_path = os.path.join(output_dir, "subject_generalization.png")
    plt.savefig(subj_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  -> Saved Subject Generalization Chart to: {subj_path}")

    # Compile JSON Report
    report_dict = {
        "summary": {
            "overall_accuracy": round(final_acc * 100.0, 2),
            "macro_f1_score": round(final_macro_f1, 4),
            "weighted_f1_score": round(final_weighted_f1, 4),
            "macro_precision": round(final_prec, 4),
            "macro_recall": round(final_rec, 4),
            "macro_roc_auc": round(macro_auc, 4),
            "peak_val_accuracy": round(best_val_acc * 100.0, 2),
            "peak_val_epoch": best_epoch,
            "min_val_loss": round(min_val_loss, 4),
            "min_loss_epoch": min_loss_epoch,
        },
        "per_class_metrics": {
            "GREEN": {
                "precision": round(clf_report["GREEN"]["precision"], 4),
                "recall": round(clf_report["GREEN"]["recall"], 4),
                "f1_score": round(clf_report["GREEN"]["f1-score"], 4),
                "roc_auc": roc_auc_dict["GREEN"],
                "support": int(clf_report["GREEN"]["support"]),
            },
            "YELLOW": {
                "precision": round(clf_report["YELLOW"]["precision"], 4),
                "recall": round(clf_report["YELLOW"]["recall"], 4),
                "f1_score": round(clf_report["YELLOW"]["f1-score"], 4),
                "roc_auc": roc_auc_dict["YELLOW"],
                "support": int(clf_report["YELLOW"]["support"]),
            },
            "RED": {
                "precision": round(clf_report["RED"]["precision"], 4),
                "recall": round(clf_report["RED"]["recall"], 4),
                "f1_score": round(clf_report["RED"]["f1-score"], 4),
                "roc_auc": roc_auc_dict["RED"],
                "support": int(clf_report["RED"]["support"]),
            },
        },
        "subject_generalization": subject_accs,
        "plots_generated": {
            "learning_curves": curves_path,
            "confusion_matrix": cm_path,
            "roc_curves": roc_path,
            "subject_generalization": subj_path,
        },
    }

    report_json_path = os.path.join(output_dir, "accuracy_test_report.json")
    with open(report_json_path, "w") as f:
        json.dump(report_dict, f, indent=2)
    print(f"  -> Saved Full Metrics Report to: {report_json_path}")

    # Print Terminal Dashboard
    print("\n" + "=" * 75)
    print("                    ACCURACY TEST RESULTS SUMMARY                    ")
    print("=" * 75)
    print(f"  Overall Validation Accuracy:  {final_acc * 100:.2f}% (Peak: {best_val_acc * 100:.2f}% @ Epoch {best_epoch})")
    print(f"  Macro F1-Score:               {final_macro_f1:.4f}")
    print(f"  Macro ROC-AUC:                {macro_auc:.4f}")
    print(f"  Min Validation Loss:          {min_val_loss:.4f} (Epoch {min_loss_epoch})")
    print("-" * 75)
    print("  Tier Breakdown:")
    for tier in CLASS_NAMES:
        m = report_dict["per_class_metrics"][tier]
        print(f"    • {tier:6s} | Precision: {m['precision']:.3f} | Recall: {m['recall']:.3f} | F1: {m['f1_score']:.3f} | AUC: {m['roc_auc']:.3f} | Support: {m['support']}")
    print("=" * 75)

    return report_dict


def main():
    parser = argparse.ArgumentParser(description="Autonomic Fatigue Model Accuracy Test Suite")
    parser.add_argument("--data-file", type=str, default=DATA_PATH, help="Path to extracted features CSV")
    parser.add_argument("--epochs", type=int, default=140, help="Number of training iterations/epochs (default: 140)")
    parser.add_argument("--lr", type=float, default=0.05, help="Learning rate (default: 0.05)")
    parser.add_argument("--depth", type=int, default=5, help="Max tree depth (default: 5)")
    parser.add_argument("--output-dir", type=str, default=REPORTS_DIR, help="Directory to save evaluation plots")
    args = parser.parse_args()

    df = load_dataset(args.data_file)
    run_accuracy_test(
        df=df,
        n_epochs=args.epochs,
        learning_rate=args.lr,
        max_depth=args.depth,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
