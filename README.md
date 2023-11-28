# <i> PopcornPicks🍿: Your Destination for Movie Recommendations </i>
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://gitHub.com/brwali/PopcornPicks/graphs/commit-activity) [![Contributors Activity](https://img.shields.io/github/commit-activity/m/brwali/PopcornPicks)](https://github.com/brwali/PopcornPicks/pulse) [![GitHub issues](https://img.shields.io/github/issues/brwali/PopcornPicks.svg)](https://github.com/brwali/PopcornPicks/issues?q=is%3Aopen+is%3Aissue) [![GitHub issues-closed](https://img.shields.io/github/issues-closed/brwali/PopcornPicks.svg)](https://github.com/brwali/PopcornPicks/issues?q=is%3Aissue+is%3Aclosed) ![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/brwali/PopcornPicks) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT) [![Unittest](https://github.com/brwali/PopcornPicks/actions/workflows/unittest.yml/badge.svg?branch=master&event=push)](https://github.com/brwali/PopcornPicks/actions/workflows/unittest.yml) [![codecov](https://codecov.io/gh/brwali/PopcornPicks/graph/badge.svg?token=0XN6K2DMGS)](https://codecov.io/gh/brwali/PopcornPicks) [![GitHub release](https://img.shields.io/github/release/brwali/PopcornPicks.svg)](https://GitHub.com/brwali/PopcornPicksreleases/) [![StyleCheck: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint) [![HitCount](https://hits.dwyl.com/brwali/PopcornPicks.svg)](https://hits.dwyl.com/brwali/PopcornPicks) ![GitHub contributors](https://img.shields.io/github/contributors/brwali/PopcornPicks) ![GitHub Release Date - Published_At](https://img.shields.io/github/release-date/brwali/PopcornPicks) ![GitHub repo size](https://img.shields.io/github/repo-size/brwali/PopcornPicks) [![Black](https://github.com/brwali/PopcornPicks/actions/workflows/black.yml/badge.svg)](https://github.com/brwali/PopcornPicks/actions/workflows/black.yml) [![Maintainability](https://api.codeclimate.com/v1/badges/260d558f17ae5e1027e5/maintainability)](https://codeclimate.com/github/brwali/PopcornPicks/maintainability) [![GitHub closed issues by-label](https://img.shields.io/github/issues-closed-raw/brwali/PopcornPicks/bug?color=green&label=Squished%20bugs)](https://github.com/brwali/PopcornPicks/issues?q=is%3Aissue+label%3Abug+is%3Aclosed) ![Discord](https://img.shields.io/discord/1143966088695124110) [![DOI](https://zenodo.org/badge/713118657.svg)](https://zenodo.org/doi/10.5281/zenodo.10210915)
  

  
<img src="https://github.com/brwali/PopcornPicks/blob/master/asset/header_display.png" alt="drawing" style="width:1000px;"/>
<b>PopcornPicks is more than just a movie recommender system; it's a gateway to a world of cinematic adventures. With an ever-expanding library of films and a powerful recommendation algorithm, PopcornPicks is here to transform the way you discover, enjoy, and connect with movies.</b>

# Contents  

