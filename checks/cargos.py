from discord.ext import commands


class NoGuild(commands.CommandError):

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "This command cannot be used in private messages")


class NoRole(commands.CommandError):

    def __init__(self, missing_roles: str | None = None, *args) -> None:

        missing = [f"'{role}'" for role in missing_roles]

        if len(missing) > 2:
            fmt = f"{', '.join(missing[:-1])}, or {missing[-1]}"
        else:
            fmt = " or ".join(missing)

        message = f"You don't have the role: {fmt}"

        super().__init__(message, *args)


def has_roles(*roles):
    def check(ctx: commands.Context) -> commands.check:

        if ctx.guild is None:
            raise NoGuild()

        roles2 = []
        for i in roles:
            if type(i) == int:
                roles2.append(i)
            elif type(i) == str:
                roles2.append(i.lower())

        v = 0
        while True:

            if v == ctx.author.roles.__len__() or ctx.author.roles.__len__() < 2:
                raise NoRole(roles2)
            elif ctx.author.roles[v].id in roles2 or ctx.author.roles[v].name.lower() in roles2:
                break
            else:
                v += 1
        return True

    return commands.check(check)
