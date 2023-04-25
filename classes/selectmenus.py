import discord

optionsvar = [
    {
        "emoji": ":BAN:903237786465894430",
        "label": 'Flood/spam.',
        "value": '1',
    },
    {
        "emoji": ":BAN:903237786465894430",
        "label": 'Divulgação inadequada.',
        "value": '2',
    },
    {
        "emoji": ":BAN:903237786465894430",
        "label": 'Off topic/mensagem fora de tópico.',
        "value": '3',
    },
    {
        "emoji": ":BAN:903237786465894430",
        "label": 'Menção desnecessária de membros e cargos.',
        "value": '4',
    },
    {
        "emoji": ":BAN:903237786465894430",
        "label": 'Provocação e brigas.',
        "value": '5',
    },
    {
        "emoji": ":BAN:903237786465894430",
        "label": 'Poluição sonora.',
        "value": '6',
    },
    {
        "emoji": ":BAN:903237786465894430",
        "label": 'Atrapalhar o andamento do Karaokê.',
        "value": '7',
    },
    {
        "emoji": ":BAN:903237786465894430",
        "label": 'Denúncias falsas.',
        "value": '8',
    },
    {
        "emoji": ":BAN:903237786465894430",
        "label": 'Linguagem discriminatória.',
        "value": '9',
    },
    {
        "emoji": ":BAN:903237786465894430",
        "label": 'Exposição de membros/ Assédio.',
        "value": '10',
    },
    {
        "emoji": ":BAN:903237786465894430",
        "label": 'Preconceito, discriminação, difamação e/ou desrespeito.',
        "value": '11',
    },
    {
        "emoji": ":BAN:903237786465894430",
        "label": 'Planejar ou exercer raids no servidor.',
        "value": '12',
    },
    {
        "emoji": ":BAN:903237786465894430",
        "label": 'NSFW/ (+18).',
        "value": '13',
    },
    {
        "emoji": ":BAN:903237786465894430",
        "label": 'Estimular ou praticar atividades ilegais ou que cause banimento de membros.',
        "value": '14',
    },
    {
        "emoji": ":BAN:903237786465894430",
        "label": 'Evasão de punição.',
        "value": '15',
    },
    {
        "emoji": ":BAN:903237786465894430",
        "label": 'Conteúdos graficamente chocantes.',
        "value": '16',
    },
    {
        "emoji": ":BAN:903237786465894430",
        "label": 'Quebra do ToS do Discord.',
        "value": '17',
    },
    {
        "emoji": ":BAN:903237786465894430",
        "label": 'Selfbot.',
        "value": '18',
    },
    {
        "emoji": ":BAN:903237786465894430",
        "label": 'Scam.',
        "value": '19',
    },

]

cargos1 = [
    {
        "label": "Eligos",
        "value": "eligos",
    },
    {
        "label": "Vagantes",
        "value": "vagantes"
    },
    {
        "label": "Naberios",
        "value": "naberios"
    },
    {
        "label": "Gremorys",
        "value": "gremorys"
    }
]

cargos2 = {
    "eligos": [
        {
            "label": "Capitão Eligo",
            "value": "cap karaoke"
        },
        {
            "label": "Eligo",
            "value": "karaoke",
        }
    ],
    "vagantes": [
        {
            "label": "Capitão Ose",
            "value": "cap poem",
        },
        {
            "label": "Vagante",
            "value": "poem"
        }

    ],
    "naberios": [
        {
            "label": "Capitão Naberios",
            "value": "cap arte",
        },
        {
            "label": "Naberio",
            "value": "arte"
        },
    ],
    "gremorys": [
        {
            "label": "Capitão Gremory",
            "value": "cap evento",
        },
        {
            "label": "Gremory",
            "value": "evento"
        },
    ]
}


class staffSelectNotify(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=500)

        options = []

        for i in optionsvar:
            options.append(
                discord.SelectOption(
                    label=i["label"],
                    value=i["value"],
                    emoji=i["emoji"]
                )
            )

        self.add_item(
            discord.ui.Select(
                placeholder="Selecione a infração",
                options=options,
                max_values=1,
                min_values=1,
                custom_id="MotivosNotify"
            )
        )

class staffSelectAdv(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=500)

        options = []

        for i in optionsvar:
            options.append(
                discord.SelectOption(
                    label=i["label"],
                    value=i["value"],
                    emoji=i["emoji"]
                )
            )

        self.add_item(
            discord.ui.Select(
                placeholder="Selecione a infração",
                options=options,
                max_values=1,
                min_values=1,
                custom_id="Motivos"
            )
        )


class iniciarCargos(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=500)

        self.add_item(
            discord.ui.Select(
                placeholder="Selecione oq fazer",
                options=[
                    discord.SelectOption(
                        label="Adicionar",
                        value="adc"
                    ),
                    discord.SelectOption(
                        label="Remover",
                        value="rmv"
                    )
                ],
                max_values=1,
                min_values=1,
                custom_id="selectIniciar"
            )
        )


class menusCargos(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=500)

        options = []

        for i in cargos1:
            options.append(
                discord.SelectOption(
                    label=i["label"],
                    value=i["value"],
                )
            )

        self.add_item(
            discord.ui.Select(
                placeholder="Selecione a equipe",
                options=options,
                max_values=1,
                min_values=1,
                custom_id="selectCargos"
            )
        )


class menusCargos2(discord.ui.View):

    def __init__(self, value: str):
        super().__init__(timeout=500)

        options = []

        for i in cargos2[value]:
            options.append(
                discord.SelectOption(
                    label=i["label"],
                    value=i["value"],
                )
            )

        self.add_item(
            discord.ui.Select(
                placeholder="Selecione o cargo",
                options=options,
                max_values=1,
                min_values=1,
                custom_id="selectCargos2"
            )
        )


class createSelect(discord.ui.View):

    def __init__(self, **kwargs):

        super().__init__()

        options = []

        for i in range(0, kwargs.get("qnt")):

            if f"c{i}-" in kwargs.get('idcategorias')[i]:

                options.append(
                    discord.SelectOption(
                        label=f"{kwargs.get('name_list')[i]}",
                        value=f"{kwargs.get('idcategorias')[i]}",
                    )
                )

            else:

                options.append(
                    discord.SelectOption(
                        label=f"{kwargs.get('name_list')[i]}",
                        value=f"c{i}-{kwargs.get('idcategorias')[i]}",
                    )
                )

        self.add_item(discord.ui.Select(
            placeholder="Abrir Ticket",
            options=options,
            custom_id="ticket_select",
            max_values=1,
            min_values=1,

        ))
