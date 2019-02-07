# Issue Tracker
Issue Tracker web app (Full Stack Frameworks with Django Milestone Project)
[![Build Status](https://travis-ci.org/jordandaly/issue_tracker.svg?branch=master)](https://travis-ci.org/jordandaly/issue_tracker)

* This is a web application that allow users to create issues, comment on issues, and show the status of an issue (‘to do,’ ‘doing,’ or ‘done’).
* Issues come in two varieties – ‘bugs’ (fix for free), and ‘features’ (only develop if offered enough money). 
* To help prioritize the work, users are able to upvote bugs (signifying ‘I have this too’), and upvote feature requests (signifying ‘I want to have this too’).
* While upvoting bugs is free, to upvote a feature request, users need to pay some money to pay for development time in working on it.
* This is a full stack web application (frontend and backend) that provides CRUD (Create, Read, Update, Delete) functionality to a database hosted in the cloud on Heroku platform as a service. 

## UX Design

Details of the UX design is available in the 'FSF project design' folder. This document outlines how I approached the design of the user interface of the main pages of the web application.

## Features

### Existing Features

Users can :
1.	View list of all Issues sorted by newest descending with pagination and search by keyword.
2.  Filter Issues by Issue Type, Status, isResolved, Tag, Author and Assignee.
3.	Add New Issue.
4.  Add New Comment to an Issue.
5.	Upvote Bugs for free.
6.  Upvote Features by adding the desired quantity of upvotes of an issue to the cart and using the checkout functionality to submit a payment
7.	Edit an Issue, Comment and Cart
8.  View list of Issues created by current logged in user (My Issues) and search by keyword
9.  View list of notifications that are generated when the user's Issues are updated, upvoted or have a comment added (My Updates)
10. View dashboard showing how many issues have been resolved today, in the past 7 days and in the past 28 days and charts for Top Bug Upvotes, Top Feature Upvotes, Issue Type and Issue Status
11. Add Replies to Comments
12. Save Issue and view list of Saved Issues

### Features Left to Implement
1. Average Time to resolve Issue chart on Dashboard.
2. Issue Tags need to behave more like the concept of "TAGS", tried a third party django package called 'django-tagulous' but found it too complicated to try to implement.
3. My Updates is using a third party Django package called 'django-notifications' and needs more work to fully implement the proper functionality.

## Demo

A demo of this web application is available [here](https://daly-issue-tracker.herokuapp.com/).


## Getting started /

1. Clone the repo and cd into the project directory.
2. Ensure you have Python 3 and Postgres installed and create a virtual environment and activate it.
3. Install dependencies: `pip3 install -r requirements.txt`.


## Technologies Used

**HTML, CSS, JavaScript, [Materialize](https://materializecss.com/) Front End Framework), Highcharts chart library, Stripe Payments API, AWS S3 API, Python, Django Full Stack Web Application Framework, PostgreSQL database hosted in the cloud on Heroku :**

## Testing

Automated tests are located in the Issues app in test_models.py, test_forms.py and test_views.py. These 16 tests passed as per screenshot in Testing folder. To run the test:
`python3 manage.py test`

Manual testing was undertaken for this application and satisfactorily passed. A sample of the tests conducted are as follows:
1.	Testing navigation buttons and hyperlinks throughout the page.
2.	Testing the CRUD functionality: adding and editing Issues, Comments, Replies.
3.	Testing the responsiveness of the application on different browsers and then using different devices.
4.  Testing ecommerce functionality: generating order transactions with Add to Cart, Checkout and payments with Stripe test card details.
5. Testing image upload to AWS S3 bucket.

## Deployment
1. Make sure requirements.txt and Procfile exist
`pip3 freeze --local requirements.txt`
`echo web: python app.py > Procfile`
2. Create Heroku App, Select Postgres add-on, download Heroku CLI toolbelt, login to heroku (Heroku login), git init, connect git to heroku (heroku git remote -a <project>), git add ., git commit, git push heroku master.
3. `heroku ps:scale web=1`
4. In heroku app settings set the config vars to add DATABASE_URL, STRIPE API key and secret, AWS key and secret

## Credits

**Jordan Daly** - This project was completed as part of Code Institute’s Mentored Online Full Stack Web Development course in 2018.

### Acknowledgements
I used the following [blog](https://simpleisbetterthancomplex.com/) for tutorials on various Django topics such as AWS S3 integration, filters, highcharts integration

The Accounts, Cart and Checkout apps are based upon the sample apps from the User Authentication and Authorisation and Ecommerce mini project components of the Full Stack Frameworks with Django module.


