# Flask AUTH

A Simple FLask Boilerplate for JWT Authentication

## Setup

- Setup your virtual environment && install dependencies

```bash
virtualenv venv && source venv/bin/activate

pip install -r requirements.txt
```

- Copy the `.env.sample` file to `.env` you could edit it to your needs

```bash
cp env.sample .env
```

- start test APIs server at `localhost:5001`

```bash
flask run
```

__Note__: Don't worry about the first issue you got relate to `JSONDecodeError: Expecting value: line 1 column 1 (char 0)` you could skip it and test the api or if this disturb you, you can change the link to `localhost:5001/docs`.

### API

Register

```bash
POST /api/auth/register
{
    username:'user',
    email: 'email@gmail.com',
    password: 'password'
}
```

Sign-In

```bash
POST /api/auth/login
{
    email: 'email@gmail.com',
    password: 'password'
}
```

Logout

```bash
POST /api/auth/logout
```
