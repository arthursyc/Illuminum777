# libraries 
import json
import requests
from asyncio import TimeoutError

from discord.ext import commands
from discord import *


headers = {'User-Agent': '(https://meta.wikimedia.org/wiki/User:Alpha1C)'}

class Web_Scraping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx, *, text):
        print(f"\nSearching Wikipedia for {text}\n")
        response = requests.get("https://en.wikipedia.org/w/rest.php/v1/search/page", headers=headers, params={'q': text, 'limit': 10})
        if response.status_code != 200:
            print("\nSearch unsuccessful\n")
            await ctx.send(embed=Embed(title="Fetch unsuccessful"))
            return
        response = json.loads(response.text)
        index = 0
        while index < len(response['pages']):
            if response['pages'][index]['description'] == 'Topics referred to by the same term':
                del response['pages'][index]
            else:
                index += 1
        index = 0

        infomsg = await ctx.send(embed=Embed(title="Fetching..."))

        while True:   
            search_result = response['pages'][index]
            exc = ''
            inBracket = False
            for i in search_result['excerpt']:
                if (i == '<' and not inBracket) or (i == '>' and inBracket):
                    inBracket = not inBracket
                if not inBracket and i != '>':
                    exc = exc + i
            exc = exc.replace('&quot;', '\"') + '...'


            wikiemb = Embed(
                title = search_result['title'],
                url = 'https://en.wikipedia.org/wiki/' + search_result['key'],
                description = search_result['description']
            )
            if search_result['thumbnail'] != None:
                wikiemb.set_thumbnail(url = 'https:' + search_result['thumbnail']['url'])
            wikiemb.add_field(name='Excerpt', value=exc, inline=False)

            value = ""
            for item in response['pages']:
                value += f"{item['title']}᲼᲼"
            wikiemb.add_field(name="All Results:", value=value, inline=False)

            await infomsg.edit(embed=wikiemb)
            await infomsg.add_reaction("\U000023EE")
            await infomsg.add_reaction("\U000023ED")


            def check(reaction, user):
                return reaction.emoji in ["\U000023EE", "\U000023ED"] and user != infomsg.author and reaction.message == infomsg
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=6000.0, check=check)
            except TimeoutError:
                await infomsg.clear_reactions()
                break

            match reaction.emoji:
                case "\U000023EE":
                    index = (index - 1) % len(response['pages'])
                case "\U000023ED":
                    index = (index + 1) % len(response['pages'])
            await infomsg.clear_reactions()


def setup(client):
    client.add_cog(Web_Scraping(client))