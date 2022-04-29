# Chatbot
The ChatBot with artificial intelligence

# Vectorizer
Vectorizer turns texts into vectors (sets of numbers)

	"mom" = 1, "cool" = 2, "soup" = 3, "frame" = 4
	-mom cooling soap the frame => [1,2,3,4]
	-cool mom soap frame => [2,1,4,3]
	-soap  => [3,0,0,0]

	vectorizer = CountVectorizer()
	vectorizer.fit(x)  # Learns to convert these specific texts into vectors
	vecX = vectorizer.transform(x)

# Train the model (algorithm, settings)

	from sklearn.linear_model import LogisticRegression
	model = LogisticRegression() # Settings
	model.fit(vecX, y)
or

	model = RandomForestClassifier(n_estimators = 500, min_samples_split=3)
	model.fit(vecX, y)

# Check model quality

	model.score(vecX, y)
	
# Save model to file

	import pickle
	f = open("bot_model.class", "wb")
	pickle.dump(model, f)
	
# Search for the ideal model

	from sklearn.model_selection import GridSearchCV
	ideal_model = RandomForestClassifier()
	param = {
		"n_estimators": [60, 140],
		"criterion": ["gini", "entropy"],
	}
	cv = GridSearchCV(ideal_model, param)
	cv.fit(vecX, y)