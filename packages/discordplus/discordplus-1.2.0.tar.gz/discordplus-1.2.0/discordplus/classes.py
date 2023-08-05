import asyncio
import inspect
import json
import os
from threading import Thread
from typing import Optional, Union, Iterable, Callable, List

import discord
from discord import Member, Embed, Message, Reaction, Color
from discord.abc import Messageable, User
from discord.ext.commands import Bot, DefaultHelpCommand, Cog, ExtensionAlreadyLoaded
from discord_slash import SlashCommand
from discord_slash.cog_ext import cog_slash
from flask import Flask, jsonify, request, Response
from requests import post

from .extra import MessageChannel, __agent__
from .lib import try_except, ExceptionFormat, try_add_reaction, try_delete, try_send
from .task import TaskPlus


class PreMessage:
    __args: list = None

    @staticmethod
    def init_args():
        if PreMessage.__args is not None:
            return

        PreMessage.__args = []
        args = inspect.getfullargspec(Messageable.send)
        for arg in args.args + args.kwonlyargs:
            if arg != 'self':
                PreMessage.__args.append(arg)

    def __init__(self, **kwargs):
        PreMessage.init_args()
        self.args = {k: v for k, v in kwargs.items() if k in PreMessage.__args}
        self._message = None

    @property
    def message(self) -> discord.Message:
        return self._message

    def clone(self) -> 'PreMessage':
        return PreMessage(**self.args)

    async def send(self, ctx: Messageable):
        self._message = await ctx.send(**self.args)
        return self._message

    async def try_send(self, ctx: Messageable):
        return await try_send(ctx, premessage=self)


