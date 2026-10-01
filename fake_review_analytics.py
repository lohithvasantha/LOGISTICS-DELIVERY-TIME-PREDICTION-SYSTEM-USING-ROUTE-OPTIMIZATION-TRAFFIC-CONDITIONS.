"""
Fake Review Analytics Utilities
Detailed analysis and statistical reports for review systems
"""

import pandas as pd
import numpy as np

def generate_analytics():
    """Generate detailed fake review analytics"""
    
    # Load review data
    df = pd.read_csv('/home/ubuntu/fake_reviews_dataset.csv')
    
    # 1. Review Statistics
    stats = {
        'Total_Reviews': len(df),
        'Genuine_Reviews': len(df[df['Is_Fake']==0]),
        'Fake_Reviews': len(df[df['Is_Fake']==1]),
        'Fake_Percentage': round(len(df[df['Is_Fake']==1]) / len(df) * 100, 2),
        'Avg_Rating': round(df['Rating'].mean(), 2),
        'Avg_Review_Length': round(df['Review_Length'].mean(), 2),
        'Avg_Helpfulness': round(df['Review_Helpfulness'].mean(), 2),
        'Verified_Purchase_Ratio': round(df['Verified_Purchase'].mean(), 2)
    }
    
    stats_df = pd.DataFrame([stats])
    stats_df.to_csv('/home/ubuntu/fake_review_statistics.csv', index=False)
    
    # 2. Rating Distribution Analysis
    rating_analysis = df.groupby('Rating').agg({
        'Is_Fake': ['count', 'sum', 'mean']
    }).round(3)
    rating_analysis.columns = ['Total_Reviews', 'Fake_Count', 'Fake_Ratio']
    rating_analysis.to_csv('/home/ubuntu/fake_review_rating_analysis.csv')
    
    # 3. Reviewer Behavior Analysis
    reviewer_analysis = df.groupby('Reviewer_Total_Reviews').agg({
        'Is_Fake': ['count', 'mean'],
        'Rating': 'mean'
    }).round(3)
    reviewer_analysis.columns = ['Review_Count', 'Fake_Ratio', 'Avg_Rating']
    reviewer_analysis.to_csv('/home/ubuntu/fake_review_reviewer_behavior.csv')
    
    # 4. Review Length Analysis
    length_bins = pd.cut(df['Review_Length'], bins=5)
    length_analysis = df.groupby(length_bins).agg({
        'Is_Fake': ['count', 'mean'],
        'Review_Helpfulness': 'mean'
    }).round(3)
    length_analysis.columns = ['Total_Reviews', 'Fake_Ratio', 'Avg_Helpfulness']
    length_analysis.to_csv('/home/ubuntu/fake_review_length_analysis.csv')
    
    # 5. Verified Purchase Impact
    verified_analysis = df.groupby('Verified_Purchase').agg({
        'Is_Fake': ['count', 'mean'],
        'Rating': 'mean',
        'Review_Helpfulness': 'mean'
    }).round(3)
    verified_analysis.columns = ['Total_Reviews', 'Fake_Ratio', 'Avg_Rating', 'Avg_Helpfulness']
    verified_analysis.to_csv('/home/ubuntu/fake_review_verified_analysis.csv')
    
    # 6. Helpfulness Score Analysis
    helpfulness_bins = pd.cut(df['Review_Helpfulness'], bins=5)
    helpfulness_analysis = df.groupby(helpfulness_bins).agg({
        'Is_Fake': ['count', 'mean']
    }).round(3)
    helpfulness_analysis.columns = ['Total_Reviews', 'Fake_Ratio']
    helpfulness_analysis.to_csv('/home/ubuntu/fake_review_helpfulness_analysis.csv')
    
    # 7. Reviewer Age Analysis
    age_bins = pd.cut(df['Reviewer_Age_Days'], bins=5)
    age_analysis = df.groupby(age_bins).agg({
        'Is_Fake': ['count', 'mean'],
        'Rating': 'mean'
    }).round(3)
    age_analysis.columns = ['Total_Reviews', 'Fake_Ratio', 'Avg_Rating']
    age_analysis.to_csv('/home/ubuntu/fake_review_age_analysis.csv')
    
    # 8. Time Between Reviews Analysis
    time_bins = pd.cut(df['Time_Between_Reviews_Hours'], bins=5)
    time_analysis = df.groupby(time_bins).agg({
        'Is_Fake': ['count', 'mean']
    }).round(3)
    time_analysis.columns = ['Total_Reviews', 'Fake_Ratio']
    time_analysis.to_csv('/home/ubuntu/fake_review_time_analysis.csv')
    
    # 9. Correlation Analysis
    numeric_cols = ['Rating', 'Review_Length', 'Reviewer_Age_Days', 'Reviewer_Total_Reviews',
                    'Reviewer_Avg_Rating', 'Review_Helpfulness', 'Time_Between_Reviews_Hours', 
                    'Verified_Purchase', 'Is_Fake']
    correlation = df[numeric_cols].corr().round(3)
    correlation.to_csv('/home/ubuntu/fake_review_correlation_matrix.csv')
    
    # 10. Authenticity Categories
    df['Authenticity_Category'] = pd.cut(df['Is_Fake'], 
                                          bins=[-0.1, 0.5, 1.1],
                                          labels=['Genuine', 'Fake'])
    category_dist = df['Authenticity_Category'].value_counts()
    category_df = pd.DataFrame({
        'Category': category_dist.index,
        'Count': category_dist.values,
        'Percentage': (category_dist.values / len(df) * 100).round(2)
    })
    category_df.to_csv('/home/ubuntu/fake_review_authenticity_categories.csv', index=False)
    
    print("Analytics generated successfully!")
    print("\nReview Statistics:")
    print(stats_df)
    print("\nRating Analysis:")
    print(rating_analysis)
    print("\nReviewer Behavior Analysis:")
    print(reviewer_analysis.head())

if __name__ == "__main__":
    generate_analytics()