- [Why use PopcornPicks?](#why-use-popcornpicks)
- [Project Documentation](#documentation)
- [Project Presentation Videos](#project-presentation-video)
- [Brief Overview of Project](#project-description)
- [What Docs](#what-docs)
- [How Docs](#how-docs)<br/>
    - [Recommendation Mechanism](#movie-recommendation-mechanism)<br/>
    - [Email Notifier](#email-notifier)
    - [Create an Acccount](#create-an-account)
    - [Login to Account](#login-to-account)
    - [Profile and Friends](#profile-and-friends)
    - [Wall](#wall)
- [Improvements Made in the Project](#project-3-delta)
- [TechStack Used for the Development of Project](#tech-stack-used)
- [Steps for Execution](#getting-started)
- [Future Scope](#future-scope)
- [Contribute](#contribute-to-the-project)
- [Team Members](#contributors)
- [Contact](#contact)
- [License](#license)

## Why use PopcornPicks?

<img
  src="https://media.giphy.com/media/l1J9GIXk9w7OYsd5S/giphy.gif"
  alt="Starship with iTerm2 and the Snazzy theme"
  width="40%"
  align="right"
/>

PopcornPicks: Your movie recommender! Input movies, get tailored suggestions, and share via email. Elevate your movie choices effortlessly!

- **Efficient:** Lightning-fast recommendations for movie buffs! 🚀
- **Adaptable:** Tailor the recommendations to your taste.
- **Accessible:** Works across all platforms and shells.
- **Insightful:** Get movie insights at a glance.
- **Comprehensive:** Supports a wide array of user-preferred movies.
- **Simple:** Easy installation and setup – start discovering great movies in no time!"

## Documentation
Checkout for project documentation [here](https://github.com/brwali/PopcornPicks/tree/master/docs)

## Project Presentation Videos
### New Features 2 minute demo
[![why contribute video](https://img.youtube.com/vi/QHju8EzQUQ4/0.jpg)](https://www.youtube.com/watch?v=QHju8EzQUQ4)

### Why contribute?
[![why contribute video](https://img.youtube.com/vi/aQ1cryH4B7A/0.jpg)](https://www.youtube.com/watch?v=aQ1cryH4B7A)


## Project Description
PopcornPicks is a user-friendly movie recommender that curates a tailored list of 10 movie predictions based on user-provided movie preferences. Users can input their favorite movies, and our algorithm refines recommendations based on feedback—Liked, Disliked, or Yet To Watch. Additionally, PopcornPicks offers the convenience of emailing the recommended movies, enhancing the movie-watching experience. For the system architecture and other details, please refer to our documentation [here](https://github.com/brwali/PopcornPicks/tree/master/docs)

## What docs
View our documentation outlining each class and function of PopcornPicks here
- [Backend](https://github.com/brwali/PopcornPicks/blob/master/docs/backend.md)
- [Frontend](https://github.com/brwali/PopcornPicks/blob/master/docs/frontend.md)
- [Testing](https://github.com/brwali/PopcornPicks/blob/master/docs/testing.md)

View our autogenerated doco here [Doco](https://github.com/brwali/PopcornPicks/blob/master/docs/generated_docs/)

## How docs

### Movie Recommendation Mechanism 
#### (Modified in project 3)
**The user selects upto 5 movies to get a tailored watchlist and provide feedback for the same**
  
<img src="https://github.com/brwali/PopcornPicks/blob/master/asset/recommend_mechanism.gif" width="600" height="375">

### Email Notifier
**The user sends his/her movies feedback via an email (Notify Me button)**
  
<div style="display: flex; justify-content: space-between;">
    <img src="https://github.com/brwali/PopcornPicks/blob/master/asset/email_notifier.gif" alt="Email Notifier" width="600" height="375">
    <img src="https://github.com/brwali/PopcornPicks/blob/master/asset/email.png" alt="Email" width="400" height="400">
</div>

### Create an Account
#### (NEW in project 3)
**Users can now create accounts, persisting data including their movie reviews and recommendations**
<img src="https://github.com/brwali/PopcornPicks/blob/master/asset/create_account.gif" width="600" height="375">

### Login to account
#### (NEW in project 3)
**The user can log in to their account securly with encrypted passwords stored in our database**
<img src="https://github.com/brwali/PopcornPicks/blob/master/asset/login.gif" width="600" height="375">

### Profile and Friends
#### (NEW in project 3)
**The user can add friends, view the movies reviewed by the friends, and see their reviewed movies in their profile**
<img src="https://github.com/brwali/PopcornPicks/blob/master/asset/profile.gif" width="600" height="375">

### Wall
#### (NEW in project 3)
**The user can interact with other users, by viewing a community sourced wall of recent moview reviews**
<img src="https://github.com/brwali/PopcornPicks/blob/master/asset/wall.gif" width="600" height="375">

## Project 3 Delta
Check out the significant changes that we made for Project 3 [here](https://github.com/brwali/PopcornPicks/blob/master/proj3/Proj3Changes.md)

Our grading scorecard can be found [here](https://github.com/brwali/PopcornPicks/blob/master/proj3/README.md)

## Tech stack Used👨‍💻:

<code><a href="https://developer.mozilla.org/en-US/docs/Glossary/HTML5" target="_blank"><img height="50" src="https://www.vectorlogo.zone/logos/w3_html5/w3_html5-ar21.svg"></a></code>
<code><a href="https://developer.mozilla.org/en-US/docs/Web/CSS" target="_blank"><img height="50" src="https://www.vectorlogo.zone/logos/w3_css/w3_css-ar21.svg"></a></code> <code><a href="https://www.javascript.com/" target="_blank"><img height="50" src="https://www.vectorlogo.zone/logos/javascript/javascript-ar21.svg"></a></code>
<code><a href="https://www.jquery.com//" target="_blank"><img height="35" src="https://www.vectorlogo.zone/logos/jquery/jquery-horizontal.svg"></a></code>
<code><a href="https://getbootstrap.com/" target="_blank"><img height="35" src="https://www.vectorlogo.zone/logos/getbootstrap/getbootstrap-ar21.svg"></a></code>
<code><a href="https://flask.palletsprojects.com/en/1.1.x/" target="_blank"><img height="50" src="https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-ar21.svg"></a></code>
<!--<code><a href="https://github.com/" target="_blank"><img height="50" src="https://www.vectorlogo.zone/logos/github/github-ar21.svg"></a></code>
 <code><a href="https://git-scm.com/" target="_blank"><img height="50" src="https://www.vectorlogo.zone/logos/git-scm/git-scm-ar21.svg"></a></code>
<code><a href="https://github.com/" target="_blank"><img height="50" src="https://www.vectorlogo.zone/logos/github/github-ar21.svg"></a></code> -->
<!-- <code><a href="https://code.visualstudio.com/" target="_blank"><img height="50" src="https://www.vectorlogo.zone/logos/visualstudio_code/visualstudio_code-ar21.svg"></a></code>
<code><a href="https://www.python.org/" target="_blank"><img height="50" src="https://www.vectorlogo.zone/logos/python/python-ar21.svg"></a></code>-->
<!-- <code><a href="https://www.python.org/" target="_blank"><img height="50" src="https://www.vectorlogo.zone/logos/python/python-horizontal.svg"></a></code>-->
<code><a href="https://www.mysql.com" target="_blank"><img height="50" src="https://www.vectorlogo.zone/logos/mysql/mysql-ar21.svg"></a></code>


<p>
<img src="https://i.giphy.com/media/LMt9638dO8dftAjtco/200.webp" width="150"> 
<img src="https://i.giphy.com/media/KzJkzjggfGN5Py6nkT/200.webp" width="150">
<img src="https://i.giphy.com/media/IdyAQJVN2kVPNUrojM/200.webp" width="150"> 
<img src="https://media.giphy.com/media/UWt0rhp21JgLwoeFQP/giphy.gif" width ="150"/> 
<img src="https://media.giphy.com/media/kH6CqYiquZawmU1HI6/giphy.gif" width ="150"/> 
</p>

## Getting Started

 Step 1: 
  Git Clone the Repository 
  
    git clone https://github.com/brwali/PopcornPicks.git
    
  (OR) Download the .zip file on your local machine from the following link
  
    https://github.com/brwali/PopcornPicks
  
 Step 2:
   Follow the setup instructions in the installation documentation
   
    https://github.com/brwali/PopcornPicks/blob/master/docs/install.md
    
    
<b>Finally, start enjoying personalized movie recommendations!</b>

## Future Scope
PopcornPicks is a dynamic project with endless possibilities for expansion and enhancement. Here are some exciting avenues for future development:


1. **User Profiles and Preferences**: Continue to improve user profiles. More features could be added with friend interaction, such as ability to send messages. More data on the users could be persisted such as preferences and watch history for a more personalized movie discovery experience.

2. **Integration with Streaming Services**: Integrate with popular streaming services to provide real-time availability information and seamless access to recommended movies.
  
3. **Improved Recommendation Algorithm**: Enhance the recommendation engine with more advanced machine learning models and collaborative filtering techniques to provide even more accurate and personalized movie suggestions.
 
4. **Frontend rework**: Currently the frontend uses jquery, which is a bit dated. As the program becomes more complex, it may be nice to use a component based architecture such as React, Angular, or Blazor.

The future of PopcornPicks is full of potential, and we invite developers, movie lovers, and anyone passionate about cinema to join us in making this platform the ultimate movie companion. 

## Contribute to the Project!

Please refer to the [CONTRIBUTING.md](https://github.com/brwali/PopcornPicks/blob/master/CONTRIBUTING.md) if you want to contribute to the PopcornPicks source code. Follow all the guidelines mentioned in the same and raise a pull request, we would love to look at it ❤️❤️!

## Contributors
<table>
  <tr>
    <td><a href="https://github.com/brwali/PopcornPicks">Project 3</a></td>
    <td align="center"><a href="https://github.com/brwali/"><img src="https://avatars.githubusercontent.com/u/144480335?v=4" width="75px;" alt=""/><br /><sub><b>Brandon Walia</b></sub></a></td>
    <td align="center"><a href="https://github.com/nathankohen/"><img src="https://avatars.githubusercontent.com/u/99231385?v=4" width="75px;" alt=""/><br /><sub><b>Nathan Kohen</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/nfoster1492/"><img src="https://avatars.githubusercontent.com/u/144182217?v=4" width="75px;" alt=""/><br /><sub><b>Nicholas Foster</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/rpkenney/"><img src="https://avatars.githubusercontent.com/u/70106196?v=4" width="75px;" alt=""/><br /><sub><b>Robert Kenney</b></sub></a><br /></td>
  </tr>
</table>

[Aditya Pai Brahmavar](https://www.linkedin.com/in/adityapai16/)<br/>
[Ananya Mantravadi](https://www.linkedin.com/in/ananya-mantravadi/)<br/>
[Rishi Singhal](https://www.linkedin.com/in/rishi-singhal1101/)<br/>
[Samarth Shetty](https://www.linkedin.com/in/samarthshetty09/)<br/>

## Contact
In case of any issues, please e-mail your queries to popcornpicks777@gmail.com or raise an issue on this repository.<br>
Our team of developers monitors this e-mail address and would be happy to answer any and all questions you have about setup or use of this project!

## Join the PopcornPicks Community:

Contribute to the project and help us improve recommendations.
Share your experience and film discoveries with us.
Together, let's make PopcornPicks the ultimate movie companion!
PopcornPicks is more than just code; it's a passion for cinema, and we invite you to be a part of this exciting journey. Start exploring, sharing, and discovering movies like never before with PopcornPicks!
Let's make movie nights extraordinary together!

## License
This project is under the MIT License.
