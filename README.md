# Twitter-like Social Media Network

#### Video Demo: <https://youtu.be/1WGBDMElxgo>

#### Access: <https://socialmedianetwork.pythonanywhere.com/>

This is a project I did while taking CS50's Web Programming with Python and Javascript Course at Harvard University.
As the fourth project in this course, my task was to design and implement a social network using Python, JavaScript, HTML, and CSS. This app is built on the Django Framework

I will here be discussing the distinctiveness and complexity of my project, what each file contains, how to run this application and any other additional information needed.

## Specifications

#### See All Posts

The “All Posts” link in the navigation bar takes the user to a page where they can see all posts from all users, with the most recent posts first.

#### Creating New Posts

Users who are signed in can write a new text-based post by filling in text into a text area and then clicking a button to submit the post.

#### Profile Pages

Clicking on a username loads that user’s profile page and :

-   Displays the number of followers the user has and the number of people that the user follows.
-   Displays all of that user's posts in reverse chronological order (that way the user sees the most recent posts first)
-   If signed in, you can follow or unfollow that user.

#### Followings Page

If signed in, the “Following” link in the navigation bar takes the user to a page where they see all posts made by users that they follow.

#### Editing Posts

Users can edit their own posts. This is done using Javascript so that it does not require a reload of the entire page.

#### Like and Unlike a Post

Users can click a button to toggle whether or not the like that post. This is done asynchronously with Javascript so that the server updates the like count is updated without requiring an entire reload of the page.

## Hosting

Since this is the best project I made so far in my short developer career, I wanted to get hosting and make my web app available online.
After doing some research online, I found two main options that had a free plan offering, [pythonanywhere](https://www.pythonanywhere.com/) and [Heroku](https://www.heroku.com/).

I decided to go with pythonanywhere, and after a little bit of struggle with file location and dependencies, I managed to get it to work.
Here is a [link](https://socialmedianetwork.pythonanywhere.com/) to it.
