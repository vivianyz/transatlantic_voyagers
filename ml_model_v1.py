# -*- coding: utf-8 -*-
"""ml_model_v1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/vivianyz/transatlantic_voyagers/blob/main/ml_model_v1.ipynb
"""

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from flask import Flask, request, render_template

"""# Joining Tables and Preparing Data
To build a comprehensive dataset for analysis or machine learning, data from multiple related tables must be combined. This process involves joining tables on shared keys or identifiers and selecting relevant columns for the task at hand.
1. **Load CSV Files**: Start by loading the data from CSV files into pandas DataFrames. Each CSV file typically represents a table in your dataset, such as `ttav_passengers.csv`, `ttav_voyages.csv`, `ttav_routes.csv`, and `ttav_occupations.csv`.

2. **Join Tables on Unique IDs**:
   - **Passengers and Voyages**: Join the `ttav_passengers` table with the `ttav_voyages` table on the `MID` column to combine voyage information with passenger details.
   - **Voyages and Routes**: Further join the above result with the `ttav_routes` table on the `routeID` to include routing details.
   - **Comprehensive Join**: Finally, join the combined table with the `ttav_occupations` table on the `occID` to add occupation information for each passenger.

3. **Select Relevant Columns**: From the fully joined table, select columns essential for the analysis or machine learning model. In this case, columns like `MID`, `routeID`, `age`, `sex`, `occID`, and `port_arv` are chosen for predicting the port of arrival based on passenger attributes.

4. **Handle Missing Values**: Before proceeding with analysis or model training, ensure to handle any missing values in the selected columns to maintain data integrity and model accuracy.

5. **Final Combined DataFrame**: The result of these steps is a comprehensive DataFrame that integrates information from multiple sources, ready for data analysis or as input to a machine learning model.
"""

# Set the path to the dataverse_files directory
path_to_files = './dataverse_files/'

# Load the CSV files into pandas DataFrames
passengers_df = pd.read_csv(f'{path_to_files}ttav_passengers.csv')
voyages_df = pd.read_csv(f'{path_to_files}ttav_voyages.csv')
routes_df = pd.read_csv(f'{path_to_files}ttav_routes.csv')
occupations_df = pd.read_csv(f'{path_to_files}ttav_occupations.csv')

# Perform the joins
passengers_voyages_df = pd.merge(passengers_df, voyages_df, on='MID')
voyages_routes_df = pd.merge(passengers_voyages_df, routes_df, on='routeID')
final_df = pd.merge(voyages_routes_df, occupations_df, on='occID')

# Select only the required columns
final_df = final_df[['MID', 'routeID', 'age', 'sex', 'occID','occ_nm','occ_ctg','occ_grp','port_arv']]
#Display the first few rows of the final DataFrame
final_df.head()

"""# Data Preprocessing
Before building the machine learning model, the dataset requires preprocessing to ensure it's in the right format for the model to interpret. This includes handling missing values and encoding categorical variables.
1. **Encode Categorical Variables**: Convert categorical variables into a format that can be provided to machine learning algorithms. This step includes encoding the `sex` column using label encoding.
2. **Handle Missing Values**: Use `SimpleImputer` to fill in missing values. For numerical columns like `age` and `occID`, missing values are replaced with the median of the column.
3. **Prepare Features and Target Variable**: Select the relevant columns (`age`, `sex`, `occID`) as features (X) and the column to predict (`port_arv`) as the target variable (y).
4. **Split the Dataset**: Divide the dataset into training and testing sets to evaluate the model's performance on unseen data.

"""

# Encode the 'sex' column if it's categorical. If it's numeric, you can skip this step.
label_encoder = LabelEncoder()
final_df['encoded_sex'] = label_encoder.fit_transform(final_df['sex'].astype(str))

# Prepare features and target variable
X = final_df[['age', 'encoded_sex', 'occID']].copy()  # Work on a copy to avoid changing the original DataFrame
y = final_df['port_arv']

# Impute missing values for 'age' and 'occID' (assuming they are numerical)
# Adjust according to your dataset's needs
imputer = SimpleImputer(strategy='median')
X[['age', 'occID']] = imputer.fit_transform(X[['age', 'occID']])

