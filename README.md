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

Conclusion: While the results were acceptable, it seems that topic modelling in 
anything but trivial texts is still no easy feat. This, in my opionion, is due to the
fact that topic modelling is not used by individuals as much as by large organizations (likely for advertising purposes).
Thus, the few open-source projects that there are, are not sufficiently maintained and
can be very frustating to use. For highly experienced users this will not be a problem, but it certainly
limits how many users are going to be able to use this technique.

This is in contrast to other tasks which are used by individuals and small organizations
such as making web-pages. There are dozens of amazing, well-maintained web-frameworks with great documentation
that just work.

Outlook: Unless a white knight leaks Google's and/or Facebook's NLP libraries,
we will just have to wait that NLP and especially topic modelling go more
mainstream for it to become simples and thus more accessible.
