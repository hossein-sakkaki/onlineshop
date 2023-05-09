def create_active_code(count):
    import random
    count-=1
    return random.randint(10**count, 10**(count+1)-1)
    
    
def send_sms(phone_number, message):
    pass

def send_email(email_add, message):
    pass
