"""
Generates PowerPoint slides for Component 2:
'Active Recovery, Joint Health & Fatigue Management Suite'
Presenter: IT23156838 | Rathnayake S
Group: J26-SE-342 | FullStrength PP1 Presentation

Exactly 5 professional 16:9 widescreen slides matching the group template.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PPTX = os.path.join(BASE_DIR, "reports", "Component2_Active_Recovery_Fatigue_Suite_Presentation.pptx")

# High-resolution charts
CURVES_IMG = os.path.join(BASE_DIR, "recovery_backend", "reports", "evaluation_curves.png")
CM_IMG = os.path.join(BASE_DIR, "recovery_backend", "reports", "confusion_matrix.png")

# Palette matching SLIIT FullStrength template
C_NAVY_HEADER = RGBColor(14, 38, 77)      # Dark Navy banner
C_WHITE = RGBColor(255, 255, 255)
C_DARK_TEXT = RGBColor(30, 41, 59)       # Slate text
C_MUTED_TEXT = RGBColor(100, 116, 139)   # Subtitle grey
C_ACCENT_GREEN = RGBColor(16, 185, 129)  # Green pill badge
C_ACCENT_BLUE = RGBColor(37, 99, 235)    # Blue card accent
C_CARD_BG = RGBColor(248, 250, 252)      # Very light grey card background
C_CARD_BORDER = RGBColor(226, 232, 240)  # Border
C_RED_ACCENT = RGBColor(220, 38, 38)     # Red accent

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_standard_header_footer(slide, slide_num_str):
        # Top banner (Dark Navy)
        top_banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        top_banner.fill.solid()
        top_banner.fill.fore_color.rgb = C_NAVY_HEADER
        top_banner.line.color.rgb = C_NAVY_HEADER

        # Header Title Text
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.18), Inches(11.5), Inches(0.8))
        tf = tx_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = "Active Recovery, Joint Health & Fatigue Management Suite"
        p.font.name = "Segoe UI"
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

        # Subtitle / Component tracker
        p2 = tf.add_paragraph()
        p2.text = "Component 2 | Contactless rPPG Fatigue Extraction & Bimodal Fusion"
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(11)
        p2.font.color.rgb = RGBColor(147, 197, 253)

        # Footer
        footer_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.02))
        footer_line.fill.solid()
        footer_line.fill.fore_color.rgb = C_CARD_BORDER
        footer_line.line.color.rgb = C_CARD_BORDER

        foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35))
        ftf = foot_box.text_frame
        fp = ftf.paragraphs[0]
        fp.text = f"SLIIT FACULTY OF COMPUTING  |  IT23156838 - Rathnayake S  |  J26-SE-342  |  Slide {slide_num_str}"
        fp.font.name = "Segoe UI"
        fp.font.size = Pt(9.5)
        fp.font.color.rgb = C_MUTED_TEXT

    def add_card(slide, left, top, width, height, title, border_color=C_CARD_BORDER, bg_color=C_CARD_BG):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)

        title_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.45))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_NAVY_HEADER
        return card

    # =========================================================================
    # SLIDE 1: Component 2 Title Slide (Slide 9 in Deck)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)

    # Component 2 Green Badge
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.5), Inches(2.2), Inches(0.45))
    badge.fill.solid()
    badge.fill.fore_color.rgb = C_ACCENT_GREEN
    badge.line.fill.background()
    btf = badge.text_frame
    bp = btf.paragraphs[0]
    bp.text = "COMPONENT 2"
    bp.alignment = PP_ALIGN.CENTER
    bp.font.name = "Segoe UI"
    bp.font.size = Pt(11)
    bp.font.bold = True
    bp.font.color.rgb = C_WHITE

    # Student Info & Title
    s1_title_box = s1.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(7.5), Inches(3.5))
    tf1 = s1_title_box.text_frame
    tf1.word_wrap = True

    p_id = tf1.paragraphs[0]
    p_id.text = "IT23156838 | Rathnayake S"
    p_id.font.name = "Segoe UI"
    p_id.font.size = Pt(28)
    p_id.font.bold = True
    p_id.font.color.rgb = C_NAVY_HEADER
    p_id.space_after = Pt(14)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Title of the individual component:"
    p_sub.font.name = "Segoe UI"
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = C_MUTED_TEXT

    p_name = tf1.add_paragraph()
    p_name.text = "Active Recovery, Joint Health &\nFatigue Management Suite"
    p_name.font.name = "Segoe UI"
    p_name.font.size = Pt(26)
    p_name.font.bold = True
    p_name.font.color.rgb = C_ACCENT_GREEN
    p_name.space_after = Pt(20)

    p_spec = tf1.add_paragraph()
    p_spec.text = "Specialization: Software Engineering"
    p_spec.font.name = "Segoe UI"
    p_spec.font.size = Pt(14)
    p_spec.font.bold = True
    p_spec.font.color.rgb = C_NAVY_HEADER

    # Right side circular accent & card
    circ = s1.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9.0), Inches(1.5), Inches(3.6), Inches(3.6))
    circ.fill.solid()
    circ.fill.fore_color.rgb = RGBColor(220, 252, 231)
    circ.line.fill.background()

    card_s1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.3), Inches(1.8), Inches(3.0), Inches(3.0))
    card_s1.fill.solid()
    card_s1.fill.fore_color.rgb = C_WHITE
    card_s1.line.color.rgb = C_ACCENT_GREEN
    card_s1.line.width = Pt(2)
    c1_tf = card_s1.text_frame
    c1_tf.word_wrap = True
    c1_p = c1_tf.paragraphs[0]
    c1_p.text = "Presenter: Rathnayake S\nID: IT23156838\n\nSubsystem 1:\nContactless rPPG Pulse Scanner\n&\nBimodal Kinematic Fusion"
    c1_p.alignment = PP_ALIGN.CENTER
    c1_p.font.name = "Segoe UI"
    c1_p.font.size = Pt(11.5)
    c1_p.font.color.rgb = C_NAVY_HEADER

    # S1 Footer
    foot_s1 = s1.shapes.add_textbox(Inches(1.2), Inches(6.8), Inches(11.0), Inches(0.4))
    fs1_tf = foot_s1.text_frame
    fs1_p = fs1_tf.paragraphs[0]
    fs1_p.text = "SLIIT FACULTY OF COMPUTING  |  IT23156838  |  Rathnayake S  |  J26-SE-342  |  Slide 9"
    fs1_p.font.name = "Segoe UI"
    fs1_p.font.size = Pt(10)
    fs1_p.font.color.rgb = C_MUTED_TEXT

    # =========================================================================
    # SLIDE 2: Problem Statement & Research Gap (Slide 10 in Deck)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_standard_header_footer(s2, "10")

    # Card 1: Problem Statement
    add_card(s2, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.3), "The Problem: Central Nervous System (CNS) Fatigue", C_RED_ACCENT)
    tb2_1 = s2.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.5))
    tf2_1 = tb2_1.text_frame
    tf2_1.word_wrap = True
    
    bullets_s2_1 = [
        ("Systemic Neural Exhaustion:", "High-intensity compound lifting (squats, deadlifts) severely taxes the brain and CNS, reducing high-threshold motor unit recruitment capacity."),
        ("Catastrophic Injury Risk:", "Attempting maximal loading while the autonomic nervous system is depleted leads to spinal buckling, tendon failure, and acute soft-tissue tears."),
        ("Subjective Perception Fails:", "Athletes cannot accurately self-judge CNS fatigue; physical muscles may feel ready while the neural drive is severely suppressed."),
    ]
    for i, (b_title, b_desc) in enumerate(bullets_s2_1):
        p = tf2_1.paragraphs[0] if i == 0 else tf2_1.add_paragraph()
        p.text = f"• {b_title} "
        p.font.name = "Segoe UI"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = C_DARK_TEXT
        
        run = p.add_run()
        run.text = b_desc
        run.font.bold = False
        run.font.size = Pt(11)
        run.font.color.rgb = C_DARK_TEXT
        p.space_after = Pt(12)

    # Card 2: Research Gap & Our Objective
    add_card(s2, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.3), "Research Gap & Project Objective", C_ACCENT_BLUE)
    tb2_2 = s2.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf2_2 = tb2_2.text_frame
    tf2_2.word_wrap = True

    bullets_s2_2 = [
        ("Clinical Wearables are Expensive:", "Gold-standard Heart Rate Variability (HRV) requires $100-$300 chest straps or multi-lead ECGs, creating high friction for everyday lifters."),
        ("Commercial Apps Are Inadequate:", "Basic mobile apps compute average Heart Rate (BPM), completely failing to measure autonomic balance or vagal parasympathetic recovery."),
        ("Proposed Software Solution:", "Transform standard smartphone cameras into a contactless photoplethysmography (rPPG) optical sensor that extracts beat-to-beat HRV metrics in 45 seconds."),
        ("Autonomous Readiness Triage:", "Predict CNS recovery state (GREEN, YELLOW, RED) and prescribe auto-regulated workout volume adjustments."),
    ]
    for i, (b_title, b_desc) in enumerate(bullets_s2_2):
        p = tf2_2.paragraphs[0] if i == 0 else tf2_2.add_paragraph()
        p.text = f"• {b_title} "
        p.font.name = "Segoe UI"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = C_DARK_TEXT
        
        run = p.add_run()
        run.text = b_desc
        run.font.bold = False
        run.font.size = Pt(11)
        run.font.color.rgb = C_DARK_TEXT
        p.space_after = Pt(12)

    # =========================================================================
    # SLIDE 3: DSP Pipeline & Feature Engineering (Slide 11 in Deck)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_standard_header_footer(s3, "11")

    # Card 1: 4-Stage DSP Architecture
    add_card(s3, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.3), "End-to-End Digital Signal Processing (DSP)")
    tb3_1 = s3.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.5))
    tf3_1 = tb3_1.text_frame
    tf3_1.word_wrap = True

    dsp_steps = [
        ("1. Hardware Locking:", "Locks Auto-Exposure (AE), Auto-Focus (AF), and Auto-White-Balance (AWB) on rear mobile camera to eliminate artificial sensor noise."),
        ("2. Green Channel Intensity:", "Extracts mean green luminance (520-570 nm) across ROI — green light matches peak oxygenated hemoglobin absorption, maximizing AC/DC pulsatile SNR."),
        ("3. 3rd-Order Butterworth Filter:", "Zero-phase bandpass filter (0.75 - 3.0 Hz / 45 - 180 BPM) eliminates respiratory baseline wander (<0.75 Hz) and high-frequency thermal noise."),
        ("4. Peak Detection & Outlier Rejection:", "Adaptive thresholding extracts systolic peaks and RR interval series; physiologically impossible intervals (RR < 330ms or > 1500ms) are strictly rejected."),
    ]
    for i, (title, desc) in enumerate(dsp_steps):
        p = tf3_1.paragraphs[0] if i == 0 else tf3_1.add_paragraph()
        p.text = f"• {title} "
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_NAVY_HEADER
        
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.size = Pt(10.5)
        run.font.color.rgb = C_DARK_TEXT
        p.space_after = Pt(10)

    # Card 2: 18-Feature Cardiorespiratory Vector
    add_card(s3, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.3), "18-Feature Cardiorespiratory Extraction")
    tb3_2 = s3.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf3_2 = tb3_2.text_frame
    tf3_2.word_wrap = True

    feats = [
        ("Time-Domain HRV:", "rMSSD (Primary vagal tone marker), SDNN (Total autonomic variance), HR Mean & Std, pNN50, pNN20, CV_RR."),
        ("Non-Linear Poincaré Geometry:", "SD1 (Short-term parasympathetic variance), SD2 (Long-term variance), SD1/SD2 Ratio."),
        ("Autonomic Strain (Baevsky SI):", "Stress Index (SI = AMo / [2 × Mo × MxDMn]) — spikes to 300-1000+ under acute sympathetic exhaustion."),
        ("Frequency-Domain (Welch PSD):", "Low Frequency (LF: 0.04-0.15 Hz), High Frequency (HF: 0.15-0.40 Hz), LF/HF Ratio (Sympathovagal balance)."),
        ("Optical Morphometrics:", "Perfusion Index (Pulsatile blood absorption), Pulse Rise Time (Systolic arterial wave upstroke)."),
    ]
    for i, (title, desc) in enumerate(feats):
        p = tf3_2.paragraphs[0] if i == 0 else tf3_2.add_paragraph()
        p.text = f"• {title} "
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_ACCENT_BLUE
        
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.size = Pt(10.5)
        run.font.color.rgb = C_DARK_TEXT
        p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 4: ML Training, WESAD Validation & Results (Slide 12 in Deck)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_standard_header_footer(s4, "12")

    # Left Column: Metrics & Architecture
    add_card(s4, Inches(0.8), Inches(1.4), Inches(5.2), Inches(5.3), "Empirical Validation on WESAD Dataset")
    tb4_1 = s4.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(4.8), Inches(4.5))
    tf4_1 = tb4_1.text_frame
    tf4_1.word_wrap = True

    results_bullets = [
        ("WESAD Benchmark Ingestion:", "Trained on 15 human subjects (S2-S17), 2,912 sliding 45-second windows across Baseline, Amusement, and TSST Stress."),
        ("Zero-Leakage GroupKFold CV:", "5-Fold cross-validation grouped by subject to guarantee the model generalizes to completely unseen individuals."),
        ("Validation Accuracy:", "82.85% overall accuracy (Peak: 83.36% @ Epoch 56)."),
        ("Multi-Class ROC-AUC:", "Macro AUC of 0.8922 (Red Exhaustion Tier AUC: 0.978)."),
        ("Safety in Exhaustion:", "86.2% true positive detection of acute fatigue (0% misclassified as mild Yellow)."),
        ("Production ONNX Export:", "Converted to .onnx format (2.5MB) with 100% numerical parity for offline sub-10ms Flutter execution."),
    ]
    for i, (title, desc) in enumerate(results_bullets):
        p = tf4_1.paragraphs[0] if i == 0 else tf4_1.add_paragraph()
        p.text = f"• {title} "
        p.font.name = "Segoe UI"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_NAVY_HEADER
        
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.size = Pt(10)
        run.font.color.rgb = C_DARK_TEXT
        p.space_after = Pt(6)

    # Right Column: Visual Curves & Confusion Matrix
    if os.path.exists(CURVES_IMG):
        s4.shapes.add_picture(CURVES_IMG, Inches(6.3), Inches(1.4), width=Inches(6.2))
    if os.path.exists(CM_IMG):
        s4.shapes.add_picture(CM_IMG, Inches(7.5), Inches(4.0), width=Inches(3.8))

    # =========================================================================
    # SLIDE 5: Bimodal Decision Fusion & Prescriptions (Slide 13 in Deck)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_standard_header_footer(s5, "13")

    # Card 1: Bimodal Fusion Concept
    add_card(s5, Inches(0.8), Inches(1.4), Inches(11.733), Inches(1.7), "Bimodal Decision Fusion: Connecting Subsystem 1 & Subsystem 2")
    tb5_1 = s5.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.3), Inches(1.1))
    tf5_1 = tb5_1.text_frame
    tf5_1.word_wrap = True
    p5_1 = tf5_1.paragraphs[0]
    p5_1.text = "A drop in rMSSD alone cannot distinguish Mental Stress from Physical Neuromuscular Damage. Subsystem 1 fuses with Subsystem 2 (5-Rep Squat Kinematics via MediaPipe) to evaluate the Bilateral Asymmetry Index (ASI):  ASI = (|L_load - R_load| / max(L_load, R_load)) × 100%"
    p5_1.font.name = "Segoe UI"
    p5_1.font.size = Pt(11)
    p5_1.font.color.rgb = C_DARK_TEXT

    # 3 Prescription Cards Side-by-Side
    card_w = Inches(3.7)
    gap = Inches(0.3)

    # Case 1: Green
    add_card(s5, Inches(0.8), Inches(3.3), card_w, Inches(3.5), "Case 1: Fully Recovered", C_ACCENT_GREEN, RGBColor(240, 253, 244))
    tb_c1 = s5.shapes.add_textbox(Inches(0.95), Inches(3.8), card_w - Inches(0.3), Inches(2.8))
    tfc1 = tb_c1.text_frame
    tfc1.word_wrap = True
    c1_items = [
        "ANS Tier: GREEN (rMSSD ≥ 45ms)",
        "Kinematic ASI: ≤ 10% (Symmetrical)",
        "Root Driver: Homeostatic Balance",
        "Prescription: 100% Volume cleared. Green-lit for maximal compound lifts (Squats, Deadlifts, 1-5 RM, Plyometrics).",
    ]
    for i, it in enumerate(c1_items):
        p = tfc1.paragraphs[0] if i == 0 else tfc1.add_paragraph()
        p.text = f"• {it}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.color.rgb = C_DARK_TEXT
        p.space_after = Pt(6)

    # Case 2: Yellow / Red Symmetrical
    add_card(s5, Inches(0.8) + card_w + gap, Inches(3.3), card_w, Inches(3.5), "Case 2: Cognitive Stress", RGBColor(245, 158, 11), RGBColor(254, 252, 232))
    tb_c2 = s5.shapes.add_textbox(Inches(0.95) + card_w + gap, Inches(3.8), card_w - Inches(0.3), Inches(2.8))
    tfc2 = tb_c2.text_frame
    tfc2.word_wrap = True
    c2_items = [
        "ANS Tier: YELLOW / RED (rMSSD < 45ms)",
        "Kinematic ASI: ≤ 10% (Symmetrical)",
        "Root Driver: Mental Load / Sleep Deficit",
        "Prescription: DO NOT CANCEL. Motor firing is balanced. Train at RPE 7-8; reduce working sets by 20%; avoid failure.",
    ]
    for i, it in enumerate(c2_items):
        p = tfc2.paragraphs[0] if i == 0 else tfc2.add_paragraph()
        p.text = f"• {it}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.color.rgb = C_DARK_TEXT
        p.space_after = Pt(6)

    # Case 3: Yellow / Red Asymmetrical
    add_card(s5, Inches(0.8) + (card_w + gap) * 2, Inches(3.3), card_w, Inches(3.5), "Case 3: Neuromuscular Fatigue", C_RED_ACCENT, RGBColor(254, 242, 242))
    tb_c3 = s5.shapes.add_textbox(Inches(0.95) + (card_w + gap) * 2, Inches(3.8), card_w - Inches(0.3), Inches(2.8))
    tfc3 = tb_c3.text_frame
    tfc3.word_wrap = True
    c3_items = [
        "ANS Tier: YELLOW / RED (rMSSD < 45ms)",
        "Kinematic ASI: > 15% (Asymmetrical)",
        "Root Driver: Structural Muscle Microtrauma",
        "Prescription: HIGH INJURY RISK! Postpone axial spinal loading. Prescribe 20 mins low-intensity Zone-2 cardio & mobility.",
    ]
    for i, it in enumerate(c3_items):
        p = tfc3.paragraphs[0] if i == 0 else tfc3.add_paragraph()
        p.text = f"• {it}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.color.rgb = C_DARK_TEXT
        p.space_after = Pt(6)

    prs.save(OUTPUT_PPTX)
    print(f"\n[PowerPoint Generated Successfully] -> {OUTPUT_PPTX}")


if __name__ == "__main__":
    create_deck()
