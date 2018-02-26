# AKA Gamestore

## Team
  * 426736 Aleksi O'Connor
  * 530347 Katri Saarinen
  * 544692 Alan Pirdil

## Final Submission

### Functional Requirements
Below are described all the functional requirements we have implemented.

#### Minimum functional requirements
User can register as either a player or a developer. Players can buy games and then play them, see game high scores and record their scores to the high score listing.
Developers can add games for everyone to buy and play, see game sale statistics, edit and delete games.

#### Authentication
Registering, logging in and logging out works for both developers and players. These are implemented using Django Auth. Email verification also works and actually sends a proper email to the user with a verification link. The verification has to be done in order for the user to be able to buy or add games.

#### Basic player functionalities
Games can be bought using the course's mockup payment service - success, error and cancel -cases work. After purchase, the games can be played and the game/service works as wanted (game-state can be saved and loaded, high score is received, frame-size is received from the settings).
User can only play a game that is bought (or self-developed) and if the user is logged in.
Games are listed in specific categories in the front page and own (bought or developed) games are listed in the beginning of the front page.

#### Basic developer functionalities
A (logged in) developer can add a new game (name, price, url, description). Own (and only own!) developed games can be edited or deleted and the game sale statistics (when the game has been bought) can be seen.

#### Game/service interaction
When a player finishes playing a game (or presses 'submit score'), the message is sent as wanted. Messages from service to the game are implemented as well.
The game high scores are served via RESTful API. The gameview shows 5 highest scores made by anyone that has played the game.

#### Quality of Work
The application is structured in a meaningful way and functions are commented properly. DRY-principle is followed and Model-View-Template separation is used.
Meaningful tests are created to make sure that the application works as wanted and is required. Tests can be ran using the ```python manage.py test``` -command.

#### Non-functional requirements
Project plan was created in the beginning of the project and can be found in the below section.
Documentation is done according to the instructions and requirements.

#### Save/load and resolution feature
The service of our gamestore supports saving and loading for games with the simple message protocol described in Game Developer Information.

#### 3rd party login
Users can also log in to the system using by using Google or Facebook authentication.

#### RESTful API
RESTful API is used to serve game highscores.

