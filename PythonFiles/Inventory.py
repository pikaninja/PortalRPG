import csv
import sqlite3
import random
from random import randint
import itertools
import discord
from discord.ext import commands

class Inventory(commands.Cog):
    def create_inventory():
        with sqlite3.connect('inventory.db') as conn:
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='inventory'")

            if c.fetchone() is None: #user_id will be used to access the inventory of a player, item_id is to insert an item to inventory at slot
                c.execute('''CREATE TABLE inventory(
                    user_id INTEGER, 
                    item_id INTEGER,
                    slot INTEGER
                    PRIMARY KEY (user_id, slot)
                    CHECK (slot >= 1 AND slot <= 32)
                )''')
    
    def insert_into_inventory(user_id, item_id, slot):
        with sqlite3.connect('items.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO inventory (user_id, item_id, slot) VALUES (?, ?, ?)", (user_id, item_id, slot))
    
    @commands.command()
    async def get_inventory(self, ctx):
        user_id = ctx.message.author.id

        with sqlite3.connect('inventory.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM inventory WHERE user_id = ?', (user_id))
    
    @commands.command()
    async def item_info(self, ctx, *args):
        args = [arg for arg in args if not isinstance(arg, discord.ext.commands.Context)]
        name = " ".join(args)
        try:
            with sqlite3.connect('items.db') as conn:
                c = conn.cursor()
                c.execute('SELECT * FROM items WHERE NAME = ?', (name,))
                row = c.fetchone()
                if row:
                    embed = discord.Embed(title=f"{row[1]}'s Information", color=0x00ff00)
                    embed.add_field(name="ID", value=f"{row[0]}", inline=True)
                    embed.add_field(name="type", value=f"{row[2]}", inline=True)
                    embed.add_field(name="rarity", value=f"{row[3]}", inline=True)
                    embed.add_field(name="damage", value=f"{row[4]}", inline=True)
                    embed.add_field(name="attack", value=f"{row[5]}", inline=True)
                    embed.add_field(name="defense", value=f"{row[6]}", inline=True)
                    embed.add_field(name="description", value=f"{row[7]}", inline=True)
                    embed.add_field(name="character", value=f"{row[8]}", inline=True)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("item not found.")
        except sqlite3.Error as e:
            print(e)
            await ctx.send("An error occurred while retrieving item information.")

def setup(bot):
    bot.add_cog(Inventory())