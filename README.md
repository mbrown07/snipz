# snipz

Look at the following link to get your gmail app password to store as an environment variable to send emails:
https://blog.coffeeinc.in/how-to-send-a-mail-using-flask-mail-and-gmail-smtp-in-python-eb235e5b2048


Do the following before sending emails:

Windows:
setx MAIL_USERNAME "your_mail_username" (i.e, 'some_email@gmail.com)
set MAIL_USERNAME="your_mail_username"
echo %MAIL_USERNAME%

setx MAIL_PASSWORD "your_mail_password"
set MAIL_PASSWORD="your_mail_password"
echo %MAIL_PASSWORD%

Mac:
export MAIL_USERNAME="YOUR_MAIL_USER" (i.e, 'some_email@gmail.com)
echo $MAIL_USERNAME

export MAIL_PASSWORD="YOUR_MAIL_PASSWORD" (received from link above - make sure to read the steps)
echo $MAIL_PASSWORD