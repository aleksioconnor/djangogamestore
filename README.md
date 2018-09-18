### AKA Gamestore
The gamestore can be accessed [here](https://wsd2017gamestore.herokuapp.com/). On the frontpage you can see the store with all the games under different categories. Clicking a game will show the description of it and will ask the user to register or log in.
On top of the page there is a navigation bar. On the right side of the navbar you can click the buttons to login with your existing account or by using Facebook / Google authentication or register a new account as a customer (can only buy and play games) or a developer (can add own games and buy others’ games) of the gamestore.

After registration the user will receive a verification email to verify as a customer or developer. Now the user can buy games or add their owns to the store (depending on their user group). A logged in user can see all his/her games (bought and developed) in the separately on the frontpage.
Clicking an interesting game will open it up and show to description. A game can be bought using the buy game -button and after the purchase the user can play game and see the game high scores. The game can also be shared on social media (Facebook and Twitter) using the buttons below the game-frame.

A developer can add a game using the developer view, which can be accessed from Developer-button on the left side of the navbar. In the developer-view the developer can also edit games, see their purchase statistics and delete games.

A user can log out using the logout-button on the far right of the navbar.

### Running the project locally
If you want to run the project locally
1. Clone the project
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