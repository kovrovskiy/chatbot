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

	model = LogisticRegression() # Settings
	model.fit(vecX, y)
or

	model = RandomForestClassifier(n_estimators = 500, min_samples_split=3)
	model.fit(vecX, y)