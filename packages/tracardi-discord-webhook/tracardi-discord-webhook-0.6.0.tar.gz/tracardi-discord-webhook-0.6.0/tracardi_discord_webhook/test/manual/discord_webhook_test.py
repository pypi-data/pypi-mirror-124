from tracardi_discord_webhook.plugin import DiscordWebHookAction
from tracardi_plugin_sdk.service.plugin_runner import run_plugin
init = {
    "url": "https://discord.com/api/webhooks/902092877243494450/-55O7I7p1jERLpzA75Nz2Z-_3maFn3u7Jv2a9hjKiKoM2mpRMDzercTJhP5QOkX2BUnJ",
    "message": "Message from Tracardi bot",
    "username": "risto"
}

payload = {

}

result = run_plugin(DiscordWebHookAction, init, payload)

print(result)
