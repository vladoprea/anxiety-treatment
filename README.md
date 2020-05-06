# Anxiety treatment

Anxiety disorder is a condition that became widely spread in the world in the last years. This site comes as a help for those who struggle with moderate anxiety and don't require medical treatment. Its content, features and tools are inspired from Cognitive Behavioural Therapy(CBT), a method successfully used in psychoterapy.
The deployed site can be accessed here: <http://anxiety-treatment.herokuapp.com/treatment>

## User Experience(UX)

The site has two levels of access of the informations and content: with or without logging with an account.

### Without account

Being a sensitive subject, I created an option for the users that are not yet convinced to create an account and start practising. On the first page there is a brief description of anxiety disorder and two detailed articles about symptoms and treatment. This comes as general information that can be accessed by anybody and is like a preview before creating an account. Having these informations, an user can decide if it will go further or not.

### With account

An user can create and login to his own account. When logged in, a dashboard page opens, that contains informations about CBT and picture-links to the two features available, named tools: journal and TFB-cycle. In journal, as its name says, the user can keep a personal journal, he can add new entries, edit them or delete them. In TFB cycle, the process rely on identifying an Hot Tought and debrief it taking in consideration all of the physical and mental implications that it have. The user has a detailed form that he can use to add a new entry, to edit it or to delete it.
Privacy of toughts is very important in general and in special in these kind of conditions. That is why, an user can see only his own entries.

### Target audience

* A person that experience more than usual level of anxiety.
* A person that has been diagnosed with moderate general anxiety disorder.
* A person that has a family member or a friend experiencing higher level of anxiety and is looking for a way to help.
* A student of Psychology or Psyhoterapy.
* A doctor in Psychology or Psyhoterapy.

### User stories

* As a person that experience more than usual level of anxiety, starts to worry about it which creates even more discomfort. Looking for answers regarding its feelings, a user can found informations about symptoms and treatment on the first page. After reading them, he can decide if he wants to create an account and try the CBT techniques available.
* As a person that has been diagnosed with moderate general anxiety disorder, I want to begin a treatment that doesn't include medication. This sort of treatment techniques are usually recomended and supervised by doctors. The user creates an account, access and use the tools available.
* A person that has a family member or a friend experiencing higher level of anxiety and is looking for a way to help, I am looking for more informations. I have access to symptoms and treatment articles, but also I want to create an account to have a better idea of how these techniques work.
* As a student of Psychology or Psyhoterapy, I am looking for ways to expand my acknowledgement about the therapy. Best way to do it is to experience myself, so I create an account and start to monitor my toughts.
* A doctor in Psychology or Psyhoterapy is using these therapies in treating pacients. This site can be recommended as a part of their treatment.

### Mock-ups

As it can be seen, the site layout and functionality was modified, improved  and adapted during development process. An Ipad mock-up has not been created, because this site has the same out on Ipad as on Desktop:

