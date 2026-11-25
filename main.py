import backend as b
import psycopg2 as ps
import datetime as dt

conn = ps.connect(
            host = 'localhost',
            dbname = 'username',
            user = 'username',
            password = 'password',
            port = 5432
        )
cur = conn.cursor()

cur.execute("SELECT username FROM user_data")
username_list = cur.fetchall()
#print(username_list)
# Printing this list you will see that the result is a list of single tuples. Each username shows up as a singlet, instead
# of as a string. Which is why the code below has been corrected to have 'while (username,) not in username_list', instead
# of 'while username not in username_list'

print("Would you like to login? ('n' leads you to account creation) ")
if b.Yes_no():
    
    # Note that everything below, up until the else statement way below, is a result of wanting to login. There are
    # two possibilities, one tries to log into an existing account, or thinks they have an account, but realy don't
    # and so are taken to account creation.
    
    # enter a username
    username = input('Enter a username: ')
    while (username,) not in username_list: 
        print('This username does not exist. Would you like to create a new account? ')
        if b.Yes_no():
            # take to username creation
            username = input('Create your username: ')
            while (username,) in username_list:
                username = input('This username is already taken, please try again: ')
            print("This username is available!")
            different_passwords = True
            while different_passwords:
                password = input("Create a password: ")
                password_check = input("Re-enter password: ")
                different_passwords = (password != password_check)
                if different_passwords:
                    print("Passwords do not match! Password creation will restart!")
            
            # Now need to add entries to database
            cur.execute("INSERT INTO user_data (username,password) VALUES (%s,%s)",(username, password)) # Update database with new user
            print(f"Account created! You are now logged in as '{username}'!")
            
        else:
            username = input("You selected 'n', please enter your username: " )

    if (username,) in username_list: # This line is redundant I think
        print('Username found!')

    cur.execute("""SELECT last_login_deny FROM user_data WHERE username = %s""", (username,))
    last_login_deny = cur.fetchone()[0] # Recall that fetchone() will return a tuple, I just need the first element.
    current_login = dt.datetime.today() # Fetches current day and time of login
    delta = current_login - last_login_deny 
    delta_in_seconds = delta.total_seconds()
    if delta_in_seconds < 300:
        print(f"The 5 minutes since your last denied login are still not over, please wait {int(300 - delta_in_seconds)}"
              ,f"\nseconds until trying to log into the account with username '{username}'")
    else:
        # Big indent was done here.
        password = input(f"Enter the password for the account with username '{username}': ")
        cur.execute("""SELECT password FROM user_data WHERE username = %s""",(username,))
        the_password_tuple = cur.fetchone()
        password_attempts = 4
        while password not in the_password_tuple and password_attempts > 0:
            password = input(f"Wrong password. You have {password_attempts} more attempt(s) left, please try again: ")
            password_attempts -= 1

        if password_attempts == 0:
            print("Incorrect password entered too many times! Please wait 5 minutes before trying again!")
            last_login_deny = dt.datetime.today()
            cur.execute("""UPDATE user_data SET last_login_deny  = %s WHERE username = %s""", (last_login_deny,username)) # Updates database
        else: 
            print(f"You are now logged in as '{username}'!")

            
else: # Not logging in, take to account creation:
    username = input('Create your username: ')
    while (username,) in username_list:
        username = input('This username is already taken, please try again: ')
    print("This username is available!")
    different_passwords = True
    while different_passwords:
        password = input("Create a password: ")
        password_check = input("Re-enter password: ")
        different_passwords = (password != password_check)
        if different_passwords:
            print("Passwords do not match! Password creation will restart!")

    # Now need to add entries to database
    cur.execute("INSERT INTO user_data (username,password) VALUES (%s,%s)",(username, password)) # This is not working...
    
    print(f"Account created! You are now logged in as '{username}'!")


conn.commit()
cur.close()
conn.close()

# If someone tries to login, and fails too many times, I might try and add a feature where you have to wait 5 minutes before
# being able to try again. What I could do is that if the passwords_attempts variable hits zero, then a time gets entered
# into the user_data database. And everytime someone tries to login into the account before 5 minutes is up, then it won't
# let them
# something like: cur.execute("SELECT last_login_deny FROM user_data WHERE username = %s",(username,))
# if... 

# Ok the login cooldown thing has been added, and it works great. Now I think we need to add something where a user can
# reset their password. Where should this feature be in the code? It has to be in the signing in section. Not the account
# creation section. But there's trouble, there needs to be something different to the username which allows someone to
# reset their password, like maybe their date of birth or email.

# I was told that, only allowing access for a correct username AND password is a lot more secure than saying that a username
# found. If a password is wrong, say that the uusername and password combination doesn't exist, if a username is wrong then
# say the same thing. The combination is incorrect, not specifically the username or password. This seems to be quite
# though.










