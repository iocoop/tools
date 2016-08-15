# get_member_id.py

## Usage

1. Install the [`refreshbooks`](https://pypi.python.org/pypi/refreshbooks/) python package by running `sudo pip install refreshbooks`
2. Obtain the Freshbooks API key for our IO Coop account by logging in to Freshbooks and going to [My Account... Freshbooks API](https://iocoop.freshbooks.com/apiEnable). The value is in the `Authentication Token` field
3. Store this API token in a config file. The default config file location is `/etc/freshbooks.cfg` but you can store it elsewhere if you use the `--config` argument to indicate the file location. The file is an `ini` style file and looks like this

        [Freshbooks]
        api_token: abcdef0123456789abcdef0123456789

4. Run `get_member_id.py` passing in the email address of the member as an argument

        python get_member_id.py jdoe@example.com

You can view usage for the tool with `get_member_id.py --help`
