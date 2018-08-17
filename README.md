# issue_tracker
Issue Tracker web app (Full Stack Frameworks with Django Milestone Project)
[![Build Status](https://travis-ci.org/jordandaly/issue_tracker.svg?branch=master)](https://travis-ci.org/jordandaly/issue_tracker)

## UX Design

Details of the UX design is available in the 'FSF project design' folder. This document outlines how I approached the design of this site.

## Features

### Existing Features

This is a web application that allow users to create issues, comment on issues, and show the status of an issue (‘to do,’ ‘doing,’ or ‘done’).
Issues come in two varieties – ‘bugs’ (fix for free), and ‘features’ (only develop if offered enough money). To help prioritize the work, users are able to upvote bugs (signifying ‘I have this too’), and upvote feature requests (signifying ‘I want to have this too’).
While upvoting bugs is free, to upvote a feature request, users need to pay some money to pay for development time in working on it.
It is a full stack web application (frontend and backend) that provides CRUD (Create, Read, Update, Delete) functionality to a database hosted in the cloud on Heroku platform as a service. Users can :
1.	View a list of issues and filter the list
2.	Add a new issue and add comments to an issue
3.	Upvote bugs for free and Upvote Features by adding the desired quantity of upvotes of an issue to the cart and using the checkout functionality to submit a payment
4.	Edit an Issue, Comment and Cart

### Features Left to Implement

## Demo

A demo of this web application is available [here](https://daly-issue-tracker.herokuapp.com/).


## Getting started /

1. Clone the repo and cd into the project directory.
2. Ensure you have Python 3 and Postgres installed and create a virtual environment and activate it.
3. Install dependencies: `pip install -r requirements.txt`.


## Technologies Used

**HTML, CSS, JavaScript (Front End Framework Materialize), Highcharts chart library, Stripe Payments API, AWS S3 API, Python, Django Full Stack Web Application Framework, PostgreSQL an object-relational database management system :**

## Testing

Manual testing was undertaken for this application and satisfactorily passed. A sample of the tests conducted are as follows:
1.	Testing navigation buttons and hyperlinks throughout the page.
2.	Testing the Read, Create and Update functionality.
3.	Testing the responsiveness of the application on different browsers and then using different devices.
4.  Testing payments with Stripe test card details.

##Automated Tests

## Deployment
1. Make sure requirements.txt and Procfile exist
⋅⋅*pip3 freeze --local requirements.txt
⋅⋅*echo web: python app.py > Procfile
2. Create Heroku App, Select Postgres add-on, download Heroku CLI toolbelt, login to heroku (Heroku login), git init, connect git to heroku (heroku git remote -a <project>), git add ., git commit, git push heroku master.
3. heroku ps:scale web=1
4. In heroku app settings set the config vars to add DATABASE_URL, STRIPE API key and secret, AWS key and secret

## Credits

**Jordan Daly** - This project was completed as part of Code Institute’s Mentored Online Full Stack Web Development course in 2018.

### Content

### Media

### Acknowledgements
