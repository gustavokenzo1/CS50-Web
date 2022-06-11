# Final Project

# Ride

For my Final Project, much like CS50x, I had trouble coming up with an idea, and I was in a bit of a rush, since my college classes would start in about a week. One of the problems that showed up after 2 years of remote classes was transportation, since I live about 30 miles from campus, and would take 2 hours just to get there by bus. So, I had the idea of merging those two problems, and creating a web app that allows students to create a ride, and then share it with others. This would allow users who don't have cars to get to campus faster, and also share gas prices, so it becomes a cheaper solution from both sides.

Prior to submitting CS50x's final project, I was already learning about React, so that's what I decided to use for this project. One of the differences was that I used the Create React App (CRA) template, instead of doing everything manually, just like it was taught in CS50w. This led to some difficulties, so I ended up using React only for pages that didn't need to send information (because Django's requirement of the CSRF token), and pure JavaScript + HTML for the rest. This ended up being a good opportunity to learn the fundamentals of React, and what it does behind the scenes, since CRA already creates and references the DOM for us. So, to sum up, I used React, JavaScript, HTML (with the Django syntax), CSS for the frontend, and Django for the backend.

# Distinctiveness and Complexity

Diving more deeply into the app itself, the first page is a description of the project, with a Login button, as well as a Register button. Once you register and login, you are presented with a list of all the rides that have been created, and you can click on any of them to see more information about it. To create a Ride, you can click the button called "Offer a Ride", in which you can fill out the form with the departure, destination, schedule, seats and total price. You can also click the "My Rides" button, which will present the user a list of all rides they created, as well as all rides they are currently signed up for. Clicking on a ride will present the user with all the information of the ride, a chat in which every user that is interested can send messages (this allows everyone to communicate with each other and make a better plan, like a pick-up route), a list of interested people, a button to confirm interest in the ride, and a list of confirmed people. Only the creator of the ride can accept or decline an interested user. I couldn't quite make the chat completely interactive, because the receiver would have to reload the page, but I managed to make the sender not reload the page when sending the message. To solve the first problem, I thought of sending a GET request every few seconds, but that felt gimmicky and unecessarily heavy, and I couldn't think of another solution for now, but it's something I'll try to do in the future.

# Files Contents

In the project, we have a single Django app called "ride", along with the default stuff when you create e Django app. In views.py, we have all the back-end logic of the application. In urls.py we have all the urls for requisitions. In models.py we have 3 models: User, Ride and Message. In the templates/ride folder, we have all the html files that are used to create the front-end. In the static/ride folder, we have both JS and CSS files. The JS files contains the React part of the application, in which I took advantage mostly of the JSX combined with the useEffect and useState hooks.

# How to Run

With Django installed, you can first make the migrations of the database using the command:

    python manage.py makemigrations

Then, you can migrate the database using the command:

    python manage.py migrate

Then, you can run the server using the command:

    python manage.py runserver

# Conclusion

As someone who has been studying web development for the past months prior to enrolling in this course, the projects were quite fun to make, because they weren't hard but had their complexity, since I had been studying only React and NodeJS, and not Django. It was really cool to look more deeply into some concepts that other lectures don't really teach, so this was still a very insightful course. Much like CS50x made me understand the fundamentals of Computer Science and, therefore, made my life in college a LOT easier, I'm sure CS50w will have the same effect on the long run.
