def spending_insights(df):
    total = df['Amount'].sum()
    category_totals = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)

    insights = []
    for category, amount in category_totals.items():
        percent = (amount / total) * 100
        if percent > 30:
            insights.append(f"⚠️ You spend {percent:.1f}% on '{category}'. Try to cut down.")
        elif percent < 5:
            insights.append(f"✅ You're doing great with '{category}'!")
    return insights
