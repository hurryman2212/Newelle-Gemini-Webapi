# Newelle Gemini Web API Extension
<p>
  <img align="left" width="200" src="https://raw.githubusercontent.com/HanaokaYuzu/Gemini-API/master/assets/banner.png"/>
  <a href="https://github.com/topics/newelle-extension">
    <img width="100" alt="Download on Flathub" src="https://raw.githubusercontent.com/qwersyk/Assets/main/newelle-extension.svg"/>
  </a>
  <br/>
  <b>
    This is an extension for <a href="https://github.com/qwersyk/Newelle">Newelle</a> that allows you to use <a href="https://github.com/HanaokaYuzu/Gemini-API">gemini_webapi</a>. This requires Gemini/Google cookies from the supported browsers by `browser-cookie3` package.
  </b>
</p>

## Installation
1. Download [gemini-webapi.py](https://raw.githubusercontent.com/hurryman2212/Newelle-Gemini-Webapi/refs/heads/main/gemini-webapi.py) file.
2. [Install the extension](https://newelle.qsk.me/docs/User-guide-to-Extensions).

## Bug
Currently, both `create_gem` and `update_gem` method from the `gemini_webapi` package does not work in this Newelle's extension.
You need to login to the Gemini Web/App version and create the gem of which name is specifically `gemini-webapi` to supplement the system prompt, initially. 
The log from `stderr` can be helpful as it dumps the completed system prompt string.
