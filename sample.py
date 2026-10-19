import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score



data={'a': [-5,-4,-3,-2,-1,-4,1,-3,0,-2,2,3,4,5,1,3,-1,2,4,0], 'b': [-3,-2,-4,-1,-3,1,-4,0,-2,-3, 3,4,2,3,2,-1,4,1,0,3] ,'c': [-1]*10 + [1]*10  }
df=pd.DataFrame(data)
X_train,X_test,Y_train,Y_test=train_test_split(df[['a','b']],df['c'],test_size=0.2,random_state=42) 
model = DecisionTreeClassifier(    max_depth=3, random_state=42)
model.fit(X_train,Y_train)
print("Accuracy:", accuracy_score(Y_test, model.predict(X_test)))
plt.figure(figsize=(12, 7))

plot_tree(
    model,
    feature_names=['a', 'b'],
    class_names=['Negative (-1)', 'Positive (+1)'],
    filled=True,
    rounded=True,
    fontsize=11
)
