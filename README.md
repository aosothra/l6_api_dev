# L6_API - XKCD VK Autoposter

This script automatically posts random XKCD comic strip in specified VK community page.

### Installation guidelines

You must have Python3 installed on your system.
You may use `pip` (or `pip3` to avoid conflict with Python2) to install dependencies.
```
pip install -r requirements.txt
```
It is strongly advised to use [virtualenv/venv](https://docs.python.org/3/library/venv.html) for project isolation.

This script uses `.env` file in root folder to store variables neccessary for operation. So, do not forget to create one!

Below you can find how contents of your `.env` file should look like, and how to set it up:

```
VK_ACCESS_TOKEN = 'putyouraccesstokenhere'
VK_APP_ID = '1234567'
VK_GROUP_ID = '123456789'
```

In order for the script to work, you must have a VK community page (or group), where you have moderating privileges. 

Begin your setup process by creating new standalone application ([here](https://vk.com/apps?act=manage)). Go to *Manage > Settings* of your newly created app to find **App ID**. Save it in `VK_APP_ID` field of your `.env` file.

`VK_ACCESS_TOKEN` can be acquired after you properly authorize your new app. Proper way to do that in our case is using [Implicit Flow](https://vk.com/dev/implicit_flow_user). Make sure you specify correct scope for your application: `photos,groups,wall,offline`

Here is how your Implicit Flow Auth request looks (this might get outdated, so refer to the Development Docs for guidelines):
```
https://oauth.vk.com/authorize?client_id=1&display=page&scope=photos,groups,wall,offline&response_type=token&v=5.131
```
where `client_id` is app ID we got in previous step.

Once submitted this request will redirect you to confirmation page, and your new `access_token` will be specified in URL parameters. Save it in `VK_ACCESS_TOKEN` field of your `.env` file.

**BE CAREFUL!** Under no circumstances share your acquired `access_token` as it gives 3rd parties control over your account activities!

`VK_GROUP_ID` can be easily acquired from [here](https://regvk.com/id/).

### Basic usage (for the lack of any other...)

```
py main.py 
```

### Project goals

This project was created for educational purposes as part of [dvmn.org](https://dvmn.org/) Backend Developer course.