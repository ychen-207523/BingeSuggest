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

    # Create a plain text string for the categorized data
    categorized_data_str = "Movies Yet to Watch:\n" + "\n".join(yet_to_watch) + "\n\n"
    categorized_data_str += "Movies Liked:\n" + "\n".join(like) + "\n\n"
    categorized_data_str += "Movies Disliked:\n" + "\n".join(dislike)

    return categorized_data_str

def send_email_to_user(recipient_email, message_body):
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
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Attach the email body
    message.attach(MIMEText(message_body, 'plain'))

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
