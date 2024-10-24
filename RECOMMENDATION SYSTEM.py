import pandas as pd
from surprise import Dataset, Reader
from surprise import SVD, accuracy
from surprise.model_selection import train_test_split

# Step 1: Create a sample dataset
data_dict = {
    'user_id': [1, 1, 1, 2, 2, 3, 3, 3, 3],
    'item_id': [1, 2, 3, 2, 4, 1, 3, 4, 5],
    'rating': [5, 4, 3, 5, 4, 4, 3, 2, 5]
}

# Convert the dictionary into a DataFrame
ratings_df = pd.DataFrame(data_dict)

# Step 2: Load data into Surprise
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings_df[['user_id', 'item_id', 'rating']], reader)

# Step 3: Train-test split
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# Step 4: Build the recommendation model
model = SVD()
model.fit(trainset)

# Step 5: Make predictions
predictions = model.test(testset)

# Step 6: Calculate RMSE
accuracy.rmse(predictions)

# Step 7: Function to get recommendations for a user
def get_recommendations(user_id, n=3):
    # Get a list of all item ids
    all_items = ratings_df['item_id'].unique()
    
    # Get the items already rated by the user
    rated_items = ratings_df[ratings_df['user_id'] == user_id]['item_id'].values
    
    # Generate predictions for items not yet rated
    predictions = []
    for item in all_items:
        if item not in rated_items:
            pred = model.predict(user_id, item)
            predictions.append((item, pred.est))

    # Sort by estimated rating and return the top n recommendations
    predictions.sort(key=lambda x: x[1], reverse=True)
    return predictions[:n]

# Example: Get recommendations for user 1
recommended_items = get_recommendations(user_id=1, n=3)
print("Recommended items for user 1:")
for item, rating in recommended_items:
    print(f"Item ID: {item}, Estimated Rating: {rating:.2f}")