* [Desktop Mock-up](https://ibb.co/album/QFKqxc)
* [Mobile Mock-up](https://ibb.co/album/3B8XP8)

## Features

### Navbar

Navbar has different buttons for general access(without account) and for logged in users(with account).

#### General access

* Home - access to the first page
* Register - opens register form
* Login - opens login form
* Help guide - opens Help Guide page

#### Logged in users

* Dashboard - access dashboard page
* Journal - access personal journal page
* TFB Cycle - access TFB Cycle page
* Logout - offers the option to log out from the account. User will be redirected to Home page
* Help guide - opens Help Guide pag

### Home

Home page contains a jumbotron with Register and Login buttons that opens forms for each. It has also general informations about anxiety disorders. Two article cards are at the bottom of the page,containing picture, text and the option to be clicked: symptoms and treatment.

### Help Guide

The Help Guide page contains a list of organizations with their sites and phone numbers that offers help and support for those suffering from anxiety. If the users needs urgent help, he can contact one of them.

### Dashboard

Dashboard contains informations about Cognitive Behavioural Therapy(CBT) making an introduction on its real life application. It also contains 2 picture-links that redirects you to the treatment techniques tools : Journal and TFB Cycle.

### Journal

On this page the user founds a button for creating a new entry. The buttons opens a form with 2 fields : title and description. After introducing informations, the user is redirected to the journal page, where his entry is displayed as an accordion. When opening each panel, the user finds 2 buttons, Edit and Delete. Edit button opens a form prepopulated with the selected entry text. Delete button, erase the entry from accordion and database.

### TFB Cycle

On this page the user founds a button for creating a new entry. The buttons opens a form with 9 fields, one of them being a select field. After introducing informations, the user is redirected to the journal page, where his entry is displayed as an accordion. When opening each panel, the user finds 2 buttons, Edit and Delete. Edit button opens a form prepopulated with the selected entry text. Delete button, erase the entry from accordion and database.

## Technologies used

This site was developed using VScode, committed to git and pushed to GitHub with the built-in functionality in VScode.

* [HTML](https://www.w3schools.com/html/)
* [CSS](https://www.w3schools.com/css/)
* [Bootstrap](https://getbootstrap.com/)
* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/1.0.x/)
* [Jinja](https://jinja.palletsprojects.com/en/2.10.x/)
* [PyMongo](https://pymongo.readthedocs.io/en/stable/)
* [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
* [Google Fonts](https://fonts.google.com/)
* [Font awesome](https://www.bootstrapcdn.com/fontawesome/)

Other tools used:

* [Adobe XD](https://www.adobe.com/ro/products/xd.html) - for creating mock-ups
* [IMGBB](https://imgbb.com/) - for uploading mock-up pictures

## Testing

This project was only tested manually on a range of devices and browsers. During development I constantly used Chrome Developer Tools in order to ensure responsivness on all devices. The site functionality was constantly checked in the following browsers:

* Chrome
* Mozzila Firefox
* Opera
* Safari
* Internet Explorer 11
* Mi Browser

### Manual Testing

Manual testing was made on several small, medium and large devices. With help from some friends, 7 accounts were created and checked the functionality of the site.

#### Register

* introducing new username and email, the feature works correct
* trying to introduce an username or email that has been used before to create an account, you get an error, as desired
* confirming password by entering a different password gives you an error, which is intended

#### Login

* introducing correct email and password redirects user to dashboard which is correct
* introducing an email that is not connected to any account or a wrong password, gives an error, which is intended

#### Journal and TFB Cycle

* Add new entry button opens a form where user can introduce data. Pressing add entry redirects to journal page where the new indroduced entry is displayed as accordion. Date and time is also displayed. Accordion functions correctly.
* Edit buttons open a form prepopulated with the selected entry data. All fields work properly besides textarea fields, an error that is detailed in Error chapter below.
* Delete buttons erase the entry and it works properly.

### Errors

* A major error and inconvienent for the user is in the Edit form. Textarea fields are being prepopulated with placeholder content of the selected entry. When trying to edit, the whole text disapears. The error comes from here in 'edit_tought.html':

```html
{{ form.hidden_tag() }} {{ render_field(form.body, class="form-control", placeholder=journal.body) }}```
I haven't found a better solution to prepopulate TextAreaFields. This causes major inconvienent for the user.

## Deployment

This project was developed using Visual Studio Code, Python, and Git, committed to a local Git repository, and pushed to GitHub using a locally installed version of Git via command prompt.

### Deployment to Heroku

1. Login to [Heroku](https://www.heroku.com/)
2. From the main dashboard, select the New dropdown, then select Create new app.
3. Give your app a unique name, and select the region you wish to deploy to.
4. After the app is created, select Deploy from the top of the page, and scroll down to Deployment Method.
5. Select GitHub as the method of deployment.
6. Log in using your Github credentials.
7. Select Connect on the repository you wish to connect to.
8. Under Manual deploy, select the branch you wish to deploy, and hit Deploy Branch
9. After the application is built, select Settings from the top of the page.
10. Select Reveal Config Vars.
11. Add your config keys for IP, PORT, MONGO_URI, MONGO_DBNAME, and SECRET_KEY.

## Credits

### Media

* [Home page text](https://www.nimh.nih.gov/health/topics/anxiety-disorders/index.shtml)
* [Symptoms page text](https://www.webmd.com/anxiety-panic/guide/anxiety-disorders#1)
* [Treatment page text](https://www.medicalnewstoday.com/articles/323494)
* [Dashboard CBT text](https://www.nhs.uk/conditions/cognitive-behavioural-therapy-cbt/)
* [Help Guide useful contacts](https://www.mind.org.uk/information-support/types-of-mental-health-problems/anxiety-and-panic-attacks/useful-contacts/)
* [Journal Tool Image](https://www.goodreads.com/book/show/49560123-my-daily-journal)
* [TFB Cycle Tool Image](https://www.estherkane.com/featured/the-power-of-positive-thinking-turning-a-vicious-cycle-into-a-luscious-cycle/)
* [Symptoms Image](https://levantin54.wordpress.com/2012/09/20/poem-cu-cer-ploios/)
* [Treatment Image](http://radioorhei.info/curcubeu-10/)

### Code

* [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
* Wtforms and form rendering: <https://www.youtube.com/watch?v=zRwy8gtgJ1A&t=905s>
* _formhelpers.html: <https://flask.palletsprojects.com/en/1.1.x/patterns/wtforms/>
* Datetime without miliseconds: <https://stackoverflow.com/questions/7999935/python-datetime-to-string-without-microsecond-component> answer by Codeif user
* Flash messages: <https://pythonise.com/series/learning-flask/flask-message-flashing>

## Acnowledgements

* Code Institute Slack Community for providing solutions to every question I had.
* Tutoring from Code Institute that was very heplful when I was in need.

Special thanks to Maranatha Ilesanmi, my mentor, who guided me through this project and provided punctual, solid, useful feedback and very helpful input and tips.