#### Own game
Our own club-game is made with JavaScript and it communicates with the service as wanted (high score, save, load). Game is included in the repository and can be found with [this url](https://wsd2017gamestore.herokuapp.com/static/clubescape/index.html).

#### Mobile Friendly
Our application works well with both traditional computers and mobile devices. Specific attention is paid to make the application work well also with mobile devices. It works with devices with varying screen width and is usable with touch based devices.

#### Social media sharing
Games can be shared in two social media sites - Facebook and Twitter. Metadata is added correctly, so when sharing, game name, description an image are shown and the game can be accessed with the (correct) link.

### Dividing work between team members
During this project we did not want to give the members of team one big specific part that they would handle alone – we all wanted to learn and understand all parts of the project. We met up every Tuesday and went through the things we would need to do each week - these tasks were given to different members of the team and some tasks were also completed in pairs. The first week we worked mainly together from Aleksi’s computer since starting the project could be done best using only one computer. Working in pairs allowed us to discuss the current tasks more and understand more deeply what is the current problem and what is the best solution to it – it also makes it a bit more difficult to define who did what. A good example of a task given to a member could have been “add the iframe-functionality to gameview and handle the different messages received from it” or “add the payment functionality to the gameview so users can buy games”. The tasks were divided evenly between team members each week and all in all everyone completed approximately the same amount of work for the project.

#### Aleksi
* User authentication
* Basic templates (base etc.)
* Lots of configuration
* REST-functionalities
* AJAX-functionalities
* Handling Heroku
* Game categories
* Some authorization
* Defining models and templates
* Testing

#### Katri
* Games to the database -functionality
* Game statistic -functionality
* Basic login / logout functionality
* Gameview - added iFrame, read the messages received from it and added required functionality (score, state, settings etc.)
* Whole payment functionality (payment + required views and templates)
* Social media -sharing
* Authorization
* Styling (navigation and some random parts)
* Defining models and templates
* Testing
* Documenting the project
* OAuth (Google + Facebook)

#### Alan
* Developer functionality
* Email-verification
* User profiles
* Most styling
* Some authorization
* Defining models and templates
* Editing and deleting games (for developers)

### AKA Gamestore
The gamestore can be accessed [here](https://wsd2017gamestore.herokuapp.com/). On the frontpage you can see the store with all the games under different categories. Clicking a game will show the description of it and will ask the user to register or log in.
On top of the page there is a navigation bar. On the right side of the navbar you can click the buttons to login with your existing account or by using Facebook / Google authentication or register a new account as a customer (can only buy and play games) or a developer (can add own games and buy others’ games) of the gamestore.

After registration the user will receive a verification email to verify as a customer or developer. Now the user can buy games or add their owns to the store (depending on their user group). A logged in user can see all his/her games (bought and developed) in the separately on the frontpage.
Clicking an interesting game will open it up and show to description. A game can be bought using the buy game -button and after the purchase the user can play game and see the game high scores. The game can also be shared on social media (Facebook and Twitter) using the buttons below the game-frame.

A developer can add a game using the developer view, which can be accessed from Developer-button on the left side of the navbar. In the developer-view the developer can also edit games, see their purchase statistics and delete games.

A user can log out using the logout-button on the far right of the navbar.

### Running the project locally
If you want to run the project locally
1. Clone the project from GitLab using SSH: ```git@version.aalto.fi:pirdila1/wsd2017-gamestore.git```
2. Activate Python environment using command ```source ~/djangoenv/bin/activate```
3. Run command ```pip install -r requirements.txt```
4. Migrate using command ```python manage.py migrate```
5. Collect static using command ```python manage.py collectstatic```
6. To add game categories and user-types to the gamestore
  1. Open python shell using command ```python manage.py shell```
  2. Import Category-model ```from store.models import Category```
  3. add wanted categories ```Category.objects.create(name='CATEGORY-NAME')```
  4. add correct groups ```from django.contrib.auth.models import Group``` ```Group.objects.create(name="Developer")``` ```Group.objects.create(name="Player")```
7. Open the gamestore locally using command ```python manage.py runserver```

When adding new users to the gamestore, the the link in the email must be changed from https -> http, since Heroku is using a secure connection, but localhost is not.

## Project Plan
### Goal
In this project, we will build an online gamestore utilizing django and jQuery. All members of our group have previous experience in front-end development, but no prior experience in developing with django. Learning goals include but are not restricted to learning the django framework, gain a deeper understanding of the jQuery framework, learn to use payment systems within a web project and learn to work efficiently with version control and small scale development projects. Technical goals include developing a stable, secure and easy-to-use online game store. We also plan to make the web platform visually compelling and user friendly. We have little experience with deploying to Heroku, so we look forward to working with the platform.

### Development and plans
Our aim is to implement all mandatory features and in addition most of the extra features.

#### Technology stack
The project will generally utilize JavaScript, jQuery HTML, CSS and Django. In addition, we will be using the node packet manager to allow the use of Gulp. Gulp will be used to automate the build process. We will test the compatibility of our stack with Heroku during the hello-world deployment and make further changes if necessary.

#### Models
Our initial models include at least Player, Developer, Games. These models may need renaming, but they give a good general sign of the direction we are heading. Player's fields would include basic information (name, age, email, etc.), games purchased and their high scores to these games. Developers would have the same basic information but instead have games they have made listed in the fields. Our initial models include a Game model, but we will evaluate its necessity during the project. This Game models' fields would most importantly include basic information (name, developer who has made it, url, price) and global high score.

#### Outline of user interface
We have come up with an initial outline of what our web-game store front page will look like.


![layout](https://version.aalto.fi/gitlab/pirdila1/wsd2017-gamestore/raw/fd71f894856efb5c99a8edc5c3f004acedf4921c/layout.png)

#### Security
Our security measures include sanitizing user inputs and keeping the input fields fairly simple. We identify SQL injection, Javascript and jQuery scripts and authentication controlling as the biggest risks we need to handle in terms of Security.

### Process and time schedule
#### Time schedule
We will begin on the project on 9.1 at 13:30. During the christmas holidays all group members will familiarize themselves with the django framework so we can begin efficient development on the 9.1. We will begin by configuring the project and deploying a simple hello-world application to Heroku. Below is pictured a rough outline of our project plan:

| Week | Goal | Description |
| ---- | ---- | ----------- |
| 2    | Configuration, initial deployment, simple communication between backend and frontend | |
| 3    | Backend | Work with API points and get backend up and running smoothly, configure basic database structure |
| 4    | Authentication and payment system | Authentication, basic player and developer functionalities, payment system |
| 5    | MVP | Achieve a MVP version of the application to enable future product development |
| 6    | Further development phase | Implement additional features, polish UI and testing |
| 7    | Further development phase | Implement additional features, polish UI, testing and writing final documentation |
| 8    | Returning the project | Deadline at 19.2 midnight (end of period three) |

#### Process
We will work using a backlog and assign tasks to team members. We will be using feature branches throughout the project, applying peer reviewing before merging features into the master branch. We will meet weekly to review changes, log process and plan for the future week. Communication will be enabled through instant messaging in addition to face-to-face meetings.

### Testing
We will be implementing unit tests to critical functions throughout the project. A testing framework is under consideration and if implemented we are aiming for at least a 50% code coverage - we are not applying full unit testing due to limited resources. We will also apply penetration testing on week 6 to ensure our project meets the required security standards. The user interface will be subject to iterative testing and will be developed throughout the project.

### Risk analysis
We are concerned about the project not progressing according to our schedule. Due to the nature of software projects, we are prepared for some delays or unexpected problems. We acknowledge that we are faced with a tight schedule, and we might have to compromise some features we wish to implement. To prevent delays affecting the outcome of our project we will review progress in weekly meetings.
