# Component 2 Presentation Slides: Active Recovery, Joint Health & Fatigue Management Suite

**Presenter:** IT23156838 | Rathnayake S  
**Specialization:** Software Engineering  
**Group:** J26-SE-342 | FullStrength PP1 Presentation  
**Component Title:** Active Recovery, Joint Health & Fatigue Management Suite  
**PowerPoint File:** [`reports/Component2_Active_Recovery_Fatigue_Suite_Presentation.pptx`](file:///c:/Users/user/Desktop/Research/fullesterker/reports/Component2_Active_Recovery_Fatigue_Suite_Presentation.pptx)

---

## Slide 1 (Slide 9 in Deck): Title Slide

* **Badge:** `COMPONENT 2`
* **Student Identifier:** `IT23156838 | Rathnayake S`
* **Sub-Header:** `Title of the individual component`
* **Component Title:** `Active Recovery, Joint Health & Fatigue Management Suite`
* **Specialization:** `Software Engineering`
* **Footer:** `SLIIT FACULTY OF COMPUTING | IT23156838 | Rathnayake S | J26-SE-342 | Slide 9`

### Speaker Notes:
> "Good morning, panel. My name is Rathnayake S, student ID IT23156838. Today, I am presenting Component 2 of the FullStrength project: the Active Recovery, Joint Health, and Fatigue Management Suite. My component focuses on solving one of the most critical challenges in strength athletics: detecting central nervous system fatigue and providing autonomous recovery auto-regulation using smartphone optics and computer vision."

---

## Slide 2 (Slide 10 in Deck): Background, Problem Statement & Research Gap

* **Header Banner:** `Active Recovery, Joint Health & Fatigue Management Suite`
* **Sub-Header:** `Component 2 | Contactless rPPG Fatigue Extraction & Bimodal Fusion`
* **Card 1 (Left): The Problem — Central Nervous System (CNS) Fatigue**
  * **Systemic Neural Exhaustion:** Heavy compound lifting (squats, deadlifts) places extreme demands on the central nervous system, reducing the brain's ability to recruit high-threshold motor units.
  * **Catastrophic Injury Risk:** Attempting maximal lifts while the autonomic nervous system is depleted leads to spinal buckling, tendon tears, and acute soft-tissue failure.
  * **Subjective Perception Fails:** Lifters cannot accurately self-judge autonomic fatigue; muscles may feel ready while the central neural drive is heavily suppressed.
* **Card 2 (Right): Research Gap & Our Objective**
  * **Clinical Wearables Are Inaccessible:** Gold-standard Heart Rate Variability (HRV) requires expensive ($100–$300) chest straps or multi-lead ECGs, creating friction for daily lifters.
  * **Commercial Apps Are Inadequate:** Existing smartphone apps only measure average pulse (BPM), which completely fails to measure autonomic balance or vagal parasympathetic recovery.
  * **Our Software Solution:** Turn a standard mobile camera into a contactless photoplethysmography (rPPG) optical sensor that extracts beat-to-beat HRV metrics in 45 seconds.
  * **Autonomous Readiness Triage:** Classify autonomic recovery (GREEN, YELLOW, RED) and prescribe auto-regulated workout volume adjustments.

### Speaker Notes:
> "While muscle soreness is easy to feel, central nervous system fatigue is systemic and silent. When an athlete trains under CNS depletion, their brain cannot properly recruit motor units, which is the leading cause of spinal and joint injuries during heavy squats and deadlifts. Gold-standard ECGs and chest straps are expensive and cumbersome, while current mobile apps only give a single heart rate number. Our goal is to turn the athlete's phone camera into a medical-grade optical pulse sensor to measure true autonomic recovery."

---

## Slide 3 (Slide 11 in Deck): End-to-End DSP Pipeline & Feature Engineering

* **Header Banner:** `Active Recovery, Joint Health & Fatigue Management Suite`
* **Sub-Header:** `Component 2 | Contactless rPPG Fatigue Extraction & Bimodal Fusion`
* **Card 1 (Left): 4-Stage Digital Signal Processing (DSP) Pipeline**
  * **1. Hardware Locking:** Flutter camera controller permanently locks Auto-Exposure (AE), Auto-Focus (AF), and Auto-White-Balance (AWB) to eliminate artificial sensor noise.
  * **2. Green Channel Intensity Extraction:** Spatially averages green luminance across the ROI (520–570 nm). Green light aligns with peak hemoglobin absorption, delivering maximum pulsatile signal-to-noise ratio.
  * **3. 3rd-Order Butterworth Filter:** Zero-phase bandpass filter (0.75–3.0 Hz / 45–180 BPM) eliminates breathing baseline wander and sensor thermal noise.
  * **4. Peak Detection & Artifact Rejection:** Detects systolic peaks and extracts Inter-Beat Intervals (RR). Physiological outlier beats (RR < 330 ms or > 1500 ms) are rejected.
* **Card 2 (Right): 18-Feature Cardiorespiratory Biometric Vector**
  * **Time-Domain HRV:** rMSSD (Primary vagal recovery tone), SDNN (Total autonomic variance), HR Mean & Std, pNN50, pNN20, CV_RR.
  * **Non-Linear Poincaré Geometry:** SD1 (Short-term parasympathetic variance), SD2 (Long-term variance), SD1/SD2 Ratio.
  * **Autonomic Strain (Baevsky SI):** Stress Index (SI = AMo / [2 × Mo × MxDMn]) — spikes to 300–1000+ under acute sympathetic exhaustion.
  * **Frequency-Domain (Welch PSD):** Low Frequency (LF: 0.04–0.15 Hz), High Frequency (HF: 0.15–0.40 Hz), LF/HF Ratio (Sympathovagal balance).
  * **Optical Morphometrics:** Perfusion Index (Blood absorption ratio), Pulse Rise Time (Systolic arterial wave velocity).

### Speaker Notes:
> "To extract clean biometrics from a phone camera, we built a 4-stage DSP pipeline. First, we lock the hardware exposure and white balance to prevent camera adjustments. Second, we extract the green optical spectrum where blood hemoglobin absorption peaks. Third, we apply a 3rd-order Butterworth bandpass filter from 0.75 to 3.0 Hz to isolate heart beats from motion noise. Finally, we reject ectopic beats and compute 18 clinical features including rMSSD, Baevsky's Stress Index, and the LF/HF ratio."

---

## Slide 4 (Slide 12 in Deck): Real-World Machine Learning Validation & Results

* **Header Banner:** `Active Recovery, Joint Health & Fatigue Management Suite`
* **Sub-Header:** `Component 2 | Contactless rPPG Fatigue Extraction & Bimodal Fusion`
* **Card 1 (Left): Empirical Validation on WESAD Dataset**
  * **WESAD Benchmark Ingestion:** Trained on 15 human subjects (S2–S17), extracting 2,912 sliding 45-second windows across Baseline, Amusement, and TSST Acute Stress.
  * **Zero-Leakage GroupKFold CV:** 5-Fold cross-validation grouped by subject to guarantee the model generalizes to completely unseen human users.
  * **Validation Accuracy:** 82.85% overall classification accuracy (Peak: 83.36% @ Epoch 56).
  * **Multi-Class ROC-AUC:** Macro AUC of 0.8922 (Red Exhaustion Tier AUC: 0.978).
  * **Safety in Exhaustion:** 86.2% true positive detection of acute fatigue (with 0% misclassified as mild Yellow).
  * **Production ONNX Export:** Converted to .onnx format (2.5 MB) with 100% numerical parity for offline sub-10ms Flutter mobile execution.
* **Visuals (Right):**
  * **Figure 1:** Training and Validation Accuracy & Loss curves over 140 epochs.
  * **Figure 2:** Confusion Matrix Heatmap showing class distributions.

### Speaker Notes:
> "Rather than using synthetic data, our production model was trained on the real-world WESAD clinical benchmark consisting of 15 subjects and 2,912 physiological windows. Using 5-fold GroupKFold cross-validation to prevent subject data leakage, our model achieved 82.85% validation accuracy, an overall ROC-AUC of 0.892, and a 0.978 AUC in detecting acute red-tier exhaustion. The model is exported to ONNX format, allowing our mobile Flutter app to run predictions offline in under 10 milliseconds without cloud latency."

---

## Slide 5 (Slide 13 in Deck): Bimodal Decision Fusion & Adaptive Prescriptions

* **Header Banner:** `Active Recovery, Joint Health & Fatigue Management Suite`
* **Sub-Header:** `Component 2 | Contactless rPPG Fatigue Extraction & Bimodal Fusion`
* **Top Banner Card: The Cross-Subsystem Fusion Concept**
  * A single heartbeat scan alone cannot distinguish whether a drop in rMSSD is driven by **Cognitive/Mental Stress** or **Physical Neuromuscular Damage**. Subsystem 1 fuses with Subsystem 2 (5-Rep Squat Kinematics via MediaPipe) to evaluate the **Bilateral Asymmetry Index (ASI)**:  
    `ASI = (|L_load - R_load| / max(L_load, R_load)) * 100%`
* **Case 1 (Green Card): Fully Recovered**
  * **Autonomic Tier:** GREEN (rMSSD ≥ 45 ms)
  * **Kinematic ASI:** ≤ 10% (Symmetrical)
  * **Root Driver:** Homeostatic Balance
  * **Prescription:** 100% Full Training Volume. Cleared for maximal compound lifts (Squats, Deadlifts, 1–5 RM, Plyometrics).
* **Case 2 (Yellow Card): Cognitive / Life Stress**
  * **Autonomic Tier:** YELLOW / RED (rMSSD < 45 ms)
  * **Kinematic ASI:** ≤ 10% (Symmetrical)
  * **Root Driver:** Mental Load / Sleep Deficit
  * **Prescription:** **DO NOT CANCEL SESSION.** Motor unit firing is balanced. Train at RPE 7–8; reduce working sets by 20%; avoid muscular failure.
* **Case 3 (Red Card): Physical Neuromuscular Fatigue**
  * **Autonomic Tier:** YELLOW / RED (rMSSD < 45 ms)
  * **Kinematic ASI:** > 15% (Asymmetrical)
  * **Root Driver:** Structural Muscle Microtrauma / Joint Strain
  * **Prescription:** **HIGH INJURY RISK.** Postpone axial spinal loading. Prescribe 20 mins low-intensity Zone-2 cardio & mobility work.

### Speaker Notes:
> "Finally, our standout contribution is the Bimodal Decision Fusion Algorithm connecting Subsystem 1 with Subsystem 2. If a lifter wakes up with low HRV, is it because they had a stressful exam, or because their quad tendon is microtraumatized? If their squat symmetry is balanced, it is life stress—so we keep training at RPE 7 to 8 with a 20% volume reduction. But if their asymmetry exceeds 15%, their neuromuscular system is structurally compromised—so we immediately stop axial spinal loading and prescribe active recovery. Thank you."
