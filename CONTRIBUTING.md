## Contributing:

* If you would like to contribute and collaborate with this repository, then please inform us through email at popcornpicks504@gmail.com.

## Purpose of Contributing:

* To develop our product and take it to the next level.
* To enhance the already existing feature.
* To make the product more efficient.
* To resolve critical bugs encountered.
* Helping the community by delivering a better product.
* Help us find solutions to computationally/memory-intensive processes
* Help us to scale the system to a larger database
* To run the email notifier feature - make your own Gmail account and password and replace the same in the utils.py(function: send_email_to_user(recipient_email, categorized_data))

## Our Table Of Contents

- .github/workflows  
  - all GitHub workflow YAML files  
- proj2  
   - score_card.md  
  
- src  
  - prediction_scripts    
     - item_based.py   
  - recommenderapp
    - static
      - script.js
      - stylesheet.css
    - templates
      - landing_page.html
      - search_page.html
      - success.html
    - app.py
    - search.py
    - utils.py
  
- test  
    - test_predict.py  
    - test_search.py  
    - test_util.py  
  
- .gitignore

- CODE_OF_CONDUCT.md

- CONTRIBUTING.md

- LICENSE

- README.md

- requirements.txt

- setup.py

## Style checkers standards:
* Use the `pylance` package for Python (VS code), and use `black` for auto-styling and auto-formatting the code.
* Use 'pylint' for proper coding standards


## Code of Conduct:

* Please go through the [Code of Conduct](https://github.com/adipai/PopcornPicks/blob/master/CODE_OF_CONDUCT.md) before you begin contributing. This project and everyone participating in it is governed by the Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to popcornpicks504@gmail.com.

## Pull Request Submission Guidelines

* Installing Git makes contributing to the repository easier
* To start contributing to the repository make sure you fork the repository first
* Create a new branch to develop the project 
* Write code to contribute and commit to create a pull request.
* Pass all the test cases that we have mentioned in the test folder and ensure the code passes the workflow checks.
* One of the repository administrators will review the pull request and merge the changes.

## Code Style Guide 

* Python language(Version 3.x) has been used to build this project repository
* Make sure to add the functionalities in the form of modules
* Any code that is not tested should be committed to the test codes in the code folder. After they are successfully tested, the  main code can be updated.
* Variable names should be self-explanatory
* Add comments in the code so that a new contributor can understand the functionality of the modules easily
* `black` is used as linter
* 'Pylint' used for proper coding standards
