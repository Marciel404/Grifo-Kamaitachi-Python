import os
import helps
from dotenv import load_dotenv
from os import getenv


def getdotenv(name: str):
    load_dotenv()
    return getenv(name)


def getallComands(opt: str):
    l = ""

    for i in os.listdir("commands/Administracao"):
        if "**Administração**" not in l:
            l += "**Administração**"
        if not i.startswith("__"):
            if i not in l:
                try:
                    name = getattr(helps, f'{i[:-3]}_{opt}')()
                except:
                    name = "Descrição não provida"

                l += f"\n↳{i[:-3]}: {name}"

    l += getModCommands(opt)
    l += getStaffCommands(opt)
    l += getStaffeCapsCommands(opt)
    l += getCapsCommands(opt)
    l += getEligosCommands(opt)
    l += getEquipeEventosCommands(opt)
    l += getCallPvCommands(opt)

    return l


def getModCommands(opt: str):
    l = ""
    for i in os.listdir("commands/Moderacao"):
        if "**Moderação**" not in l:
            l += "\n\n**Moderação**"
        if not i.startswith("__"):
            if i not in l:
                try:
                    name = getattr(helps, f'{i[:-3]}_{opt}')()
                except:
                    name = "Descrição não provida"

                l += f"\n↳{i[:-3]}: {name}"
    return l


def getStaffCommands(opt: str):
    l = ""
    for i in os.listdir("commands/Staff"):
        if "**Staff**" not in l:
            l += "\n\n**Staff**"
        if not i.startswith("__"):
            if i not in l:
                try:
                    name = getattr(helps, f'{i[:-3]}_{opt}')()
                except:
                    name = "Descrição não provida"

                l += f"\n↳{i[:-3]}: {name}"
    return l


def getStaffeCapsCommands(opt: str):
    l = ""
    for i in os.listdir("commands/Staff e Caps"):
        if "**Staff e Caps**" not in l:
            l += "\n\n**Staff e Caps**"
        if not i.startswith("__"):
            if i not in l:
                try:
                    name = getattr(helps, f'{i[:-3]}_{opt}')()
                except:
                    name = "Descrição não provida"

                l += f"\n↳{i[:-3]}: {name}"
    return l


def getEquipeEventosCommands(opt: str):
    l = ""
    for i in os.listdir("commands/EquipeEventos"):
        if "**Gremorys**" not in l:
            l += "\n\n**Gremorys**"
        if not i.startswith("__"):
            if i not in l:
                try:
                    name = getattr(helps, f'{i[:-3]}_{opt}')()
                except:
                    name = "Descrição não provida"

                l += f"\n↳{i[:-3]}: {name}"
    return l


def getPulicCommands(opt: str):
    l = ""
    for i in os.listdir("commands/Publicos"):
        if "**Publicos**" not in l:
            l += "\n\n**Publicos**"
        if not i.startswith("__"):
            if i not in l:
                try:
                    name = getattr(helps, f'{i[:-3]}_{opt}')()
                except:
                    name = "Descrição não provida"

                l += f"\n↳{i[:-3]}: {name}"
    return l


def getCapsCommands(opt: str):
    l = ""
    for i in os.listdir("commands/Caps"):
        if "**Capitães**" not in l:
            l += "\n\n**Capitães**"
        if not i.startswith("__"):
            if i not in l:
                try:
                    name = getattr(helps, f'{i[:-3]}_{opt}')()
                except:
                    name = "Descrição não provida"

                l += f"\n↳{i[:-3]}: {name}"
    return l


def getEligosCommands(opt: str):
    l = ""
    for i in os.listdir("commands/EquipeKaraoke"):
        if "**Eligos**" not in l:
            l += "\n\n**Eligos**"
        if not i.startswith("__"):
            if i not in l:
                try:
                    name = getattr(helps, f'{i[:-3]}_{opt}')()
                except:
                    name = "Descrição não provida"

                l += f"\n↳{i[:-3]}: {name}"
    return l


def getCallPvCommands(opt: str):
    l = ""
    for i in os.listdir("commands/Call Pv"):
        if "**Call Pv**" not in l:
            l += "\n\n**Call Pv**"
        if not i.startswith("__"):
            if i not in l:
                try:
                    name = getattr(helps, f'{i[:-3]}_{opt}')()
                except:
                    name = "Descrição não provida"

                l += f"\n↳{i[:-3]}: {name}"
    return l
