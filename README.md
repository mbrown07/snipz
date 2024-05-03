# snipz

Look at the following link to get your gmail app password to store as an environment variable to send emails: <br/>
https://blog.coffeeinc.in/how-to-send-a-mail-using-flask-mail-and-gmail-smtp-in-python-eb235e5b2048 <br/>


Do the following before sending emails. If it doesnt work, check your environment and redo these steps. <br/>

Windows: <br/>
setx MAIL_USERNAME "your_mail_username" (i.e, 'some_email@gmail.com) <br/>
set MAIL_USERNAME="your_mail_username" <br/>
echo %MAIL_USERNAME% <br/>

setx MAIL_PASSWORD "your_mail_password" <br/>
set MAIL_PASSWORD="your_mail_password" <br/>
echo %MAIL_PASSWORD% <br/>

Mac: <br/>
export MAIL_USERNAME="YOUR_MAIL_USER" (i.e, 'some_email@gmail.com) <br/>
echo $MAIL_USERNAME <br/>

export MAIL_PASSWORD="YOUR_MAIL_PASSWORD" (received from link above - make sure to read the steps) <br/>
echo $MAIL_PASSWORD <br/>

after this, all you need to do to run the program is cd /snipz then execute 'flask run' in terminal <br/>