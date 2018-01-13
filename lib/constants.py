# Date: 12/16/2017
# Author: Ethical-H4CK3R
# Description: Contains configurations

credentials = 'Cracked.txt'
database_path = 'sessions/sessions.db'
useragents = 'useragents/useragents.txt'

# colors 
colors = {
 'red': '\033[31m',
 'blue': '\033[34m',
 'white': '\033[0m',
 'green': '\033[32m',
 'yellow': '\033[33m'
 }

# tor
tor_ip = '127.0.0.1'
tor_port = 9050

# time settings
proxy_time_out = 5
ip_fetch_timeout = 10
network_manager_time = 75
visit_login_page_timeout = 15

# limits
proxies_max_size_ = 8 # total amount of proxies to store
proxies_wait_time = 1 # time to wait before retying IP fetch
failures_max_size = 2 # after this amount of fails change the ip
passlist_max_size = 5 # maximum size of passwords to hold at once
brwsr_max_refresh = 3 # the total amount a times a page can be refreshed
session_save_time = 5 # the time to write or rewrite the session information to database
proxy_total_usage = 8 # the amount of times a proxy can be used before requesting a new proxy

# Twitter's details
twitter_url = 'https://m.twitter.com/login'
twitter_username_field = 'session[username_or_email]'
twitter_password_field = 'session[password]'
twitter_authentic_response = ['user_id']
twitter_locked_response = ['/search']

# Facebook's details
facebook_url = 'https://mbasic.facebook.com/login.php'
facebook_username_field = 'email'
facebook_password_field = 'pass'
facebook_authentic_response = ['home.php?', 'server_Init', 'serverLID', 'save-device']
facebook_locked_response = ['/help/contact/']

# Instagram's details
instagram_url = 'https://www.instagram.com/accounts/login/?force_classic_login'
instagram_username_field = 'username'
instagram_password_field = 'password'
instagram_authentic_response = ['feedpagecontainer.js', 'Challenge.js', 'comment_likes']
instagram_locked_response = ['FBSignupPage.js']

# supported sites
sites = {
'twitter' : {
 'name':'Twitter',
 'url': twitter_url,
 'username_field': twitter_username_field,
 'password_field': twitter_password_field,
 'key': twitter_authentic_response,
 'lock': twitter_locked_response,
 'wait': 3815,
 'delay': 0.5
 }, 'facebook' : {
 'name': 'Facebook',
 'url': facebook_url,
 'username_field': facebook_username_field,
 'password_field': facebook_password_field,
 'key': facebook_authentic_response,
 'lock': facebook_locked_response,
 'wait': 4096,
 'delay': 5.7 
 }, 'instagram' : {
 'name':'Instagram',
 'url': instagram_url,
 'username_field': instagram_username_field,
 'password_field': instagram_password_field,
 'key': instagram_authentic_response,
 'lock': instagram_locked_response,
 'wait': 3724,
 'delay': 0.25
 }
}
