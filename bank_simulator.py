balance = 0
history = []
withdrawal_limit = 700

while True:
    print('===== BANK SIMULATOR =====\n')
    print('1. Check Balance')
    print('2. Deposit')
    print('3. Withdraw')
    print('4. Transaction History')
    print('5. Reset Session')
    print('6. Exit')
    print('===========================')
    choice = input('Pick an Option from Menu (1-to-6): ')

    if choice == '1':
        print(f"Available Balance: ${balance}")
    elif choice == '2':
        deposit = int(input('Enter an Amt to Deposit: '))
        balance += deposit
        history.append(f"Deposited: ${deposit}")
        print('--- Deposit Successful! ---')
        print(f"A Deposit of ${deposit} was made.")
    elif choice == '3':
        withdraw = int(input('Enter Amt you wish to Withdraw: '))
        if withdraw > balance:
            print('Insufficient Funds!')
        elif withdraw > withdrawal_limit:
            print('Withdrawal limit exceeded!')
        else:
            balance -= withdraw
            history.append(f"Withdrawn: ${withdraw}")
            print('Withdraw Successful!')
    elif choice == '4':
        print('--- Transaction History ---')
        if history == []:
            print('No transaction was made during this Session.')
        else:
            for transaction in history:
                print(transaction)
    elif choice == '5':
        print('Clearing Transaction History...')
        history.clear()
        balance = 0
        print('Session reset successfully!')
    elif choice == '6':
        print('Thank You for using Bank Simulator.\n GOODBYE.')
        break
    else:
        print('Invalid Option!\n Please, choose a Valid Option from Opt(1-6).')