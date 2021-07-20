# Deployment

## Amazon Web Services S3 Bucket

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
65. Add "storages" to installed apps and add the Amazon Web Services s3 bucket settings to the static files and media files settings in settings.py
66. Add the custom_storages.py file to set the static files and media files storage locations in the relevant s3boto3 storage classes.
67. Commit these changes to GitHub.

## Heroku

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
8. Run the command ```python3 manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json``` in the terminal to backup the local database and load it into a db.json file.
9. Run the commands ```pip3 install dj_database_url``` and ```pip3 install psycopg2```in the terminal to install the neccessary packages to connect to the heroku database.
10. Add the heroku database settings to settings.py and commit the changes to github.
11. Run the command ```python3 manage.py migrate``` in the terminal to migrate the models to the database.
12. Run the command ```python3 manage.py loaddata db.json``` in the terminal to load the data from the db.json file into the postgres database.
13. Run the command ```python3 manage.py createsuperuser``` in the terminal and enter a username, email address and password for the superuser.
14. Run the command ```pip3 install gunicorn``` in the terminal to install the gunicorn web server.
15. Run the command ```pip3 freeze > requirements.txt``` in the terminal and press enter to create the requirements.txt file and commit these changes to GitHub.
16. Run the command ``echo web: gunicorn go_explore.wsgi:application > Procfile`` in the terminal and press enter to create the procfile and commit these changes to GitHub.
17. In Heroku, click on the "deploy" tab
![Image of the deploy tab](media/deployment/heroku_8.png)
18. Scroll down to the "deployment method" section and click on the "connect to GitHub" button
![Image of the deployment method section](media/deployment/heroku_9.png)
19. Enter the project's GitHub repository name in the repo-name field and click the "search" button.
![Image of the connect to GitHub section](media/deployment/heroku_10.png)
20. Click the "connect" button next to the GitHub repository.
![Image of the connect button](media/deployment/heroku_11.png)
21. Scroll down to the automatic deploys section and click the "enable automatic deploys" button.
![Image of the enable automatic deploys section](media/deployment/heroku_12.png)
22. Scroll back up to the top of the page and click the "settings" tab.
![Image of the settings tab](media/deployment/heroku_13.png)
23. Scroll down to the convig vars section and click the "reveal config vars" button.
![Image of the config variables section](media/deployment/heroku_14.png)
24. For each of the AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, GOOGLE_PLACES_KEY, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, SECRET_KEY, STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY, STRIPE_WH_SECRET and USE_AWS, enter the key and value and click the "add" button.
![Image of the config variables](media/deployment/heroku_15.png)

More information about deploying a website to Heroku is available [here](https://devcenter.heroku.com/categories/deployment).

## Forking the GitHub repository

The GitHub Repository can be forked using the following steps:

1.  Log in to GitHub and locate the project's [GitHub Repository](https://github.com/jonathan-odonnell/milestone-project-4).
2.  At the top-right of the repository, click the "fork" Button.
![Image of the fork button](media/deployment/fork.png)

More information about forking a GitHub repository is available [here](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo).

## Making a Local Clone

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

