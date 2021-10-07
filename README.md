# emilio_kuhlmann_fp

Results of Harry Potter topic modelling:
![alt text](https://github.com/mcmiloy/emilio_kuhlmann_fp/blob/main/topics.png)


Motivation:
Topic modelling is essentially forming clusters of related words into topics within a text.
This could be useful to very roughly summarize a text or also to compare it to others by checking
similarities between detected topics.
I chose Harry Potter because I know the book and so could compare the output with what I would expect.
It is also a challenge,given how the story is a lot more complicated and entangled than children's books
often used for such projects.

Strengths: The algorithm produces topics that 
a) make sense, comparing it with my knowledge of the text
b) cover a broad spectrum
c) do not overly overlap

Weaknesses: The algorithm breaks down when removing propper nouns.
I have tinkered with every setting and simply do not understand why it happens.
The results can still be improved, to produce even more comprehensive topics.

Difficulties: It is very difficult to get everything running.
A lot of hours were spent on configuring versions and setting up environment variables.
Unfortunately I could not find a library that makes topic modelling more seamless than gensim.

The main algorithm is located in basic_nlp.py.
Several Jupyter-notebooks used for tests are clearly labeled, as well as 
a notebook for turning the final results into world clouds.
