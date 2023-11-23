# Steps for setting up the repository and running the web app

**Step 1:**
  **Git Clone the Repository** 
  
    git clone https://github.com/brwali/PopcornPicks.git
    
  (OR) Download the .zip file on your local machine from the following link
  
    https://github.com/brwali/PopcornPicks/

**Step 2:**
   **Install the required packages by running the following command in the terminal** 
   
    pip install -r requirements.txt
    
**Step 3:**
    **Run the following command in the terminal**

    cd src/recommenderapp
    python app.py
    
**Step 4:**
    **Open the URL in your browser:**  

      http://127.0.0.1:5000/

**You can also leave Steps 2-4 and directly run the setup.py file for setting up all dependencies and running the web app!**

    python setup.py

**NOTE: For the email notifier feature - create a new gmail account, replace the sender_email variable with the new email and sender_password variable with its password (2 factor authentication) in the utils.py file (function: send_email_to_user(recipient_email, categorized_data)).**