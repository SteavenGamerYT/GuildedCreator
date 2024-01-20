# `GUILDEDCREATOR`
https://t.me/guildedfunny
## `✴️` `INTRODUCTION`
**GuildedCreator**, a sequel to [**TokenCreator**](https://github.com/anhonor/TokenCreator), is a simple tool that creates email verified accounts for https://guilded.gg. This is done fully requests-based, and only requires rotating proxies to run. I will be creating an AIO for guilded, as verified accounts have no restrictions whatsoever.
## `✴️` `REQUIREMENTS`
- `pip install -r requirements.txt`
- `python3 -m pip install -r requirements.txt`
## `✴️` `SETUP`
`config.json`
```json
{
    "threads": 125, // Thread Amount
    "thread_retry_delay": 1.5, // Thread Retry Delay

    "full_name": "", // Account's "Display Name" -- [OPTIONAL]

    // DON'T CHANGE IF YOU DON'T UNDERSTAND
    "verification_attempts": 7,
    "verification_delay": 1.5
}
```
