import getpass
import sys
from pyelice import Elice, EliceResponseError

ORG = 'kaist'
UID_FILENAME = 'uids.txt'
ROLES = {
    'banned': 15,
    'preview_only': 30,
    'student': 45,
    'ta': 60,
    'head_ta': 90,
    'instructor': 120,
    'admin': 150
}

def get_uids():
    f = open(UID_FILENAME, 'r')
    uids = []
    for line in f:
        if line.strip():
            uids.append(line.strip())
    return uids

def fetch_users(elice, course_id):
    users_iter = elice.get_iter(
        '/common/course/user/list/',
        { 'course_id': course_id },
        lambda x: x['users'])
    users = list(users_iter)
    return users

def filter_users_with_uids(users, uids):
    filtered_users = []
    for user in users:
        if 'organization_uid' in user and user['organization_uid'] in uids:
            filtered_users.append(user)
    return filtered_users

def get_power(user):
    try:
        user_power = user['user_course_role']['power']
    except KeyError:
        user_power = 0
    return user_power

def change_roles(elice, course_id, users, power):
    for user in users:
        try:
            result = elice.post(
                '/common/course/role/edit/',
                {
                    'course_id': course_id,
                    'user_id': user['id'],
                    'power': power,
                    'is_confirmed': True
                })
        except EliceResponseError as err:
            print('Failed to change role of user %s with error message: "%s"' % (user['firstname'], err.message))

def login():
    print('Login to %s.elice.io' % ORG)
    elice = Elice()
    email = input('Email: ')
    password = getpass.getpass('Password: ')
    elice.login(email, password, org=ORG)

def main():
    elice = login()
    print('Which course do you want to change user roles in?')
    course_id = int(input('Course ID (https://kaist.elice.io/courses/{course_id}/): '))
    print('Which role do you want to give to the users?')
    roles_string = '/'.join(ROLES.keys())
    role = input('Role ID (%s):' % roles_string)
    power = ROLES[role]
    force_ans = input('Do you want to give this role to the users who already has more powerful role than this (Y/N)?')
    force = force_ans.strip().lower() == 'y'

    print('Fetching users from the course...')
    users = fetch_users(elice, course_id)
    print('Fetched %d users.' % len(users))
    print('Filtering users with uids from "uids.txt"...')
    uids = get_uids()
    users = filter_users_with_uids(users, uids)
    print('Found %d uid matching users.' % len(users))
    if force:
        users = [user for user in users if get_power(user) != power]
        print('Found %d matching users with role other than %s.'  % (len(users), role))
    else:
        users = [user for user in users if get_power(user) < power]
        print('Found %d matching users with role less powerful than %s.'  % (len(users), role))
    print('Changing roles of users...')
    change_roles(elice, course_id, users, power)
    print('Done.')

if __name__ == '__main__':
    main()

elice = Elice()
