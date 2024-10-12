# -*- coding: utf-8 -*-

import logging, ipaddress, subprocess, configparser
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser()
config.read('main-bot.ini')
configTg = config['telegram']
configScript = config['script']

async def ssh(update: Update, context: ContextTypes.DEFAULT_TYPE):
	if update.effective_chat != None:
		if update.effective_chat.id != configTg.getint('chat_id'):
			await context.bot.send_message( \
				chat_id=update.effective_chat.id, \
				text="This bot in intended to be used only by it''s owner")
			return

	ipAddrText = update.message.text[5:]
	logging.info(f"Got ssh command with argument: '{ipAddrText}'")

	try:
		ipAddr = ipaddress.ip_address(ipAddrText)
		if not ipAddr.is_global:
			logging.warning('Supplied IP address is not global, ignoring')
			await context.bot.send_message(chat_id=update.effective_chat.id, text='Supplied IP address is not global')
			return
	except:
		logging.warning(f"Argument '{ipAddrText}' does not look like IP address")
		await context.bot.send_message(chat_id=update.effective_chat.id, text='Invalid argument, shoud be an IP address')
		return
	
	script = subprocess.run(configScript['path'], shell=True, env={'REMOTE_IP':ipAddrText})
	if script.returncode != 0:
		logging.warning(f'Script failed with return code {script.returncode}')
		await context.bot.send_message(chat_id=update.effective_chat.id, text='Executing script failed')
		return
	
	logging.info('Successfully executed SSH script')
	

if __name__ == '__main__':
	application = ApplicationBuilder().token(configTg['token']).build()

	ssh_handler = CommandHandler('ssh', ssh)
	application.add_handler(ssh_handler)

	application.run_polling()
