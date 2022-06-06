import json
import requests
from discord.ext import commands
from discord import *


headers = {'User-Agent': '(https://meta.wikimedia.org/wiki/User:Alpha1C)'}


class Web_Scraping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx, *, text):
        print(f"\nSearching Wikipedia for {text}\n")
        response = requests.get("https://en.wikipedia.org/w/rest.php/v1/search/page", headers=headers, params={'q': text, 'limit': 2})
        response = json.loads(response.text)
        if response['pages'][0]['description'] != 'Topics referred to by the same term':
            search_result = response['pages'][0]
        else:
            search_result = response['pages'][1]

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
        wikiemb.add_field(name='Excerpt', value=exc)

        await ctx.send(embed=wikiemb)


def setup(client):
    client.add_cog(Web_Scraping(client))