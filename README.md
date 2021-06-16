# Go Explore Website

## User Experience (UX)

### User Stories

### Design

#### Colour Scheme
- The three main colours used in the website are pink, light blue and dark blue.
- These colours were chosen because they complement each other well.

#### Typography
- The main font used throughout the website is PT Sans.
This font was chosen because it makes the content easy to read.
- Nothing You Could Do was used for the hero image headings to make them stand out.
- Sans Serif is the fallback font which is used in the event that the specified font fails to import into the website correctly.

#### Imagery
- The hero images were chosen because they give the user an idea of what they can expect to experience in each destination if they book a holiday there.

### Wireframes

### Entity Relationship Diagrams

The Entity Relationship Diagram shows details of each field in each model in the database and the relationships between the different models. They can be accessed [here](static/readme/entity_relationship_diagram.pdf).

## Features

### Existing Features

### Features Left To Implement

1. More Destinations
   - Add more destinations including from more countries and more holiday categories.

2. Flight and Holiday Package Capacity Limits
    - Add a capacity limits to the flights and packages model and add a date selection page where the user can only select dates with available capacity.

3. Different Prices on Different Dates
    - Add a prices model and functionality to search holidays by departure date.

4. Buy Now Pay Later Payment Option
    - Add a payment option where the customer can split the payment over a series of monthly payments. 

5. Add Paypal Payments Webhooks
    - Add webhooks for paypal payments to ensure that the booking is updated if the user closes the checkout page after payment has been approved but before the form has been submitted. 

6. Include Visa Information in Confirmation Email
    - Amend the confirmation email to include visa information for the relevant destination.

7. Manage Payment Methods from Profile
    - Add an additional page to the profile app where the user can add, update and delete their payment methods.

8. Amend Booking
    - Add functionality to the bookings page to be able to submit a request to amend a booking.

## Technologies Used

### Languages Used

