import os
from dotenv import load_dotenv
from discord.ext import commands
from

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix='!')

runes = open('runes.txt', 'r')
runewords = open('runewords.txt', 'r')
mercs = open('mercs.txt', 'r')
separator = '---'
sub_separator = '***'
rwd_parse = [elem.strip('\n') for elem in runewords.read().split(separator)]
rune_list = [elem.strip('\n') for elem in runes.read().split(separator)]
runewords_list = rwd_parse[:-1]
mercs_list = [elem.strip('\n') for elem in mercs.read().split(separator)]
starter_builds = rwd_parse[-1]


def _discord_text_format(elem):
    elem = elem.split('\n')
    elem[0] = "**" + elem[0].replace('(', '```').replace(')', '```') + "**"
    elem[elem.index(sub_separator) - 1] = '*' + elem[elem.index(sub_separator) - 1] + '*'
    return '\n'.join(elem)


def d2_rune(inp, key='-d'):
    inp = inp.lower().capitalize().replace('#', '')
    if inp == 'All':
        return '```' + ', '.join(['('+elem[:elem.index('#')+3].rstrip(' ')+')' for elem in rune_list]) + '```'
    elif inp.isdigit():
        try:
            return _discord_text_format(rune_list[int(inp) - 1]).split(sub_separator)[0]
        except:
            return f'Number: "{inp}" of rune not found. Must be between **1-33**'
    else:
        for elem in rune_list:
            if elem.startswith(inp) and key == '-d':
                return _discord_text_format(elem).split(sub_separator)[0]
            elif elem.startswith(inp) and key == '-r':
                return '**' + elem[:elem.index('\n')].replace('(', '```').replace(')', '```') \
                       + '**' + elem.split(sub_separator)[1]
        return f'Rune "{inp}" not found. Try **!d2r all** to see all runes'


def d2_runewords(inp, key='-d'):
    inp = inp.lower().split(' ')
    inp = ' '.join([elem if elem == 'of' or elem == 'the' or elem == 'to' else elem.capitalize() for elem in inp])
    if inp == 'All':
        return "```" + ', '.join([elem[:elem.index('\n')] for elem in runewords_list]) + "```"
    else:
        for elem in runewords_list:
            if elem.startswith(inp) and key == '-d':
                sub_elem = elem.split('\n')
                sub_elem[0] = '**' + sub_elem[0]
                sub_elem[1] = '```'
                sub_elem[sub_elem.index('Stats:') - 1] = '```' + '**'
                return '\n'.join(sub_elem)
    return f'Runeword "{inp}" not found. Try **!d2w all** to see all runewords'


def d2_mercenaries(inp):
    inp = ''.join(c for c in inp if c.isdigit())
    try:
        return mercs_list[int(inp)-1]
    except:
        return f'Number: "{inp}" of Act not found. Must be between **1-5**'


@bot.command(name='d2w', aliases=['runewords', 'runeword', 'рунворд'],
             brief='Diablo 2 Runeword Helper\n    Example: !d2w call to arms',
             description='Diablo 2 Runeword Helper')
async def d2w(ctx, *, arg):
    key = '-d'
    if arg.endswith('-r'):
        key = '-r'
        arg = arg.split(' ')[0]
    await ctx.send(f'{ctx.author.mention}, your info about runeword: \n{d2_runewords(arg, key)}')


@bot.command(name='d2r', aliases=['rune', 'runes', 'руна'],
             brief='Diablo 2 Rune Helper\n    Example: !d2r sol',
             description='Diablo 2 Rune Helper')
async def d2r(ctx, arg1, arg2='-d'):
    await ctx.send(f'{ctx.author.mention}, your info about rune(s): \n{d2_rune(arg1, arg2)}')


@bot.command(name='d2m', aliases=['merc', 'mercs', 'mercenaries', 'мерк', 'наемник', 'наёмник'],
             brief='Diablo 2 Mercenaries info\n    Example: !d2m act2',
             description='Diablo 2 Mercenaries info')
async def d2m(ctx, *, arg):
    await ctx.send(f'{ctx.author.mention}, your info about d2 mercenaries: \n{d2_mercenaries(arg)}')


@bot.command(name='d2s', aliases=['starter', 'd2start', 'd2starter'],
             brief='Diablo 2 Starter builds\n    Example: !d2s',
             description='Diablo 2 Starter builds')
async def d2s(ctx):
    await ctx.send(f'{ctx.author.mention}. Message sent to you as "private"')
    await ctx.author.send(f'{ctx.author.mention}, your info about starter builds: \n{starter_builds}')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Make sure you put the required arguments / Не указан аргумент')


@bot.event
async def on_ready():
    print('PepegaBot has successfully connected')


bot.run(TOKEN)