from sklearn.feature_extraction.text import CountVectorizer as CV
from sklearn.linear_model import LogisticRegression as Reg
from sklearn.metrics import accuracy_score as acc
from sklearn.model_selection import train_test_split as train
import re
import pickle
import os

train_data_directory = r'C:\Users\Dolcevice\Documents\GitHub\TwitterAggregateSolution\common\Jupyter\Train_Data\aclImdb' \
                       r'\movie_data\full_train.txt'
test_data_directory = r'C:\Users\Dolcevice\Documents\GitHub\TwitterAggregateSolution\common\Jupyter\Train_Data\aclImdb' \
                      r'\movie_data\full_test.txt'
# Create containers
train_container = []
test_container = []

# Append contents into the containers
for line in open(train_data_directory, 'r', encoding='utf-8'):
    train_container.append(line.strip())
for line in open(test_data_directory, 'r', encoding='utf-8'):
    test_container.append(line.strip())

# Clean training data
REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])")
train_clean = [REPLACE_NO_SPACE.sub("", line.lower()) for line in train_container]
test_clean = [REPLACE_NO_SPACE.sub("", line.lower()) for line in test_container]

# Vectorize as binary since we are dealing with true/false data
cv = CV(binary=True)
cv.fit(train_clean)  # Fit the count vectorizer using the training data
X = cv.transform(train_clean)
X_test = cv.transform(test_clean)

# Classifier
# The first 12500 are positive and others are negative
target = [1 if i < 12500 else 0 for i in range(25000)]
X_train, X_val, y_train, y_val = train(X, target, train_size=0.75)

# Logistic Regression
# for c in [0.01, 0.05, 0.25, 0.5, 1]:
#    lr = Reg(C=c)
#    lr.fit(X_train, y_train)
#    print('Accuracy for c=%s: %s' % (c, acc(y_val, lr.predict(X_val))))
# C = 0.05 was the optimal constant

# Create a final model
final_model = Reg(C=0.05, n_jobs=-1)
final_model.fit(X, target)

# Save final model
os.remove('logreg_model.sav')
pickle.dump(final_model, open('logreg_model.sav', 'wb'))
