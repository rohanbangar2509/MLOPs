# Assignment Report: SHAP/LIME for Explainability

**Name:**  
**Roll number:**  
**Subject / assignment:** MLOps — Apply SHAP/LIME for Explainability  
**Date:**  

## 1. Objective
The objective is to apply post-hoc explainability methods to a trained machine-learning classifier and understand both global feature influence and individual predictions.

## 2. Tools and dataset
- Python:
- scikit-learn:
- Model: Random Forest classifier
- Dataset: scikit-learn built-in Wisconsin Breast Cancer dataset
- Explainability tools: SHAP and LIME

## 3. Methodology
1. Loaded the dataset and separated features from the target.
2. Split the data into training and testing subsets with a fixed random seed.
3. Trained a Random Forest classifier and measured classification performance.
4. Used SHAP to generate a global summary plot and a local explanation.
5. Used LIME to generate a local explanation for the same selected test instance.
6. Saved plots, metrics, and a text summary under `artifacts/`.

## 4. Model evaluation
Copy the actual values from `artifacts/metrics.json`.

| Metric | Result |
|---|---:|
| Accuracy | |
| Precision | |
| Recall | |
| F1-score | |
| ROC-AUC | |

## 5. SHAP results
Insert `artifacts/shap_summary.png` and `artifacts/shap_local.png`.

**Global interpretation:** Describe the top three features visible in the SHAP summary plot and how their SHAP values vary.

**Local interpretation:** Describe the features with the largest absolute SHAP values for the selected prediction. Explain that direction is relative to class 1 model output in this implementation.

## 6. LIME results
Insert `artifacts/lime_local.png` or include a screenshot of `artifacts/lime_local.html`.

Describe the top conditions and weights. Explain which conditions support or oppose the selected predicted class according to LIME.

## 7. SHAP vs LIME
- SHAP uses Shapley-value-based feature attributions and can be used for global and local interpretation.
- LIME perturbs a selected instance and fits a locally interpretable surrogate model.
- The methods may not rank features identically because their definitions, sampling, and approximations differ.
- Both explanations describe model behavior; they do not establish causation.

## 8. Limitations and responsible use
- Explanations are specific to the trained model, data, and chosen instance.
- Feature attribution does not prove causal relationships.
- Dataset and model bias can affect predictions and explanations.
- This dataset is for educational demonstration only and must not be used for medical decisions.

## 9. Conclusion
Summarize what SHAP revealed globally, what the local SHAP/LIME explanations showed for the selected instance, and why explainability can improve transparency in an ML workflow.
