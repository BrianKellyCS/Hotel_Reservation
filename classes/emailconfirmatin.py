import smtplib
#import ssl

def send_email(message, email_recipient):
    smtp_server = "stmp.gmail.com"
    port = 587
    sender_email = "teamjabhotel@gmail.com"
    password = 'eqrlzonjnrqmgwob'
    message = 'Hello there user.'
    
    
    #context = ssl.create_default_context
    
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(send_email,password)
        server.sendmail(sender_email,email_recipient, message)
        
    except Exception as e:
        print(e)
        
    finally:
        server.quit()
