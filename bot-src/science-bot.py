#!/usr/bin/env python

import discord
import logging
import os

from discord.ext.commands import Bot


bot = Bot(command_prefix="\"")


@bot.command()
async def testmsg(ctx, *, txt):
    """
    This generates a text message
    """
    await ctx.send(txt)


if __name__ == "__main__":
    SCIENCE_BOT_TOKEN = os.getenv('SCIENCE_BOT_TOKEN')
    bot.run(SCIENCE_BOT_TOKEN)
