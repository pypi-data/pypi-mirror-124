# dude CLI

# Installation and Setup
```
pipx install nubium-dude
```

## Further setup
In order to use `dude`, you will need to set a few things up.

## Environment Variables and Configuration

`dude` can largely be configured via a `config.env` file, an example of which
can be found at `./dude/config.env` (which is also used by default if one not provided. It
will basically set any possible working defaults). Simply set the path of:

`DUDE_CONFIG_DOTENV`

Additionally, you'll likely need to set, at minimum:

`DUDE_CREDENTIALS_DOTENV`={path to a .env with various credentials}

NOTE: this will likely change in the future and secrets will be downloaded by default for you.


Lastly, there are (new) variables related to `nubium-utils`; these can just go in your `dude` creds.env file:


```
RHOSAK_USERNAME=(same as preprod)
RHOSAK_PASSWORD=(same as preprod)
TEST_CLUSTER=(ask Tim)
```

# Usage

## examples of common tasks

- Create topics:

    `dude topics create topic_a,topic_b`


- Build requirements.txt:

    (in app root folder): `dude app build_reqs`


- Run app:
    
    (in app root folder): `dude app run`


## Known limitations:

- Currently, no proper error handling if topics already exist (create) or are missing (delete); you will
  need to validate whether your topics exist else it will fail.

- Test coverage is almost non-existent.


# Development
There's two ways to develop: 

## option 1
if you only need to make changes to `dude`, the easiest thing to do is just install an
editable version of the library:
```
pipx install -e /PATH/TO/DUDE/REPO
```

## option 2
Another option more suitable for coordinating changes that involve multiple nubium
libraries is instead making a new venv, sourcing it, and then:
```
pip install -e /PATH/TO/DUDE/REPO
```
then you can install `-e` versions of all the `nubium-{}` packages. You'll of course need to
source this environment when you test.

### once we finish adding more tests...
Run tests via
```
pipx install tox
tox && tox -e cov
```
