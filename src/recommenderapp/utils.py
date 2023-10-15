""" Module contains utility functions used for various purposes in the backend """

import logging
import smtplib
from smtplib import SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import pandas as pd
import constants as c

def create_colored_tags(genres):
    """
        Utitilty function to create colored tags for different
        movie genres
    """
    # Define colors for specific genres
    genre_colors = {
        'Musical': '#FF1493',  # DeepPink
        'Sci-Fi': '#00CED1',  # DarkTurquoise
        'Mystery': '#8A2BE2',  # BlueViolet
        'Thriller': '#FF4500',  # OrangeRed
        'Horror': '#FF0000',  # Red
        'Documentary': '#228B22',  # ForestGreen
        'Fantasy': '#FF8C00',  # DarkOrange
        'Adventure': '#FFD700',  # Gold
        'Children': '#32CD32',  # LimeGreen
        'Film-Noir': '#000000',  # Black
        'Comedy': '#FFD700',  # Gold
        'Crime': '#8B0000',  # DarkRed
        'Drama': '#8B008B',  # DarkMagenta
        'Western': '#FF6347',  # Tomato
        'IMAX': '#7FFFD4',  # Aquamarine
        'Action': '#FF4500',  # OrangeRed
        'War': '#B22222',  # FireBrick
        '(no genres listed)': '#A9A9A9',  # DarkGray
        'Romance': '#FF69B4',  # HotPink
        'Animation': '#20B2AA'  # LightSeaGreen
    }
    tags = []
    for genre in genres:
        color = genre_colors.get(genre, '#CCCCCC')  # Default color if not found
        tag = f'<span style="background-color: {color}; color: #FFFFFF; \
            padding: 5px; border-radius: 5px;">{genre}</span>'
        tags.append(tag)
    return ' '.join(tags)

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

def create_movie_genres(movie_genre_df):
    """
        Utility function for creating a dictionary for movie-genres mapping
    """
    # Create a dictionary to map movies to their genres
    movie_to_genres = {}

    # Iterating on all movies to create the map
    for row in movie_genre_df.iterrows():
        movie = row[1]['title']
        genres = row[1]['genres'].split('|')
        movie_to_genres[movie] = genres
    return movie_to_genres
    

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
    # Load the CSV file into a DataFrame
    movie_genre_df = pd.read_csv('../../data/movies.csv')
    # Creating movie-genres map
    movie_to_genres = create_movie_genres(movie_genre_df)
    # Create the email message with HTML content
    html_content = c.EMAIL_HTML_CONTENT.format(
        '\n'.join(f'<li>{movie} \
            {create_colored_tags(movie_to_genres.get(movie, ["Unknown Genre"]))}</li><br>' \
            for movie in categorized_data['Liked']),
        '\n'.join(f'<li>{movie} \
            {create_colored_tags(movie_to_genres.get(movie, ["Unknown Genre"]))}</li><br>' \
            for movie in categorized_data['Disliked']),
        '\n'.join(f'<li>{movie} \
            {create_colored_tags(movie_to_genres.get(movie, ["Unknown Genre"]))}</li><br>' \
            for movie in categorized_data['Yet to Watch']))

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

    finally:
        server.quit()
