"""
AI-Based Fake Review Detection System
Text Mining, Metadata Analysis, and Machine Learning Algorithms
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

def generate_review_data():
    """Generate synthetic review data for fake review detection"""
    np.random.seed(42)
    n_reviews = 1000
    
    # Fake review characteristics
    fake_keywords = ['amazing', 'best', 'perfect', 'highly recommend', 'love it', 'excellent', 'awesome', 'fantastic']
    genuine_keywords = ['good', 'decent', 'okay', 'average', 'nice', 'works well', 'satisfied', 'meets expectations']
    
    reviews = []
    labels = []
    
    for i in range(n_reviews):
        is_fake = np.random.choice([0, 1], p=[0.6, 0.4])  # 40% fake reviews
        
        if is_fake:
            review_text = np.random.choice(fake_keywords, size=np.random.randint(3, 8))
            review_text = ' '.join(review_text) + ' ' + ' '.join(np.random.choice(['great', 'wonderful', 'superb'], 2))
        else:
            review_text = np.random.choice(genuine_keywords, size=np.random.randint(3, 8))
            review_text = ' '.join(review_text) + ' ' + ' '.join(np.random.choice(['product', 'service', 'quality'], 2))
        
        reviews.append(review_text)
        labels.append(is_fake)
    
    data = {
        'Review_ID': range(1, n_reviews + 1),
        'Review_Text': reviews,
        'Rating': np.random.randint(1, 6, n_reviews),
        'Review_Length': [len(r.split()) for r in reviews],
        'Reviewer_Age_Days': np.random.randint(1, 3650, n_reviews),
        'Reviewer_Total_Reviews': np.random.randint(1, 100, n_reviews),
        'Reviewer_Avg_Rating': np.random.uniform(1, 5, n_reviews),
        'Review_Helpfulness': np.random.randint(0, 100, n_reviews),
        'Time_Between_Reviews_Hours': np.random.randint(1, 720, n_reviews),
        'Verified_Purchase': np.random.choice([0, 1], n_reviews, p=[0.3, 0.7]),
        'Is_Fake': labels
    }
    
    df = pd.DataFrame(data)
    df.to_csv('/home/ubuntu/fake_reviews_dataset.csv', index=False)
    return df

def train_classification_models(df):
    """Train classification models for fake review detection"""
    
    # Text vectorization
    vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
    X_text = vectorizer.fit_transform(df['Review_Text'])
    
    # Metadata features
    X_metadata = df[['Rating', 'Review_Length', 'Reviewer_Age_Days', 'Reviewer_Total_Reviews',
                     'Reviewer_Avg_Rating', 'Review_Helpfulness', 'Time_Between_Reviews_Hours', 'Verified_Purchase']]
    
    # Combine features
    from scipy.sparse import hstack
    X_combined = hstack([X_text, X_metadata.values])
    y = df['Is_Fake']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=42)
    
    results = {}
    
    # Logistic Regression
    lr_model = LogisticRegression(max_iter=1000, random_state=42)
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)
    y_pred_proba_lr = lr_model.predict_proba(X_test)[:, 1]
    results['Logistic Regression'] = {
        'accuracy': accuracy_score(y_test, y_pred_lr),
        'precision': precision_score(y_test, y_pred_lr),
        'recall': recall_score(y_test, y_pred_lr),
        'f1': f1_score(y_test, y_pred_lr),
        'auc': roc_auc_score(y_test, y_pred_proba_lr),
        'predictions': y_pred_lr,
        'probabilities': y_pred_proba_lr,
        'model': lr_model
    }
    
    # Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    y_pred_proba_rf = rf_model.predict_proba(X_test)[:, 1]
    results['Random Forest'] = {
        'accuracy': accuracy_score(y_test, y_pred_rf),
        'precision': precision_score(y_test, y_pred_rf),
        'recall': recall_score(y_test, y_pred_rf),
        'f1': f1_score(y_test, y_pred_rf),
        'auc': roc_auc_score(y_test, y_pred_proba_rf),
        'predictions': y_pred_rf,
        'probabilities': y_pred_proba_rf,
        'feature_importance': rf_model.feature_importances_,
        'model': rf_model
    }
    
    # Gradient Boosting
    gb_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
    gb_model.fit(X_train, y_train)
    y_pred_gb = gb_model.predict(X_test)
    y_pred_proba_gb = gb_model.predict_proba(X_test)[:, 1]
    results['Gradient Boosting'] = {
        'accuracy': accuracy_score(y_test, y_pred_gb),
        'precision': precision_score(y_test, y_pred_gb),
        'recall': recall_score(y_test, y_pred_gb),
        'f1': f1_score(y_test, y_pred_gb),
        'auc': roc_auc_score(y_test, y_pred_proba_gb),
        'predictions': y_pred_gb,
        'probabilities': y_pred_proba_gb,
        'feature_importance': gb_model.feature_importances_,
        'model': gb_model
    }
    
    return results, X_test, y_test, vectorizer

def generate_visualizations(df, results, X_test, y_test):
    """Generate fake review detection visualizations"""
    
    # 1. Review Distribution and Characteristics
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Fake Review Detection: Data Analysis', fontsize=16, fontweight='bold')
    
    axes[0, 0].hist(df['Rating'], bins=5, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Rating Distribution')
    axes[0, 0].set_xlabel('Rating')
    axes[0, 0].set_ylabel('Frequency')
    
    fake_genuine = df['Is_Fake'].value_counts()
    axes[0, 1].bar(['Genuine', 'Fake'], [fake_genuine[0], fake_genuine[1]], color=['green', 'red'])
    axes[0, 1].set_title('Genuine vs Fake Reviews')
    axes[0, 1].set_ylabel('Count')
    
    axes[1, 0].scatter(df['Review_Length'], df['Rating'], alpha=0.6, c=df['Is_Fake'], cmap='RdYlGn_r')
    axes[1, 0].set_title('Review Length vs Rating')
    axes[1, 0].set_xlabel('Review Length (words)')
    axes[1, 0].set_ylabel('Rating')
    
    axes[1, 1].hist(df[df['Is_Fake']==0]['Review_Length'], bins=20, alpha=0.6, label='Genuine', color='green')
    axes[1, 1].hist(df[df['Is_Fake']==1]['Review_Length'], bins=20, alpha=0.6, label='Fake', color='red')
    axes[1, 1].set_title('Review Length Distribution')
    axes[1, 1].set_xlabel('Review Length (words)')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].legend()
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/fake_review_data_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Model Performance Comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    models = list(results.keys())
    accuracy_vals = [results[m]['accuracy'] for m in models]
    precision_vals = [results[m]['precision'] for m in models]
    recall_vals = [results[m]['recall'] for m in models]
    f1_vals = [results[m]['f1'] for m in models]
    
    x = np.arange(len(models))
    width = 0.2
    
    ax.bar(x - 1.5*width, accuracy_vals, width, label='Accuracy', color='skyblue')
    ax.bar(x - 0.5*width, precision_vals, width, label='Precision', color='lightcoral')
    ax.bar(x + 0.5*width, recall_vals, width, label='Recall', color='lightgreen')
    ax.bar(x + 1.5*width, f1_vals, width, label='F1 Score', color='gold')
    
    ax.set_xlabel('Models', fontweight='bold')
    ax.set_ylabel('Score', fontweight='bold')
    ax.set_title('Model Performance Comparison', fontweight='bold', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim([0, 1.1])
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/fake_review_model_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Confusion Matrices
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle('Confusion Matrices for All Models', fontsize=14, fontweight='bold')
    
    for idx, model_name in enumerate(results.keys()):
        y_pred = results[model_name]['predictions']
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx], cbar=False)
        axes[idx].set_title(f'{model_name}')
        axes[idx].set_ylabel('True Label')
        axes[idx].set_xlabel('Predicted Label')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/fake_review_confusion_matrices.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. ROC Curves
    fig, ax = plt.subplots(figsize=(10, 7))
    
    for model_name in results.keys():
        y_pred_proba = results[model_name]['probabilities']
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        auc = results[model_name]['auc']
        ax.plot(fpr, tpr, label=f'{model_name} (AUC = {auc:.3f})', linewidth=2)
    
    ax.plot([0, 1], [0, 1], 'k--', label='Random Classifier', linewidth=1)
    ax.set_xlabel('False Positive Rate', fontweight='bold')
    ax.set_ylabel('True Positive Rate', fontweight='bold')
    ax.set_title('ROC Curves for Fake Review Detection Models', fontweight='bold', fontsize=14)
    ax.legend(loc='lower right')
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/fake_review_roc_curves.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Feature Importance and Metadata Analysis
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Metadata Analysis and Feature Insights', fontsize=16, fontweight='bold')
    
    # Verified Purchase vs Fake
    verified_fake = pd.crosstab(df['Verified_Purchase'], df['Is_Fake'])
    verified_fake.plot(kind='bar', ax=axes[0, 0], color=['green', 'red'])
    axes[0, 0].set_title('Verified Purchase vs Review Authenticity')
    axes[0, 0].set_ylabel('Count')
    axes[0, 0].legend(['Genuine', 'Fake'])
    
    # Reviewer Total Reviews vs Fake
    axes[0, 1].scatter(df['Reviewer_Total_Reviews'], df['Is_Fake'], alpha=0.5, c=df['Is_Fake'], cmap='RdYlGn_r')
    axes[0, 1].set_title('Reviewer Activity vs Review Authenticity')
    axes[0, 1].set_xlabel('Total Reviews by Reviewer')
    axes[0, 1].set_ylabel('Is Fake')
    
    # Rating vs Authenticity
    rating_fake = df.groupby('Rating')['Is_Fake'].mean()
    axes[1, 0].bar(rating_fake.index, rating_fake.values, color='steelblue')
    axes[1, 0].set_title('Fake Review Percentage by Rating')
    axes[1, 0].set_xlabel('Rating')
    axes[1, 0].set_ylabel('Proportion of Fake Reviews')
    
    # Helpfulness vs Authenticity
    axes[1, 1].scatter(df['Review_Helpfulness'], df['Is_Fake'], alpha=0.5, c=df['Is_Fake'], cmap='RdYlGn_r')
    axes[1, 1].set_title('Review Helpfulness vs Authenticity')
    axes[1, 1].set_xlabel('Helpfulness Score')
    axes[1, 1].set_ylabel('Is Fake')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/fake_review_metadata_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Visualizations generated successfully!")

def save_model_results(results):
    """Save model results to CSV"""
    results_data = []
    for model_name, metrics in results.items():
        results_data.append({
            'Model': model_name,
            'Accuracy': round(metrics['accuracy'], 4),
            'Precision': round(metrics['precision'], 4),
            'Recall': round(metrics['recall'], 4),
            'F1_Score': round(metrics['f1'], 4),
            'AUC': round(metrics['auc'], 4)
        })
    
    df_results = pd.DataFrame(results_data)
    df_results.to_csv('/home/ubuntu/fake_review_model_results.csv', index=False)
    print("\nModel Results:")
    print(df_results)

def main():
    print("Generating synthetic review data...")
    df = generate_review_data()
    
    print("Training classification models...")
    results, X_test, y_test, vectorizer = train_classification_models(df)
    
    print("Generating visualizations...")
    generate_visualizations(df, results, X_test, y_test)
    
    print("Saving model results...")
    save_model_results(results)
    
    print("\nFake Review Detection System completed successfully!")

if __name__ == "__main__":
    main()
