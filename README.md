# README

An application to enable you to login and have your own bookmarks so you don't need to be on a single device.

Add a list, say a holiday you are going on.
Add a section to the list, say flight information.
Add a link to the flight information section, say a link to the airline check-in website.

The login screen:

![Alt text](login.png?raw=true "Login")

The Links screen:

![Alt text](links.png?raw=true "Links")

## Notes

Setup to deploy to Heroku, and using postgres for the database. 

The following environment variables are used:

- ADMIN_EMAIL
- ADMIN_NAME

- DJANGO_SETTINGS_MODULE
- SECRET_KEY

- DEFAULT_FROM_EMAIL
- EMAIL_HOST
- EMAIL_HOST_PASSWORD
- EMAIL_HOST_USER
- EMAIL_PORT