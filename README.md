# Setting up private repos in GitLab

Script for creating private repos by template (import_url)

## Install requirements

```shell
pip3 install -r /path/to/requirements.txt
```

## Run

### Creating repos and inviting users

Get list of all users from [settings.json](config/settings.json)\
Create a repo with a username using template (import_url) from [settings.toml](config/settings.toml)

```shell
python3 inviter.py
```

### Approve signing up users

By default, GitLab requires you to approve the registration of all users.

Get white list of users from [settings.json](config/settings.json)

```shell
python3 inviter.py
```

## Settings

You can see an example of all settings in [settings.json](config/settings.json)
and [settings.toml](config/settings.toml)

I recommend creating `config/.secrets.json` and `config/.secrets.toml` files following the pattern `config/settings.json`
and `config/settings.toml`\
To store sensitive settings