class User:
    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self._password_hash = password_hash
class AuthSystem:
    def __init__(self):
        self.users = {}
        self.emails = set()
        self.logged_in_users = set()

    # User Registration
    def register_user(self, username, email, password):
        if not username.isalnum():
            return "Username must contain (a-z), (1-3) Only!"
        if username in self.users:
            return f"Username '{username} is already taken."
        if '@' not in email or '.' not in email:
            return "Invalid email format."
        if email in self.emails:
            return f"The email '{email}' is already registered."
        # Written by mik0-logic™
        user = User(username, email, password)
        self.users[username] = user
        self.emails.add(email)
        return f"Success!\nThe account '{username}' has been created successfully."
    # Login*****
    def login_user(self, username, password):
        if username not in self.users:
            return "This username does not exist."
        user = self.users[username]
        if user._password_hash != password:
            return "Incorrect Password."
        self.logged_in_users.add(username)
        return f"Welcome back, {username}!"
    # LogOut*****
    def logout_user(self, username, password):
        if not username in self.logged_in_users:
            return f"The user '{username}' is not currently Logged in!"
        user = self.users[username]
        if user._password_hash != password:
            return "Incorrect Password!\nRe-authentication failed."
        self.logged_in_users.remove(username)
        return f"'{username}' has been securely Logged out"
    # Written by mik0-logic™
    # Update User Info
    def update_user(self, username, password, new_username=None, new_password=None):
        if username not in self.logged_in_users:
            return "Login to Update your account."
        user = self.users[username]
        if user._password_hash != password:
            return "Incorrect Password."
        # Password Change
        if new_password is not None:
            if new_password == password:
                return "New password can not be same as Current password."
            user._password_hash = new_password
        # Username change
        if new_username is not None:
            if new_username in self.users:
                return f"The username '{new_username}' is already taken."
            self.users[new_username] = user
            del self.users[username]
            user.username = new_username
            self.logged_in_users.remove(username)
            self.logged_in_users.add(new_username)
        return "Account settings updated Successfully!"
    # List users
    @property
    def list_users(self):
        if not self.users:
            return "No registered users found in the System."
        return list(self.users.keys())

# Instantiate Obj
auth_system = AuthSystem()
while True:
    print('\n=== AUTHENTICATION SYSTEM MENU ===')
    print('1. Register User')
    print('2. Login User')
    print('3. Logout User')
    print('4. Update User Settings')
    print('5. List All users')
    print('6. Exit')
    print('======================')

    try:
        choice = input('\nSelect an Option (1-6): ').strip()
        if choice == '1':
            print('--- Register User ---')
            username = input('Enter username: ').strip()
            email = input('Enter email: ').strip()
            password = input('Enter password: ')
            feedback = auth_system.register_user(username, email, password)
            print('\n---> Feedback:', feedback)

        elif choice == '2':
            print('--- Login User ---')
            username = input('Enter username: ').strip()
            password = input('Enter password: ')
            feedback = auth_system.login_user(username, password)
            print('\n---> Feedback:', feedback)

        elif choice == '3':
            print('--- Logout User ---')
            # Written by mik0-logic™
            username = input('Enter username: ').strip()
            password = input('Enter password: ')
            feedback = auth_system.logout_user(username, password)
            print('\n---> Feedback:', feedback)

        elif choice == '4':
            print('--- Update User Settings ---')
            username = input('Enter username: ').strip()
            password = input('Enter password: ')
            new_username = input('Enter new username: ').strip() or None
            new_password = input('Enter new password: ') or None
            feedback = auth_system.update_user(username, password, new_username, new_password)
            print('\n---> Feedback:', feedback)

        elif choice == '5':
            print('--- List all Users ---')
            feedback = auth_system.list_users
            print('\n--> Registered Users:', feedback)

        elif choice == '6':
            print('--> Exiting Authentication System <--')
            print('Thank you for using our Authentication system')
            break
        else:
            print("Invalid Choice!\nChoose from option (1-6)")
    except Exception as e:
        print(f"\nAn unexpected error occured: {e}")