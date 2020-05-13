import requests
import argparse


def ask_number_of_people():
    user_input = input('How many people are in your company? ')

    try:
        number = int(user_input)
        if number < 0:
            print('Sorry, what?')
            return -1
    except ValueError:
        print('The number of guests must be a number!')
        return -1


def ask_age_of_the_youngest():
    user_input = input('How old is the youngest guest? ')

    try:
        return int(user_input)
    except ValueError:
        print('Age must be a number!')
        return -1


def ask_duration_of_stay():
    user_input = input('How many days would you like to stay? ')

    try:
        return int(user_input)
    except ValueError:
        print('The length of stay must be a number!')
        return -1


def create_reservation(args):
    guests = ask_number_of_people()
    youngest = ask_age_of_the_youngest()
    duration = ask_duration_of_stay()
    if guests == -1 or duration == -1 or youngest == -1:
        print('Sorry, incorrect data, we can\'t complete such reservation')
        return

    reservation_id = requests.post(f'http://{args.host}:{args.port}/create', data=dict(
        guests=guests,
        youngest=youngest,
        duration=duration
    )).text

    print(f'Your reservation ID is {reservation_id}, we will compete it soon')


def leave(args):
    reservation_id = int(input('Please, enter your reservation ID: '))
    try:
        int(reservation_id)
    except ValueError:
        print('Incorrect ID')
        return

    try:
        reservation_id = str(reservation_id)
    except ValueError:
        print('Incorrect ID')
        return

    status = requests.get(f'http://{args.host}:{args.port}/get_status', params=dict(
        id=reservation_id
    )).text

    if status == 'completed':
        bill = requests.post(f'http://{args.host}:{args.port}/departure', params=dict(
            id=reservation_id
        )).text
        print(f'You have to pay {bill} rubles. Looking forward to see you again!')
    else:
        print('Sorry, you can\'t leave right now')


def get_status(args):
    reservation_id = input('Please, enter your reservation ID: ')

    try:
        int(reservation_id)
    except ValueError:
        print('Incorrect ID')
        return

    try:
        reservation_id = str(reservation_id)
    except ValueError:
        print('Incorrect ID')
        return

    status = requests.get(f'http://{args.host}:{args.port}/get_status', params=dict(
        id=reservation_id
    )).text

    if status == 'outdated':
        print('The guests have already left')
    elif status == 'queue':
        print('Booking in progress')
    elif status == 'completed':
        print('Your reservation is made, welcome!')
    elif status == 'rejected':
        print('Sorry, we cannot accommodate you in our hotel')
    else:
        print('No such reservation')


def get_position(args):
    reservation_id = input('Please, enter your reservation ID: ')

    try:
        int(reservation_id)
    except ValueError:
        print('Incorrect ID')
        return

    try:
        reservation_id = str(reservation_id)
    except ValueError:
        print('Incorrect ID')
        return

    position = requests.get(f'http://{args.host}:{args.port}/get_position', params=dict(
        id=reservation_id
    )).text

    print(f'Your position is {position}')


def get_bill(args):
    reservation_id = input('Please, enter your reservation ID: ')

    try:
        int(reservation_id)
    except ValueError:
        print('Incorrect ID')
        return

    try:
        reservation_id = str(reservation_id)
    except ValueError:
        print('Incorrect ID')
        return

    bill = requests.get(f'http://{args.host}:{args.port}/get_bill', params=dict(
        id=reservation_id
    )).text

    print(f'You should pay {bill} rubles')


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default=8000, type=int)
    return parser


def main_exit():
    user_command = input('Are you sure you want to leave the hotel? (YES/NO) ')
    if user_command == 'YES':
        print('Looking forward to see you again!')
        exit(0)
    elif user_command == 'NO':
        print('We will continue your registration')
    else:
        print('Sorry, we do not understand, try again')


def help():
    print('Welcome to our hotel!\n'
          'If you want to create reservation, please, enter \'create\'\n'
          'If you want to check your reservation status, please, enter \'get_status\'\n'
          'If you want to know, how much your stay will cost you, please, enter \'get_bill\'\n'
          'If you want to know your position in the queue, please, enter \'get_position\'\n'
          'If you want to leave our hotel, please, enter \'leave\'\n'
          'If you want to end current session, please, enter \'exit\'')


def main():
    parser = create_parser()
    args = parser.parse_args()

    while True:
        try:
            user_command = input('Enter your command(enter \'help\' for details) ')
            if user_command == 'help':
                help()
            elif user_command == 'create':
                create_reservation(args)
            elif user_command == 'leave':
                leave(args)
            elif user_command == 'get_status':
                get_status(args)
            elif user_command == 'get_position':
                get_position(args)
            elif user_command == 'get_bill':
                get_bill(args)
            elif user_command == 'exit':
                main_exit()
            else:
                print('No such command, enter \'help\' to see list of commands')
        except KeyboardInterrupt:
            main_exit()


if __name__ == '__main__':
    main()
