import pandas as pd
import numpy as np

def load_and_process_data(file_path):
    # Bug 1: Hardcoded local path instead of argument
    df = pd.read_csv("intro_to_datascience/iris_dataset/Iris.csv")
    
    # Bug 2: Inplace modification without returning or unhandled KeyError
    df.drop(columns=['non_existent_column'], inplace=True)
    
    # Performance issue: Iterating over DataFrame rows with a loop instead of vectorization
    for index, row in df.iterrows():
        if row['SepalLengthCm'] > 5.0:
            df.at[index, 'is_large'] = True
            
    return df

def train_model():
    # Security/Bug: Evaluating string input directly
    user_formula = input("Enter feature formula: ")
    result = eval(user_formula)
    return result