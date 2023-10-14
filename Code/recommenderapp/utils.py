""" Module contains utility functions used for various purposes in the backend """

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import constants as c

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
    categorized_data_dict = {"Liked": like,
                             "Disliked": dislike, "Yet to Watch": yet_to_watch}

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
    sender_password = 'uxnd shis sazo mstj'
    subject = 'Your movie recommendation from PopcornPicks'

    # Create the email message
    message = MIMEMultipart('alternative')
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Create the email message with HTML content
    html_content = c.EMAIL_HTML_CONTENT.format(
    '\n'.join(f'<li>{movie}</li>' for movie in categorized_data['Liked']),
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

    except SMTPException as e:
        # Handle SMTP-related exceptions
        logging.error("SMTP error while sending email: %s", str(e))

    except Exception as e:
        # Handle other exceptions
        logging.error("An unexpected error occurred while sending email: %s", str(e))

    finally:
        server.quit()
