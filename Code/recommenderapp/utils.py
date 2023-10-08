import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

def beautify_feedback_data(data):
    """
    Utility function to beautify the feedback json containing predicted movies for sending in email
    """
    # Create empty lists for each category
    yet_to_watch = []
    like = []
    dislike = []

    # Iterate through the data and categorize movies
    for movie, status in data.items():
        if status == 'Yet to watch':
            yet_to_watch.append(movie)
        elif status == 'Like':
            like.append(movie)
        elif status == 'Dislike':
            dislike.append(movie)

    # Create a category-dictionary of liked, disliked and yet to watch movies
    categorized_data_dict = {"Liked":like, "Disliked":dislike, "Yet to Watch":yet_to_watch}

    return categorized_data_dict

        

def send_email_to_user(recipient_email, categorized_data):
    """
    Utility function to send movie recommendations to user over email
    """

    # Email configuration
    smtp_server = 'smtp.gmail.com'
    # Port for TLS
    smtp_port = 587  
    sender_email = 'popcornpicks504@gmail.com'

    # Use an app password since 2-factor authentication is enabled
    sender_password = '' 
    subject = 'Your movie recommendation from PopcornPicks'

    # Create the email message
    message = MIMEMultipart('alternative')
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Create the email message with HTML content
    html_content = """
    <html>
      <head></head>
      <body>
        <h1 style="color: #333333;">Movie Recommendations from PopcornPicks</h1>
        <p style="color: #555555;">Dear Movie Enthusiast,</p>
        <p style="color: #555555;">We hope you're having a fantastic day!</p>
        <div style="padding: 10px; border: 1px solid #cccccc; border-radius: 5px; background-color: #f9f9f9;">
          <h2>Your Movie Recommendations:</h2>
          <h3>Movies Liked:</h3>
          <ul style="color: #555555;">
            {}
          </ul>
          <h3>Movies Disliked:</h3>
          <ul style="color: #555555;">
            {}
          </ul>
          <h3>Movies Yet to Watch:</h3>
          <ul style="color: #555555;">
            {}
          </ul>
        </div>
        <p style="color: #555555;">Enjoy your movie time with PopcornPicks!</p>
        <p style="color: #555555;">Best regards,<br>PopcornPicks Team</p>
      </body>
    </html>
    """.format('\n'.join(f'<li>{movie}</li>' for movie in categorized_data['Liked']),
               '\n'.join(f'<li>{movie}</li>' for movie in categorized_data['Disliked']),
               '\n'.join(f'<li>{movie}</li>' for movie in categorized_data['Yet to Watch']))

    # Attach the HTML email body
    message.attach(MIMEText(html_content, 'html'))
    
    # Connect to the SMTP server
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        # Start TLS encryption
        server.starttls()  
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, message.as_string())
        logging.info("Email sent successfully!")

    except Exception as e:
        logging.warning(f'Email could not be sent. Error: {str(e)}')

    finally:
        server.quit()
