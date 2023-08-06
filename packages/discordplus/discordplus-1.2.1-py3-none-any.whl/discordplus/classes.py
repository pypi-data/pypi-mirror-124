import asyncio
import inspect
import os
from typing import Optional, Union, Iterable, Callable, List

import discord
from discord import Member, Embed, Message, Reaction, Color
from discord.abc import Messageable, User
from discord.ext.commands import Bot, DefaultHelpCommand, Cog, ExtensionAlreadyLoaded, command, Context
from discord_slash import SlashCommand, SlashContext
from discord_slash.cog_ext import cog_slash

from .extra import MessageChannel
from .lib import try_except, ExceptionFormat, try_add_reaction, try_delete, try_send, Config, RequiredValue


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


class SlashConfig(Config, auto_setup=True):
    sync_commands: bool = False
    debug_guild: Optional[int] = None
    delete_from_unused_guilds: bool = False
    sync_on_cog_reload: bool = False
    override_type: bool = False
    application_id: Optional[int] = None


class BotPlusConfig(Config, auto_setup=True):
    token: str = RequiredValue()
    command_prefix: Union[str, Callable[[Bot, Message], str]] = None
    log_channel_id: int = None
    help_command = DefaultHelpCommand()
    description = None
    color = Color.default()

    slash_config: Optional[SlashConfig] = None


class BotPlus(Bot):
    def __init__(self, config: BotPlusConfig):
        super().__init__(
            command_prefix=config.command_prefix,
            help_command=config.help_command,
            description=config.description,
            **config.extra_options
        )
        self._token = config.token
        self.log_channel_id = config.log_channel_id
        self._color = config.color

        slash_config = config.slash_config
        self._slash = None
        if slash_config is not None:
            self._slash = SlashCommand(self, **slash_config.options)

        from .coglib import CogLib
        self._library = CogLib(self)

        self.api = None
        self.__disabled_cogs__ = []
        self.__beta_cogs__ = []

    @property
    def library(self):
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
            if not os.path.exists(file):
                continue
            if any(part.startswith('_') for part in file.replace('\\', '/').split('/')):
                continue
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

        # 2.0 - Add override to add_cog
        super(BotPlus, self).add_cog(cog)
        if hasattr(cog, '__beta__') and cog.__beta__:
            self.__beta_cogs__.append(cog)
            print(f'"{cog.qualified_name}" is tagged beta but it has been activated')

    def run(self):
        return super(BotPlus, self).run(self._token)


class CogPlus(Cog):
    __disabled__ = False
    __beta__ = False

    class Status:
        BetaDisabled = 'BetaDisabled'
        BetaEnabled = 'BetaEnabled'
        Disabled = 'Disabled'
        Enabled = 'Enabled'

    def __init__(self, bot: BotPlus):
        self.bot = bot

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


class CommandPlus:
    name: str = None
    description: str = None
    guild_ids: List[int] = None
    options: List[dict] = None
    default_permission: bool = True
    permissions: dict = None
    connector: dict = None

    def __init__(self, cog: CogPlus):
        self.cog = cog

    def init_slash_command(self):
        cmd = getattr(self, 'slash_command', None)
        if cmd is None:
            raise NotImplementedError

        wrapper = self.cog.bot.slash_command(
            name=self.name,
            description=self.description,
            guild_ids=self.guild_ids,
            options=self.options,
            default_permission=self.default_permission,
            permissions=self.permissions,
            connector=self.connector
        )

        return wrapper(cmd)

    def init_command(self, **attr):
        cmd = getattr(self, 'command', None)
        if cmd is None:
            raise NotImplementedError

        wrapper = command(name=self.name, description=self.description, **attr)

        return wrapper(cmd)
