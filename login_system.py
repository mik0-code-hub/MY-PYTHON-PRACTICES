class User:
    def __init__(self, user_name, pin):
        self.user_name = user_name
        self.pin = pin        
    def check_pin(self):
        try:
            entered_pin = input('Enter your 4-digit PIN to Login: ')
            if len(entered_pin) != 4:
                print('Your PIN should be 4-digits Only!')
            elif entered_pin == self.pin:    
                print('Access Granted!')
            else:
                print('Access Denied!\nWrong PIN.')
        except ValueError:
            print('Invalid input.\nYour PIN should consist of Numbers Only!!')

    def change_pin(self):
        print('=== CHANGE PIN ===')
        try:
            entered_pin = input('Enter your 4-digit PIN to Login: ')
            new_pin = input('Enter New PIN: ')
            if entered_pin == self.pin:
                self.pin = new_pin
                print('Your PIN has been Updated successfully!')
            else:
                print('Incorrect current PIN, cannot change.')
        except ValueError:
            print('Invalid PIN.')
            print('Your PIN should consist of Numbers Only!!')

bob_acct = User('Bob', '1234')
bob_acct.check_pin()
bob_acct.change_pin()