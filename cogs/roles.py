import discord
from discord.ext import commands
import asyncio
from discord.ext.commands import has_permissions

import json


class Roles(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bannedUsers = []


	# assign roles based on adding a reaction
	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		if user.id == 604820657620123648: # don't assign roles for BotName
			return
		if reaction.message.channel.id == 601451037659889664: # check for right channel
			if reaction.emoji == "🔵":
				#add_role = discord.utils.get(user.guild.roles, name = "Revival Craft Player")
				#await user.add_roles(add_role)

				def is_me(m):
					return m.author.id == user.id

				await user.send("Please enter your Minecraft username")
				try:
					msg1 = await self.bot.wait_for('message', check=is_me, timeout=6) 
				except asyncio.TimeoutError:
					await user.send("Request timed out; please readd reaction to the message to continue...")
					self.bannedUsers.append(user.id)
					await reaction.message.remove_reaction("🔵", user)
					return

				await user.send("Please re-enter your Minecraft username")
				try:
					msg2 = await self.bot.wait_for('message', check=is_me, timeout=6) 
				except asyncio.TimeoutError:
					await user.send("Request timed out; please readd reaction to the message to continue...")
					self.bannedUsers.append(user.id)
					await reaction.message.remove_reaction("🔵", user)
					return

				if msg1.content == msg2.content:
					add_role = discord.utils.get(user.guild.roles, name = "Revival Craft Player")
					await user.add_roles(add_role)
					await user.send("Revival Craft Player role added.")
				else:
					self.bannedUsers.append(user.id)
					await reaction.message.remove_reaction("🔵", user)
					await user.send("The names you entered were not the same; please readd reaction to the message to restart the process...")


			elif(str(reaction.emoji) == "🔴"):
				add_role = discord.utils.get(user.guild.roles, name = "Toxic")
				await user.add_roles(add_role)
				await user.send("Toxic role added.")
			elif(str(reaction.emoji) == "⚪"):
				add_role = discord.utils.get(user.guild.roles, name = "Event Notifications")
				await user.add_roles(add_role)
				await user.send("Event Notifications role added.")


	# remove roles based on removing a reaction
	@commands.Cog.listener()
	async def on_reaction_remove(self, reaction, user):
		if reaction.message.channel.id == 601451037659889664: # check for right channel
			if user.id in self.bannedUsers:
				self.bannedUsers.remove(user.id)
				return
			print(2)
			if str(reaction.emoji) == "🔵":
				remove_role = discord.utils.get(user.guild.roles, name = "Revival Craft Player")
				await user.remove_roles(remove_role)
				await user.send("`Revival Craft Player` role removed.")
			elif(str(reaction.emoji) == "🔴"):
				remove_role = discord.utils.get(user.guild.roles, name = "Toxic")
				await user.remove_roles(remove_role)
				await user.send("`Toxic` role removed.")
			elif(str(reaction.emoji) == "⚪"):
				remove_role = discord.utils.get(user.guild.roles, name = "Event Notifications")
				await user.remove_roles(remove_role)
				await user.send("`Event Notifications` role removed.")


	@commands.command(pass_context = True)
	@has_permissions(administrator=True)
	async def update_roles(self, ctx):
		# delete existing messages
		channel = self.bot.get_channel(601451037659889664) # get the channel to clear the messages from
		i = 0
		async for message in channel.history():
			i += 1
			await message.delete()
		print("Roles channel cleared\n")

		# update the roles channel for autoroles
		embed = discord.Embed(color=1768431) # set up embed
		embed.add_field(name = f"Self-Assignable Role Menu", value = f"""
			🔵 : `Revival Craft Player`\n
			🔴 : `Toxic`\n
			⚪ : `Event Notifications`""", inline=False)
		embed.set_footer(text="React to give yourself a role")
		channel_roles = await channel.send(embed=embed)
		# add the emojis to react with
		await channel_roles.add_reaction("🔵")
		await channel_roles.add_reaction("🔴")
		await channel_roles.add_reaction("⚪")

		# ❗ : `Access to Information Channels`\n


def setup(bot):
	bot.add_cog(Roles(bot))
