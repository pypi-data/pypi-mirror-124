# XPHN_ezDiscord
Easily  use and create Discord webhooks and simple Discord bots.

Webhook text Example:
```
import ezDiscord
ezDiscord.ezWebhook.Send("your_webhook_url","send_from_username","message_content") 
#Of course replace them with your own values (url,username,message)
```
Webhook file/image example:
```
import ezDiscord
ezDiscord.ezWebhook.File("webhook_url","from_username","file_name_along_with_file_extension")
#Again, replace them with your own values (url,username,filename)
```
Bot Example:
```
import ezDiscord
ezDiscord.ezBot.Respond("your_bot_token","message_to_which_the_bot_will_reply","message_which_bot_will_send_back_as_reply")  
#Telling Again,replace them with your own values (token,trigger,reply)
```