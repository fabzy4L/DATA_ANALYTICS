# Statistical Methods: Nicotine Exposure Gene Expression Study

**Reference:** Vargas-Medrano J, Carcoba LM, et al. (2023). *Sex and diet-dependent gene alterations in human and rat brains with a history of nicotine exposure*. Front. Psychiatry. [doi: 10.3389/fpsyt.2023.1104563](https://doi.org/10.3389/fpsyt.2023.1104563)

---

## 1. Study Design and Data Preparation
The study utilizes a cross-species comparative design (Human and Rat) to investigate the effects of nicotine exposure on the expression of genes related to neuroplasticity and oligodendrocyte function.

### qPCR Data Transformation
Raw Cycle Threshold (Ct) values obtained from qPCR instruments were processed using the **$\Delta\Delta Ct$ methodology**:
*   **Normalization:** Gene expression was normalized to **GAPDH** (the internal housekeeping control) to account for variations in RNA quality and input quantity.
*   **Relative Quantification:** Relative expression was calculated as **$2^{-\Delta Ct}$**.
*   **Fold Change (FC):** Final data were expressed as Fold Change relative to the average of the control group.

---

## 2. Mathematical Justification for Transformations
To satisfy the assumptions of General Linear Models (GLM) and ANOVA, data were subjected to a rigorous transformation pipeline.

### Logarithmic Transformation ($Log_{10}$)
*   **Justification:** Raw Fold Change data is inherently asymmetrical (upregulation spans 1 to $\infty$, while downregulation is compressed between 0 and 1). This asymmetry violates the assumption of homoscedasticity (equal variance).
*   **Result:** Applying $Log_{10}$ (using the `fx` function) creates a symmetrical additive scale where a 2-fold increase (+0.301) and a 2-fold decrease (-0.301) are mathematically equivalent, stabilizing variance across treatment groups.

### Z-score Standardisation (Scaling)
*   **Justification:** Different genes (e.g., high-abundance `GAPDH` vs. low-abundance `CERKL`) exhibit baseline expression levels differing by orders of magnitude. 
*   **Result:** The `scale` (or `fx2`) function centers data at a mean of 0 with a standard deviation of 1. This allows for valid cross-gene comparisons and effective visualization in heatmaps.

### Power Transformation ($x^{-1/2}$)
*   **Justification:** In cases where $Log_{10}$ fails to resolve heteroscedasticity or non-normality, more aggressive power transformations (using `fx3`) were employed.
*   **Result:** This stabilizes the relationship between the mean and variance, particularly for data following a Poisson-like distribution.

---

## 3. Statistical Decision Tree
The analysis followed a systematic workflow to ensure the validity of $P$-values:

1.  **Normality Check:** Every gene/cohort subset was tested using the **Shapiro-Wilk test**.
2.  **Initial Transformation:** If $P < 0.05$ (non-normal), data was **$Log_{10}$ transformed**.
3.  **Secondary Validation:** The transformed data was re-tested for normality.
4.  **Alternative Paths:**
    *   **Parametric Path:** If data became normal ($P > 0.05$), **ANOVA/Linear Models** were applied.
    *   **Non-Parametric Path:** If data remained non-normal despite transformation (e.g., `COL4A1`), non-parametric tests (Kruskal-Wallis) were utilized.
5.  **Multi-Way ANOVA:** Verified normal data were then passed into factorial models (`Gene ~ DX * SEX * DIET`).

---

## 4. Statistical Modeling Framework
The core analysis utilizes General Linear Models (GLM) and Multi-way ANOVA to identify main effects and complex biological interactions.

### Main Effects Analysis
Initial screens determined the independent impact of **Diagnosis (DX):** Control vs. Nicotine/VDS.

### Interaction Modeling
To address the sex and diet-dependent nature of the alterations:
*   **Sex Interactions:** `Gene ~ DX * SEX` determined if nicotine exposure effects were sex-specific.
*   **Dietary Interactions:** In the rat cohort, `DX * DIET` analyzed the metabolic modulation of gene regulation.
*   **Species Interactions:** `DX * SPECIES` evaluated translational conservation.

---

## 5. Post-Hoc Analysis and Significance
*   **Tukey’s Honest Significant Difference (HSD):** Applied following significant ANOVA results to identify specific pairwise differences between group combinations.
*   **Significance Thresholds:**
    *   **$P < 0.05$:** Statistically significant.
    *   **$0.05 \leq P < 0.10$:** Statistical trend.
*   **Software:** Analysis implemented using **R (v4.x)** and **Python**.
