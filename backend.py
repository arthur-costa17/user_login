# The only thing used here is the Yes_no function. The class has not been used as of yet.

def request_password(username):
     return input(f'Enter the password for {username}')
     
def Yes_no():
    answer = input('Y/n ')
    if answer in ['Y','']:
         return True
    else:
         return False

class User:
    def __init__(self,username: str, password: str, logged_in = False):
        self.username = username
        self.logged_in = logged_in
        self.password = password # How do I prevent someone just writing self.password? I mean that can only happen if they
        # acces the Python file. Is that an easy thing to do?

        # having a password as an attribute might be problematic.
    
    
    def log_in(self) -> None:
        entry = request_password(self.username)
        if entry != self.password:
             raise 'Wrong password!'
        if self.logged_in == True:
            print(f'{self.username} is already logged in!')
        else:
            self.logged_in = True
            print(f'{self.username} is now logged in')
    
    
    def log_out(self):
        entry = request_password(self.username)
        if entry != self.password:
            raise 'Wrong password!'
        if self.logged_in == False:
                print(f'{self.username} is already logged out!')
        else:
            self.logged_in = False
            print(f'{self.username} is now logged out!')
        