1. [HTML5:](https://en.wikipedia.org/wiki/HTML5/)
   - HTML5 was used for the sturcture of the webpages.
2. [CSS3:](https://en.wikipedia.org/wiki/Cascading_Style_Sheets/)
   - CSS3 was used for the styling of the webpages.
3. [JavaScript:](https://en.wikipedia.org/wiki/JavaScript/)
   - JavaScript was used for the interactive features on the webpages.
4. [Python:](https://www.python.org/)
    - Python was used to communicate the database information to the browser.

### Frameworks, Libraries & Programs Used

1. [Bootstrap 5](https://getbootstrap.com/)
   - Bootstrap was used for the navbar, forms, butons, dropdowns, tabs, cards, tables and toasts. Bootstrap was also used for the grid which assists with the responsiveness of the website and for the styling.
2. [Material Design Bootstrap](https://mdbootstrap.com/)
    - The Material Design Bootstrap theme was used for the styling of the website.
3. [Hover.css](https://ianlunn.github.io/Hover/)
   - Hover.css was used for the hover effects on the social media icons.
4. [Font Awesome](https://fontawesome.com/)
   - Font Awesome was used throughout the website to enhance the user experience by adding icons.
5. [jQuery](https://jquery.com/)
   - JQuery was used throughout the website for the interactive features.
6. [Slick Slider](https://kenwheeler.github.io/slick/)
    - Slick Slider was used for the offers carousel, popular holidays slider and related holidays sliders. License is [here](slick_license.md).
7. [Gijgo](https://gijgo.com/)
    - Gijgo was used for the datepicker and datetime picker.
8. [JQuery.formset](https://github.com/nortigo/jquery-formset)
    - JQuery.formset was used to dynamically add rows to the formsets in the add holiday and edit holiday forms.
9. [Pytz](https://pypi.org/project/pytz/)
    - Pytz was used for the coverting of time zones.
10. [Stripe](https://stripe.com/docs/payments)
    - The Stripe API was used for the processing of card, Apple Pay and Google Pay payments.
11. [Paypal](https://developer.paypal.com/docs/checkout/)
    - The Paypal Smart Payment Button API was used for the processing of Paypal Payments.
12. [Django](https://www.djangoproject.com/)
    - Django was used for the accessing of the data models, the routing of the appliction, the messages and the templating.
13. [Django Allauth](https://django-allauth.readthedocs.io/en/latest/installation.html)
    - Django allauth was used for the authentication of users.
14. [Postgresql](https://www.postgresql.org/)
    - A postgresql database was used to store the data used in the project.
15. [Visual Studio Code](https://code.visualstudio.com/)
    - Visual Studio Code was used to write the code for this project and gitpod terminal was used to commit changes to Git and push them to GitHub.
16. [Git](https://git-scm.com/)
    - Git was the version control system used for this project.
17. [GitHub](https://github.com/)
    - GitHub is used to store the project's code and any other required files.
18. [Heroku](https://www.heroku.com/)
    - Heroku is used to host the deployed website.
19. [Amazon Web Services](https://aws.amazon.com)
    - An Amazon Web Services S3 bucket was used to host the images and static files used in the website
20. [Balsamiq](https://balsamiq.com/)
    - Balsamiq was used to create the wireframes during the design phase of the project.
21. [DB Diagram](https://dbdiagram.io/home)
    - DB Diagram was used to create the Entity Relationship Diagrams of the database.

## Testing

### Validation and Accessibility Testing

| Test                      | Outcome                                           |
| ------------------------- |--------------------------------------------------:|
| W3C Markup Validator      | No errors except for the django templating syntax |
| W3C CSS Validator         | No errors                                         |
| PEP8                      | No errors                                         |
| JSHint                    | No errors                                         |
| Lighthouse Accessibility  | TBC                                               |

### Testing User Stories from User Experience (UX) Section

### Manual Testing

### Further Testing

- The Website was tested on a variety of different web browsers including Google Chrome, Microsoft Edge, Safari and Firefox.
- The Website was also viewed on a number of different devices with a range of screen widths including an iMac, MacBook, iPad and iPhone.
- Family and friends were asked to review the site and documentation and identify any bugs or other issues that were affecting the user experience.

### Fixed Bugs

1. Many to Many fields in the Package form were not saving
    - Fixed an error in the code.

2. Non UK addresses were being populated to the wrong form fields by the address autocomplete
    - Restricted the autocomplete to UK addresses

3. Times were appearing in the wrong time zone
    - Added time zone fields to the flights model and added logic to the flight model save method to convert departure time and arrival time to UTC.

4. Itineraries were appearing in the wrong order on the holiday details pages
    - Added sorting by ID to the itineraries model meta class

5. All bookings were appearing on the bookings page, no matter how many
    - Used the slice filter in the template to restrict the number of bookings shown to 10.

6. Filters and sorting previously selected on the flights and holidays pages were not being re-applied when the user clicked the back button
    - Added a new entry to the browser's session history every time the filters or sorting are changed.

7. Payments made using Apple Pay or Google Pay were not being processed successfully
    - Fixed an error in the code.

8. The email address was not being saved when the profile was saved
    - Fixed an error in the code.

## Deployment

### Amazon Web Services S3 Bucket

The project's media and static files were stored in an Amazon Web Services S3 bucket using the following steps:

1. Log in to Amazon Web Services, enter "s3" into the search bar and click on the s3 result.
![Image of the s3 results](media/deployment/aws_1.png)
2. Click on the "create bucket" button.
![Image of the create bucket button](media/deployment/aws_2.png)
3. Enter a name for the bucket.
![Image of the create bucket page](media/deployment/aws_3.png)
4. Uncheck the "Block all public access" checkbox.
![Image of the create bucket page](media/deployment/aws_4.png)
5. Check the "I acknowledge that the current settings might result in this bucket and the objects within it becoming public" checkbox.
![Image of the create bucket page](media/deployment/aws_5.png)
6. Click on the "create bucket" button.
![Image of the create bucket button](media/deployment/aws_6.png)
7. Click on the "go-explore-1" bucket.
![Image of the buckets list](media/deployment/aws_7.png)
8. Click on the "properties" tab.
![Image of the properties tab](media/deployment/aws_8.png)
9. Scroll down to the "Static website hosting" section and click on the "edit" button.
![Image of the static website hosting section](media/deployment/aws_9.png)
10. Under "static website hosting" select the enable option.
![Image of the static website hosting page](media/deployment/aws_10.png)
11. Enter the index document and error document details.
![Image of the static website hosting page](media/deployment/aws_11.png)
12. Click on the "save changes" button.
![Image of the save changes button](media/deployment/aws_12.png)
13. Click on the "permissions" tab.
![Image of the permissions tab](media/deployment/aws_13.png)
14. Scroll down to the "cross-origin resource sharing" section and click on the "edit" button.
![Image of the cross-origin resource sharing section](media/deployment/aws_14.png)
15. Add the CORS configuration.
![Image of the edit cross-origin resource sharing page](media/deployment/aws_15.png)
16. Click on the "save changes" button.
![Image of the save changes button](media/deployment/aws_16.png)
17. Scroll down to the "bucket policy" section and click on the "edit" button.
![Image of the bucket policy section](media/deployment/aws_17.png)
18. Click on the "policy generator" button.
![Image of the policy generator button](media/deployment/aws_18.png)
19. Select the policy type, enter the policy statements and click on the "add statement" button.
![Image of the policy generator page](media/deployment/aws_19.png)
20. Click on the "generate policy" button.
![Image of the generate policy button](media/deployment/aws_20.png)
21. Copy the policy and click on the "close" button.
![Image of the policy page](media/deployment/aws_21.png)
22. Paste the policy into the policy section and amend the resource to include subdirectories in the bucket.
![Image of the policy section](media/deployment/aws_22.png)
23. Click on the "save changes" button.
![Image of the save changes button](media/deployment/aws_23.png)
24. Scroll down to the "access control list" and click on the "edit" button.
![Image of the access control list section](media/deployment/aws_24.png)
25. Select the "everyone (public access)" checkbox.
![Image of the access control list page](media/deployment/aws_25.png)
26. Click on the "save changes" button.
![Image of the save changes button](media/deployment/aws_26.png)
27. Enter "IAM" into the search bar and click on the s3 result.
![Image of the IAM results](media/deployment/aws_27.png)
28. Click on the "user groups" link.
![Image of the IAM dashboard](media/deployment/aws_28.png)
29. Click on the "create group" button.
![Image of the create group button](media/deployment/aws_29.png)
30. Enter a group name.
![Image of the create group page](media/deployment/aws_30.png)
31. Click on the "save changes" button.
![Image of the save changes button](media/deployment/aws_31.png)
32. Click on the "policies" link.
![Image of the policies link](media/deployment/aws_32.png)
33. Click on the "create policy" button.
![Image of the create policy button](media/deployment/aws_33.png)
34. Click on the "JSON" button.
![Image of the create policy page](media/deployment/aws_34.png)
35. Click on the "import managed policy" link.
![Image of the create policy page](media/deployment/aws_35.png)
36. Search for "s3", select the "AmazonS3FullAccess" option and click on the "import" button.
![Image of the import managed policies page](media/deployment/aws_36.png)
37. Amend the resource to include subdirectories in the bucket and click on the "next" button.
![Image of the create policy page](media/deployment/aws_37.png)
38. Click on the "next" button.
![Image of the next button](media/deployment/aws_38.png)
39. Enter a policy name and description.
![Image of the create policy page](media/deployment/aws_39.png)
40. Click on the "create policy" button.
![Image of the create policy button](media/deployment/aws_40.png)
41. Click on the "user groups" link.
![Image of the user groups link](media/deployment/aws_41.png)
42. Click on the "manage-go-explore" user group.
![Image of the user groups page](media/deployment/aws_42.png)
43. Click on the "permissions" tab.
![Image of the permissions tab](media/deployment/aws_43.png)
44. Click on the "add permissions" button.
![Image of the user group page](media/deployment/aws_44.png)
45. Click on the "attach policies" button.
![Image of the user group page](media/deployment/aws_45.png)
46. Select the "manage-go-explore" option.
![Image of the attach permission poliicies page](media/deployment/aws_46.png)
47. Click on the "add policies" button.
![Image of the attach permission poliicies page](media/deployment/aws_47.png)
48. Click on the "users" link.
![Image of the users link](media/deployment/aws_48.png)
49. Click on the "add user" button.
![Image of the users page](media/deployment/aws_49.png)
50. Enter a user name, select "programmatic access" under access type and click on the "next" button.
![Image of the add user page](media/deployment/aws_50.png)
51. Select the "manage-go-explore" user group and click on the "next" button.
![Image of the add user page](media/deployment/aws_51.png)
52. Click on the "next" button.
![Image of the add user page](media/deployment/aws_52.png)
53. Click on the "create user" button.
![Image of the add user page](media/deployment/aws_53.png)
54. Click on the "download .csv" button and then click on the "close" button.
![Image of the add user page](media/deployment/aws_54.png)
55. Click on the "services" button and then click on "s3" under recently visited.
![Image of the add user page](media/deployment/aws_55.png)
56. Click on the "go-explore-1" bucket.
![Image of the buckets list](media/deployment/aws_56.png)
57. Click on the "create folder" button.
![Image of the create folder button](media/deployment/aws_57.png)
58. Enter "media" in the folder name field and click on the "create folder" button.
![Image of the create folder page](media/deployment/aws_58.png)
59. Click on the "media" folder.
![Image of the folders list](media/deployment/aws_59.png)
60. Click on the "upload" button.
![Image of the media folder page](media/deployment/aws_60.png)
61. Click on the "add files" button and select the files to upload from your workspace media directory.
![Image of the upload page](media/deployment/aws_61.png)
62. Under permissions select the "grant public-read access" option.
![Image of the upload page](media/deployment/aws_62.png)
63. Select the "I understand the risk of granting public access to the specified objects" checkbox and click on the "upload" button.
![Image of the upload page](media/deployment/aws_63.png)
64. Run the command ```pip3 install boto3``` and ```pip3 install django-storages``` in the terminal to install the neccessary packages to connect to the Amazon Web Services s3 bucket.
65. Add "storages" to installed apps and add the Amazon Web Services s3 bucket settings to the static and media settings in settings.py
66. Commit these changes to GitHub.

### Heroku

The project was deployed to Heroku using the following steps:

1. Log in to Heroku and click on the "new" button.
![Image of the heroku dashboard](media/deployment/heroku_1.png)
2. Click on the "create new app" button in the dropdown list.
![Image of the heroku dashboard](media/deployment/heroku_2.png)
3. Enter a name for the app and check that it is available.
![Image of the heroku dashboard](media/deployment/heroku_3.png)
4. Click the "create app" button.
![Image of the create new app page](media/deployment/heroku_4.png)
5. Click the "resources" tab
![Image of the heroku app dashboard](media/deployment/heroku_5.png)
6. Enter "heroku postgres" in the search box and click on the "heroku postgres" option.
![Image of the add-ons page](media/deployment/heroku_6.png)
7. Make sure the plan name is set to "hobby dev - free" and click the "provision" button.
![Image of the order modal](media/deployment/heroku_7.png)
8. Run the commands ```pip3 install dj_database_url``` and ```pip3 install psycopg2```in the terminal to install the neccessary packages to connect to the heroku database.
9. Add the heroku database settings to settings.py
10. Run the command ```python3 manage.py migrate``` in the terminal to migrate the models to the database.
11. Run the command ```python3 manage.py createsuperuser``` in the terminal and enter a username, email address and password for the superuser.
12. Run the command ```pip3 install gunicorn``` in the terminal to install the gunicorn web server.
13. Run the command ```pip3 freeze > requirements.txt``` in the terminal and press enter to create the requirements.txt file.
14. Run the command ``echo web: gunicorn go_explore.wsgi:application > Procfile`` in the terminal and press enter to create the procfile.
15. Commit these changes to GitHub.
16. In Heroku, click on the "deploy" tab
![Image of the deploy tab](media/deployment/heroku_8.png)
17. Scroll down to the "deployment method" section and click on the "connect to GitHub" button
![Image of the deployment method section](media/deployment/heroku_9.png)
18. Enter the project's GitHub repository name in the repo-name field and click the "search" button.
![Image of the connect to GitHub section](media/deployment/heroku_10.png)
19. Click the "connect" button next to the GitHub repository.
![Image of the connect button](media/deployment/heroku_11.png)
20. Scroll down to the automatic deploys section and click the "enable automatic deploys" button.
![Image of the enable automatic deploys section](media/deployment/heroku_12.png)
21. Scroll back up to the top of the page and click the "settings" tab.
![Image of the settings tab](media/deployment/heroku_13.png)
22. Scroll down to the convig vars section and click the "reveal config vars" button.
![Image of the config variables section](media/deployment/heroku_14.png)
23. For each of the AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, GOOGLE_PLACES_KEY, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, SECRET_KEY, STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY, STRIPE_WH_SECRET and USE_AWS, enter the key and value and click the "add" button.
![Image of the config variables](media/deployment/heroku_15.png)

More information about deploying a website to Heroku is available [here](https://devcenter.heroku.com/categories/deployment).

### Forking the GitHub repository

The GitHub Repository can be forked using the following steps:

1.  Log in to GitHub and locate the project's [GitHub Repository](https://github.com/jonathan-odonnell/milestone-project-4).
2.  At the top-right of the repository, click the "fork" Button.
![Image of the fork button](media/deployment/fork.png)

More information about forking a GitHub repository is available [here](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo).

### Making a Local Clone

A local clone of the project can be created using the following steps:

1. Log in to GitHub and locate the project's [GitHub Repository](https://github.com/jonathan-odonnell/milestone-project-4).
2. Under the repository name, click the "code" button.
![Image of the code button](media/deployment/clone_1.png)
3. To clone the repository using HTTPS, under "clone with HTTPS", click the clipboard button to copy the repository URL.
![Image of the clipboard button](media/deployment/clone_2.png)
To clone using GitHub CLI, click "use GitHub" CLI and then click the clipboard button.
![Image of the use GitHub CLI button](media/deployment/clone_3.png)
![Image of the clipboard button](media/deployment/clone_4.png)
4.  Open the terminal.
5.  Change the current working directory to the location where you want to store the cloned repository.
6.  Type `git clone` and then paste the URL you copied in Step 3.

```
$ git clone https://github.com/jonathan-odonnell/milestone-project-4.git
```

7.  Press enter to create your clone.

```
Cloning into 'milestone-project-4'...
remote: Enumerating objects: 4783, done.
remote: Counting objects: 100% (190/190), done.
remote: Compressing objects: 100% (106/106), done.
remote: Total 4783 (delta 119), reused 130 (delta 82), pack-reused 4593
Receiving objects: 100% (4783/4783), 78.78 MiB | 3.19 MiB/s, done.
Resolving deltas: 100% (2919/2919), done.
```

More information about making a local clone of a GitHub repository is available [here](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository).

## Credits

### Code

### Content

### Media

- The North Island image was from [Unsplash](https://unsplash.com/photos/73F4pKoUkM0).
- The Praia Da Luz image was from [Unsplash](https://unsplash.com/photos/bTJKBZ-_h4I).
- The Antalya image was from [Unsplash](https://unsplash.com/photos/Hs1tXq1g4kQ).
- The New South Wales image was from [Unsplash](https://unsplash.com/photos/a80osyu1stE).
- The Milan image was from [Unsplash](https://unsplash.com/photos/5QrM3dEf5mA).
- The Amancil image was from [Unsplash](https://unsplash.com/photos/HSr-sfDLC0g).
- The Carvoiero image was from [Unsplash](https://unsplash.com/photos/04huF1iBwug).
- The Santorini image was from [Unsplash](https://unsplash.com/photos/8PR1tT9UmmU).
- The Canadian Rockies image was from [Unsplash](https://unsplash.com/photos/2Fl6efcITLA).
- The Dublin image was from [Unsplash](https://unsplash.com/photos/tnzzr8HpLhs).
- The Vancouver image was from [Unsplash](https://unsplash.com/photos/MzCeUhY3Xy0).
- The New York image was from [Unsplash](https://unsplash.com/photos/0_la3_Slfwk).
- The Miami image was from [Unsplash](https://unsplash.com/photos/_K4B1puV484).
- The Singapore image was from [Unsplash](https://unsplash.com/photos/7ryPpZK1qV8).
- The Toronto image was from [Unsplash](https://unsplash.com/photos/igRWvbLxGjw).
- The Hawaii image was from [Unsplash](https://unsplash.com/photos/oIvJWPPKbWk).
- The Albufeira image was from [Unsplash](https://unsplash.com/photos/tMffGE7u1bI).
- The Agios Nikolaos image was from [Unsplash](https://unsplash.com/photos/ekpJ4wqf2io).
- The Rhodes image was from [Unsplash](https://unsplash.com/photos/7jXvvEMNTkc).
- The Marbella image was from [Unsplash](https://unsplash.com/photos/XzcBoj8gBhY).
- The Lefkas image was from [Unsplash](https://unsplash.com/photos/O2wgGEZVvA4).
- The Fethiye image was from [Unsplash](https://unsplash.com/photos/wzDl9U0A0DI).
- The Zermatt image was from [Unsplash](https://unsplash.com/photos/8hCbyovrhKw).
- The Paris image was from [Unsplash](https://unsplash.com/photos/PIOqHJG5a1U).
- The Chicago image was from [Unsplash](https://unsplash.com/photos/Lmc-tvmuopw).
- The San Francisco image was from [Unsplash](https://unsplash.com/photos/zcoDYal9GkQ).
- The Los Angeles image was from [Unsplash](https://unsplash.com/photos/cHRDevKFDBw).
- The Whistler image was from [Unsplash](https://unsplash.com/photos/v1VfRqT8MSA).
- The Madrid image was from [Unsplash](https://unsplash.com/photos/ChSZETOal-I).
- The South Island image was from [Unsplash](https://unsplash.com/photos/NS0WZ8XnEdk).
- The Tasmania image was from [Unsplash](https://unsplash.com/photos/sQNUFc2RXbk).
- The South Australia image was from [Unsplash](https://unsplash.com/photos/dqrfDkAOeos).
- The Queensland image was from [Unsplash](https://unsplash.com/photos/O3ji6Tv0PtY).
- The Victoria image was from [Unsplash](https://unsplash.com/photos/GqO1nskZeFY).
- The Northern Territory image was from [Unsplash](https://unsplash.com/photos/WEtXkeIlMoM).
- The Praia Da Rocha image was from [Unsplash](https://unsplash.com/photos/Aj8FTuWDM5w).
- The Montréal image was from [Unsplash](https://unsplash.com/photos/BG9oZ15a4Xk).
- The Zante image was from [Unsplash](https://unsplash.com/photos/qai_Clhyq0s).
- The Lanzarote image was from [Unsplash](https://unsplash.com/photos/tVUJGXRp1PU).
- The Tenerife image was from [Unsplash](https://unsplash.com/photos/wOxgcRwXCzo).
- The Alvor image was from [Unsplash](https://unsplash.com/photos/cmYjQ30PbWk).
- The Cancun image was from [Unsplash](https://unsplash.com/photos/5_vf0xlRxB4).
- The Lagos image was from [Unsplash](https://unsplash.com/photos/zVs8YsTgIOU).
- The Kos image was from [Unsplash](https://unsplash.com/photos/YzSvUjPlDYs).
- The Mykonos image was from [Unsplash](https://unsplash.com/photos/TzDGmeq4VjY).
- The Western Australia image was from [Unsplash](https://unsplash.com/photos/OzUJa5Q9m1g).
- The Stalos image was from [Unsplash](https://unsplash.com/photos/xvknd8C7Kic).
- The North America image was from [Unsplash](https://unsplash.com/photos/5xa0SI9JmmY).
- The Asia and Oceana image was from [Pixabay](https://pixabay.com/photos/australia-great-ocean-road-beach-3912587/).
- The Europe image was from [Unsplash](https://unsplash.com/photos/f-DvU93UhTs).
- The Offers image was from [Unsplash](https://unsplash.com/photos/O2wgGEZVvA4).
- The Activity Holidays image was from [Unsplash](https://unsplash.com/photos/6EXdJNbjxV0).
- The City Breaks image was from [Unsplash](https://unsplash.com/photos/TaCk3NspYe0).
- The Resort Holidays image was from [Unsplash](https://unsplash.com/photos/IdpYE0Qt8Hw).
- The Airport Lounge image was from [Unsplash](https://unsplash.com/photos/MiDPt7D4WN8).
- The Additional Luggage image was from [Unsplash](https://unsplash.com/photos/OMwCLuZu5_w).
- The Flight Food image was from [Unsplash](https://unsplash.com/photos/aeESmmFKH0M).
- The Airoplane Seats image was from [Unsplash](https://unsplash.com/photos/1g3qVp7ynX4).
- The Sign Up image was from [Unsplash](https://unsplash.com/photos/dzD67vW_93I).
- The Contact image was from [Unsplash](https://unsplash.com/photos/Prb-sjOUBFs).
