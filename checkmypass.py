import requests
import hashlib
import sys

# list of hashed (anonymous encoded secured passwords, we provide
# only part of it (5 symbols)and receive a list of all that has this beginning)


# request API response, of beginning of hashed func
def request_api_data(query_char):
    url = 'http://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res


# splits full hashed pass to beginning and tail, checks the tail
# and tells how many times the password was hacked
def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


# check password if it exists in api response - gets the list
# of all passwords with beginning of hashed pass
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


# provides answer
def main(password):
    count = pwned_api_check(password)
    hidden_pass = password.replace(password, '•'*len(password))
    if count:
        return f'{hidden_pass} was hacked {count} times, you should be more creative! '
    else:
        return f'{hidden_pass} hasn\'t been hacked yet. Carry on!'


if __name__ == '__main__':
    sys.exit(main(password))