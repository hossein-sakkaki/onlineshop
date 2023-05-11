def create_active_code(count):
    import random
    count-=1
    return random.randint(10**count, 10**(count+1)-1)

#---------==========================================================---------#
def send_sms(phone_number, message):
    pass

#---------==========================================================---------#
def send_email(email_add, message):
    pass

#---------==========================================================---------#
import os
from uuid import uuid4
class FileUpload:
    def __init__(self, dir, prefix):
        self.dir = dir
        self.prefix = prefix
        
    def upload_to(self, instance, filename):
        name , ext = os.path.splitext(filename)
        return f'{self.dir}/{self.prefix}/{uuid4()}{ext}'
    
#---------==========================================================---------#