# Start up

1) install docker & docker-compose
2) run `make init-dev`
3) fill `POSTGRES_USER` and `POSTGRES_PASSWORD` to `./.envs/.local/.postgres`
3) fill `CELERY_FLOWER_USER` and `CELERY_FLOWER_PASSWORD` to `./.envs/.local/.django`
4) fill `STRIPE_PUBLIC_KEY` and `STRIPE_SECRET_KEY`to `./.envs/.local/.django`
5) fill `SOCIAL_AUTH_FACEBOOK_NAME`
        `SOCIAL_AUTH_FACEBOOK_APP_ID`
        `SOCIAL_AUTH_FACEBOOK_SECRET`
        `SOCIAL_AUTH_GOOGLE_NAME`
        `SOCIAL_AUTH_GOOGLE_APP_ID`
        `SOCIAL_AUTH_GOOGLE_SECRET`
        to `./.envs/.local/.django`
6) run `make build-dev`
7) run `create-stripe-dev` to create stripe plans
8) run `set-socials-dev` to set social ids, names and keys

Run With Demo Data(https://wiki.itransition.com/display/ONE33T/Demo+Data):
1) run `make recreatedb-demo-dev` to create dev environment with demo data.

Run Without Demo Data:
1) run `make start-dev`
2) run `make createsuperuser-dev` and create admin

localhost:8000 - backend (Django 2)
localhost:4200 - frontend (Angular 7)


# To run tests

1) stop all containers dev/prod if running(`make down-dev` or `make down-prod`)
2) run `make build-test`
3) run `make start-test`
4) Frontend tests: `make frontend-all-test`
5) Backend tests: `make backend-all-test`


# Front end code style

There are code style agreements:
Front-end: https://wiki.itransition.com/display/ONE33T/Front-end+style+guide
Back-end: https://wiki.itransition.com/display/ONE33T/BE+Style+Guide
