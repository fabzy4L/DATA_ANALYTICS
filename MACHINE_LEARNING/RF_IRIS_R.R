# Load the iris dataset
data(iris)

# Split the dataset into training and testing sets
set.seed(123)
train_index <- sample(nrow(iris), 0.7 * nrow(iris))
train_data <- iris[train_index, ]
test_data <- iris[-train_index, ]

# Load the randomForest package
library(randomForest)

# Train the random forest model
model <- randomForest(Species ~ ., data = train_data)

# Make predictions on the test set
predictions <- predict(model, newdata = test_data)

# Evaluate the accuracy of the model
accuracy <- sum(predictions == test_data$Species) / nrow(test_data)
print(paste("Accuracy:", round(accuracy, 2)))