class BotPlus(Bot):
    def __init__(self, command_prefix, log_channel_id=None, help_command=DefaultHelpCommand(), description=None, **options):
        super().__init__(command_prefix=command_prefix, help_command=help_command, description=description, **options)
        self.log_channel_id = log_channel_id
        self._library = CogLib(self)
        self._slash = SlashCommand(self, sync_commands=True)

        self.api = None
        self.__disabled_cogs__ = []
        self.__beta_cogs__ = []

    @property
    def library(self) -> 'CogLib':
        return self._library

    def slash_command(self, *, name: str = None, description: str = None, guild_ids: List[int] = None, options: List[dict] = None, default_permission: bool = True, permissions: dict = None, connector: dict = None):
        return self._slash.slash(name=name, description=description, guild_ids=guild_ids, options=options, default_permission=default_permission, permissions=permissions, connector=connector)

    async def log(self, premessage: PreMessage):
        channel = self.get_channel(self.log_channel_id)
        return await premessage.try_send(channel)

    async def log_exception(self, exception: Exception, *details: str):
        return await self.log(ExceptionFormat(exception, *details).premessage)

    async def confirm(self, channel: MessageChannel, premessage: PreMessage, target: Union[User, Member], timeout: Optional[int] = None, delete_after: bool = False) -> Optional[bool]:
        emoji = await self.get_reaction(channel, premessage, target, timeout, delete_after, ['✅', '❌'])
        return None if emoji is None else emoji == '✅'

    async def get_reaction(self, channel: MessageChannel, premessage: PreMessage, target: Union[User, Member], timeout: Optional[int] = None, delete_after: bool = False, emotes: Iterable = None) -> Optional[str]:
        message: discord.Message = await premessage.send(channel)
        await try_add_reaction(message, emotes)

        emoji = None
        try:
            event = await self.wait_for('reaction_add', check=self.check_reaction(message, target, emotes), timeout=timeout)
            emoji = event[0].emoji
        finally:
            if delete_after:
                await try_delete(message)
            else:
                await try_except(message.clear_reactions)
        return emoji

    async def get_answer(self, channel: MessageChannel, premessage: PreMessage, target: Union[User, Member], timeout: Optional[int] = None, delete_after: bool = False, forbid: bool = False, forbid_premessage: PreMessage = None) -> Optional[str]:
        message: discord.Message = await premessage.send(channel)
        content = None
        respond = None

        try:
            respond = await self.wait_for('message', check=self.check_message(channel, target, forbid, forbid_premessage), timeout=timeout)
            content = respond.content
        finally:
            if delete_after:
                await try_delete(message)
                await try_delete(respond)

            return content

    def check_message(self, channel: MessageChannel, target: Union[User, Member], forbid: bool = False, forbid_premessage: PreMessage = None):
        if forbid:
            if forbid_premessage is None:
                forbid_premessage = PreMessage(embed=Embed(title='**ERROR**', description=f'Only {target.mention} can send message here', colour=discord.Colour.red()))
            forbid_premessage.delete_after = max(forbid_premessage.delete_after, 20)

            def check(message: Message):
                if message.channel.id == channel.id and message.author.id not in (target.id, self.user.id):
                    asyncio.ensure_future(try_delete(message))
                    asyncio.ensure_future(forbid_premessage.send(channel))
                    return False
                return message.channel.id == channel.id and message.author.id == target.id
        else:
            def check(message: Message):
                return message.channel.id == channel.id and message.author.id == target.id

        return check

    def check_reaction(self, message: Message, target: Union[User, Member], emotes: list = None):
        def check(reaction: Reaction, user):
            if reaction.message.id == message.id and user.id != self.user.id:
                asyncio.ensure_future(reaction.remove(user))
            if user != target or reaction.message.id != message.id:
                return False
            return emotes is None or len(emotes) == 0 or str(reaction.emoji) in [str(e) for e in emotes]

        return check

    def load_extensions(self, *files: str):
        for file in files:
            if os.path.isdir(file):
                within_files = [f'{file}/{within_file}' for within_file in os.listdir(file)]
                self.load_extensions(*within_files)
            else:
                path = file.replace('/', '.').replace('\\', '.')
                if path.endswith('.py'):
                    path = path[:-3]

                try:
                    self.load_extension(path)
                except ExtensionAlreadyLoaded:
                    self.reload_extension(path)

    @property
    def cogs_status(self):
        cogs = [(name, CogPlus.Status.BetaEnabled if hasattr(cog, '__beta__') and cog.__beta__ else CogPlus.Status.Enabled)
                for name, cog in self.cogs.items()]
        cogs.extend([(cog.qualified_name, CogPlus.Status.BetaDisabled if hasattr(cog, '__beta__') and cog.__beta__ else CogPlus.Status.Disabled)
                     for cog in self.__disabled_cogs__])
        return dict(cogs)

    def add_cog(self, cog, *, override: bool = False):
        if hasattr(cog, '__disabled__') and cog.__disabled__:
            if cog not in self.__disabled_cogs__:
                self.__disabled_cogs__.append(cog)
                print(f'"{cog.qualified_name}" is tagged disabled.')
            return

        super(BotPlus, self).add_cog(cog, override=override)
        if hasattr(cog, '__beta__') and cog.__beta__:
            self.__beta_cogs__.append(cog)
            print(f'"{cog.qualified_name}" is tagged beta but it has been activated')


class CogPlus(Cog):
    __disabled__ = False
    __beta__ = False

    class Status:
        BetaDisabled = 'BetaDisabled'
        BetaEnabled = 'BetaEnabled'
        Disabled = 'Disabled'
        Enabled = 'Enabled'

    @staticmethod
    def slash_command(*, name: str = None, description: str = None, guild_ids: List[int] = None, options: List[dict] = None, default_permission: bool = True, permissions: dict = None, connector: dict = None):
        return cog_slash(name=name, description=description, guild_ids=guild_ids, options=options, default_permission=default_permission, permissions=permissions, connector=connector)

    # Decorators
    @staticmethod
    def disabled(cls):
        if issubclass(cls, CogPlus):
            cls.__disabled__ = True
        else:
            raise TypeError(f'CogPlus.disabled only accept a sub-class of "CogPlus" not a "{type(cls)}"')
        return cls

    @staticmethod
    def beta(cls):
        if issubclass(cls, CogPlus):
            cls.__beta__ = True
        else:
            raise TypeError(f'CogPlus.disabled only accept a sub-class of "CogPlus" not a "{type(cls)}"')
        return cls


