import os


async def verify_pastas():
    try:
        os.listdir("tickets")
    except:
        try:
            os.mkdir("tickets")
        except:
            pass
        try:
            os.mkdir("tickets/chat")
        except:
            pass
        try:
            os.mkdir("tickets/call")
        except:
            pass
        try:
            os.mkdir("tickets/privado")
        except:
            pass
        try:
            os.mkdir("tickets/outros")
        except:
            pass