# Now, we also need to ensure that 'port_arv' is encoded
y = label_encoder.fit_transform(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Decision Tree Model
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
decoded_prediction = label_encoder.inverse_transform(y_pred)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(decoded_prediction)
print(classification_report(y_test, y_pred))

# Now, your model is ready to make predictions

final_df.head()

import pandas as pd

# Assuming final_df is your DataFrame and it has a 'port_arv' column

# Count the frequency of each distinct value in 'port_arv'
port_arv_counts = final_df['port_arv'].value_counts()

# Calculate the percentage of each distinct value
port_arv_percentages = final_df['port_arv'].value_counts(normalize=True) * 100

# Combine both counts and percentages into a single DataFrame for easy viewing
port_arv_summary = pd.DataFrame({
    'Count': port_arv_counts,
    'Percentage': port_arv_percentages
})

# Display the summary DataFrame
print(port_arv_summary)

"""### Model Training and Evaluation

After preprocessing the data, the next step is to train the decision tree model and evaluate its performance.

1. **Train the Decision Tree Model**: A `DecisionTreeClassifier` is used to fit the model on the training data. The model learns to predict the `port_arv` based on the features `age`, `sex`, and `occID`.
2. **Evaluate the Model**: Use the testing set to evaluate the model's accuracy and overall performance. This step involves comparing the predicted values of `port_arv` against the actual values in the test dataset.
3. **Accuracy and Classification Report**: The model's performance is summarized through the following metrics, providing insight into its predictive capabilities and areas for improvement:

    - **Accuracy**:
        - *Definition*: The ratio of correctly predicted instances to the total instances in the dataset.
        - *Interpretation*: High accuracy means that the model correctly predicted many of the outcomes. However, it might not be reliable in the presence of class imbalance.
        - *Example*: If a model correctly predicts 950 out of 1000 instances, its accuracy is 95%.
    
    - **Precision**:
        - *Definition*: The ratio of true positive predictions to the total positive predictions made for a given class.
        - *Interpretation*: Precision is important when the cost of a false positive is high.
        - *Example*: If a model predicts 100 instances as class 1, but only 90 are actually class 1, the precision for class 1 is 90%.

    - **Recall**:
        - *Definition*: The ratio of true positive predictions to the total actual positives for a given class.
        - *Interpretation*: Recall is crucial when the cost of a false negative is high.
        - *Example*: If there are 120 actual instances of class 1 and the model correctly identifies 90, the recall for class 1 is 75%.

    - **F1-Score**:
        - *Definition*: The harmonic mean of precision and recall.
        - *Interpretation*: The F1-score is useful when you want to find a balance between precision and recall.
        - *Example*: If the precision is 90% and recall is 75% for class 1, the F1-score would be approximately 82%.

    - **Support**:
        - *Definition*: The number of actual occurrences of the class in the specified dataset.
        - *Interpretation*: Indicates the prevalence of each class in the dataset. Useful for identifying class imbalance.
        - *Example*: If class 1 appears 120 times in the dataset, the support for class 1 is 120.

    - **Macro Average**:
        - *Definition*: The average of the metric computed independently for each class.
        - *Interpretation*: Treats all classes equally, not considering their support.
        - *Example*: If there are five classes, the macro average precision would be the average of the precision scores for each class.

    - **Weighted Average**:
        - *Definition*: The average of the metric weighted by the support of each class.
        - *Interpretation*: Accounts for class imbalance by weighting the metric by the number of true instances for each class.
        - *Example*: If class 1 has a support of 120 and a precision of 90%, while class 2 has a support of 30 and a precision of 60%, the weighted average precision would give more importance to the precision of class 1.

# Why Use a Decision Tree Model

Using a Decision Tree model for predicting `port_arv` based on features like `age`, `sex`, and `occID` from the dataset offers several advantages, making it a suitable choice for our scenario:

## 1. Interpretability
Decision Trees are highly interpretable models. They allow an easy understanding of how decisions are made, showing clear decision paths from features to outcomes. This is beneficial for explaining model predictions.

## 2. Handling of Categorical Variables
Decision Trees can directly handle categorical variables, making them a convenient choice given that our dataset includes categorical features like `sex` and `occID`.

## 3. Non-linear Relationships
They are capable of capturing non-linear relationships between features and the target variable, accommodating complex patterns in data.

## 4. No Need for Feature Scaling
Unlike some other models, Decision Trees do not require input features to be scaled or normalized. This simplifies the data preprocessing steps.

## 5. Modeling Complex Decision Boundaries
Decision Trees can model complex decision boundaries by learning a hierarchy of if-else questions, making them capable of understanding complicated relationships in the data.

## 6. Fast Prediction Time
After training, Decision Trees can make predictions quickly, as it only involves traversing the tree, which can be crucial for time-sensitive applications.

## Limitations
While Decision Trees have many benefits, they can be prone to overfitting, especially with complex data and without constraints on tree depth. Overfitting can be addressed by pruning the tree or using ensemble methods like Random Forests, which improve generalization by averaging multiple trees' predictions.

In conclusion, a Decision Tree is an excellent starting point due to its interpretability, ease of handling categorical data, and flexibility in modeling complex relationships. Nonetheless, it's essential to assess its performance against other models and consider ensemble techniques if needed.
"""

# Train the Decision Tree Model
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Now, the model is ready to make simulations

joblib.dump(model, 'decision_tree_model.joblib')

from sklearn.preprocessing import LabelEncoder

# Assuming 'sex' and 'port_arv' are columns in final_df
sex_encoder = LabelEncoder()
port_arv_encoder = LabelEncoder()

# Fit and transform the columns
final_df['sex_encoded'] = sex_encoder.fit_transform(final_df['sex'])
final_df['port_arv_encoded'] = port_arv_encoder.fit_transform(final_df['port_arv'])

# Now, you use 'sex_encoded' and 'port_arv_encoded' for training the model...
# After training, save your model and encoders:
joblib.dump(sex_encoder, 'sex_encoder.joblib')
joblib.dump(port_arv_encoder, 'port_arv_encoder.joblib')

from sklearn.preprocessing import LabelEncoder

# Assuming 'sex' and 'port_arv' are columns in final_df
sex_encoder = LabelEncoder()
port_arv_encoder = LabelEncoder()

# Fit and transform the columns
final_df['sex_encoded'] = sex_encoder.fit_transform(final_df['sex'])
final_df['port_arv_encoded'] = port_arv_encoder.fit_transform(final_df['port_arv'])

# Now, you use 'sex_encoded' and 'port_arv_encoded' for training the model...
# After training, save your model and encoders:
joblib.dump(sex_encoder, 'sex_encoder.joblib')
joblib.dump(port_arv_encoder, 'port_arv_encoder.joblib')

import tkinter as tk
from tkinter import ttk
import joblib
import pandas as pd

port_arv_encoder = joblib.load('port_arv_encoder.joblib')


# Map occupation names to IDs
occ_nm_to_id = occupations_df.set_index('occ_nm')['occID'].to_dict()
occ_names = list(occ_nm_to_id.keys())

# Map 'sex' to 'encoded_sex'
sex_to_encoded = final_df[['sex', 'encoded_sex']].drop_duplicates().set_index('sex')['encoded_sex'].to_dict()

def predict():
    age = int(age_entry.get())
    sex = sex_combobox.get()
    occ_nm = occ_nm_combobox.get()
    occID = occ_nm_to_id[occ_nm]

    # Encode sex
    encoded_sex = sex_to_encoded[sex]
    #print(encoded_sex)

    # Predict using the model
    prediction = model.predict(pd.DataFrame([[age, encoded_sex, occID]], columns=['age', 'encoded_sex', 'occID']))

    # Decode the port_arv prediction
    decoded_port_arv = port_arv_encoder.inverse_transform(prediction)[0]

    result_label.config(text=f"Simulated Port of Arrival: {decoded_port_arv}")

app = tk.Tk()
app.title("Arrival Port Simulation")

tk.Label(app, text="Please enter your age, sex, and occupation info:").pack()

tk.Label(app, text="Age:").pack()
age_entry = tk.Entry(app)
age_entry.pack()

tk.Label(app, text="Sex:").pack()
sex_combobox = ttk.Combobox(app, values=['M', 'F'])
sex_combobox.pack()

tk.Label(app, text="Occupation:").pack()
occ_nm_combobox = ttk.Combobox(app, values=occ_names)
occ_nm_combobox.pack()
predict_button = tk.Button(app, text="Simulate", command=predict)
predict_button.pack()

result_label = tk.Label(app, text="Port of Arrival will be shown here.")
result_label.pack()

app.mainloop()
