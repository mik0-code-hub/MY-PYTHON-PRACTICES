temperature = 0
pressure = 0
ph_level = 0

while True:
    print('===== CHEMICAL REACTOR MONITOR =====')
    print('1. Set Reactor Temperature')
    print('2. Set Reactor Pressure')
    print('3. Set pH Level')
    print('4. View Current Readings')
    print('5. Exit')
    print('====================================')
    choice = input('Enter your choice: ')

    if choice == '1':
        print('--- Set Reactor Temperature ---')
        try:
            user_temp = float(input('Enter temperature value: '))
            if user_temp < 0 or user_temp > 500:
                print('Temperature must be between 0 and 500 degrees!')
            else:
                temperature = user_temp
                print('Temperature set successfully!')
        except ValueError:
            print('Invalid Input!\nPlease enter a Number.')
    
    elif choice == '2':
        print('--- Set Reactor Pressure ---') 
        try:
            user_pressure = float(input('Enter Pressure value: '))
            if user_pressure < 0 or user_pressure > 300:
                print('Pressure must be between 0 and 300 bar!')
            else:
                pressure = user_pressure
                print('Pressure set successfully!')
        except ValueError:
            print('Invalid Input!\nPlease enter a Number.')
    
    elif choice == '3':
        print('--- Set pH Level ---')
        try:
            user_ph = float(input('Enter a pH value: '))
            if user_ph < 0 or user_ph > 14:
                print('pH level must be between 0 and 14!')
            else:
                ph_level = user_ph
                print('pH level set successfully!')
        except ValueError:
            print('Invalid Input!\nPlease enter a Number.')

    elif choice == '4':
        print('--- Current Reactor Readings ---')
        print(f"Temperature: {temperature} degrees")
        print(f"Pressure: {pressure} bar")
        print(f"pH Level: {ph_level}")

    elif choice == '5':
        print('Shutting down reactor monitor.\nGoodbye!')

    else:
        print('The Menu you selected is Invalid!!!\nPlease, choose a Menu between [1 and 5].')