class API(CogPlus):
    def __init__(self, bot: BotPlus, import_name, **kwargs):
        self.bot = bot
        self.app = Flask(import_name, **kwargs)
        self._auth = None
        self._thread = None

        self.app.add_url_rule('/', None, self.ping)
        self.app.add_url_rule('/ping', None, self.ping)
        self.app.add_url_rule('/vote', None, self.vote, methods=['POST'])

    def set_auth(self, auth):
        self._auth = auth

    def main(self):
        return jsonify(Name=self.bot.user.name, Status='Online' if self.bot.is_ready() else 'Offline', Ping=self.bot.latency * 1000 if self.bot.is_ready() else 0)

    def ping(self):
        return jsonify(Status='Online' if self.bot.is_ready() else 'Offline', Ping=self.bot.latency * 1000 if self.bot.is_ready() else 0)

    def vote(self):
        req_auth = request.headers.get('Authorization')
        if self._auth == req_auth and self._auth is not None:
            data = request.json or request.form or request.args or {}
            if data.get('type', None) == 'upvote':
                event_name = 'vote'
            elif data.get('type', None) == 'test':
                event_name = 'test_vote'
            else:
                return Response(status=401)
            self.bot.dispatch(event_name, data)
            return Response(status=200)
        else:
            return Response(status=401)

    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        self._thread = Thread(target=lambda: self.app.run(host, port, debug, load_dotenv=load_dotenv, **options))
        self._thread.setDaemon(True)
        self._thread.start()


class TopGGPoster(TaskPlus):
    def __init__(self, bot: BotPlus, token: str, timer: float = 1800):
        super().__init__(bot, seconds=timer)
        self.token = token
        self.shard_count: Optional[int] = None
        self.shard_id: Optional[int] = None

        self.headers = {
            'User-Agent': __agent__,
            'Content-Type': 'application/json',
            'Authorization': self.token
        }

    @TaskPlus.execute
    def post(self):
        payload = {'server_count': len(self.bot.guilds)}
        if self.shard_count is not None:
            payload["shard_count"] = self.shard_count
        if self.shard_id is not None:
            payload["shard_id"] = self.shard_id
        return post('https://top.gg/api/bots/stats', data=json.dumps(payload), headers=self.headers)


class CogLib:
    def __init__(self, bot: BotPlus):
        self.bot = bot

        self._TopGGTask = None
        self._PSOP = None

    def activate_api(self, import_name, host=None, port=None, vote_auth=None):
        self.bot.api = API(self.bot, import_name)
        self.bot.add_cog(self.bot.api, )
        self.bot.api.set_auth(vote_auth)
        self.bot.api.run(host=host, port=port)
        return self.bot.api

    def activate_topgg_poster(self, token: str, timer: float = 1800):
        self._TopGGTask = TopGGPoster(self.bot, token, timer)
        self._TopGGTask.start()
        return self._TopGGTask

    def disable_topgg_poster(self):
        self._TopGGTask.stop()

    def activate_prefix_send_on_ping(self, premessage: Union[PreMessage, Callable[[Message], PreMessage]] = None):
        import re

        if premessage is None:
            def _premessage(message: Message):
                return PreMessage(emded=Embed(title='Prefix', description=f'My prefix is {self.bot.get_prefix(message)}', color=Color.green()))
        elif isinstance(premessage, PreMessage):
            def _premessage(message: Message):
                return premessage
        else:
            _premessage = premessage

        async def custom_event(message: Message):
            content = message.content
            if re.match(f'^\s*<@{id}>\s*$', content) and message.author.id != self.bot.user.id:
                await _premessage(message).try_send(message.channel)

        self._PSOP = custom_event
        self.bot.add_listener(self._PSOP, 'on_message')

    def disable_prefix_send_on_ping(self):
        self.bot.remove_listener(self._PSOP, 'on_message')
