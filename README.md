# Newelle Gemini Web API Extension
This uses [gemini_webapi](https://github.com/HanaokaYuzu/Gemini-API) and requires Gemini/Google cookies from the supported browsers by `browser-cookie3` package. 

## Installation
1. Download [gemini-webapi.py](https://raw.githubusercontent.com/hurryman2212/Newelle-Gemini-Webapi/refs/heads/main/gemini-webapi.py) file.
2. [Install the extension](https://newelle.qsk.me/docs/User-guide-to-Extensions).
3. In Newelle's Preferences window, select General, scroll down and install `gemini_webapi` and `browser-cookie3`.

## Bug
Currently, both `create_gem` and `update_gem` method from the `gemini_webapi` package does not work in this Newelle's extension.
You need to login to the Gemini Web/App version and create the gem of which name is specifically `gemini-webapi` to supplement the system prompt, initially. 
The log from `stderr` can be helpful as it dumps the completed system prompt string.
