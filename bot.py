import openai
import discord
import requests
import json
import os
import datetime

from bs4 import BeautifulSoup

openai.api_key = ""
discord_token = "MTA5NTg0MDYxNjY2OTI0OTU0Nw.G7JmJg.tOMAxhf5J9MzitdNKEy88TYucEVRIv0iD1fbHc"

bot_website = "https://botchatgpt.netlify.app"

ajudas = [
    '`!gpt` - Faça uma pergunta :)',
    '`!receita` - Gera uma receita aleatória.',
    '`!musica` - Gera uma música aleatória.',
    '`!motive` - Te motiva a programar.',
    '`!net` - Faz um resumo de um link da web.',
    '`!para` - Enviar uma mensagem para algum chat do servidor.',
    '`!user` - Enviar uma mensagem para o usuário mencionado.',
    '`!show` - Mostra uma imagem que você pediu.',
    '`!infos` - Mostra informações sobre o bot.',
    '`!corrija` - Se você estiver com preguiça de escrever certo, use esse comando.',
    '`!pesquise` - Em Breve',
    '______________________________________________\n',
    '`!donate` - Nos ajude a manter o bot ativo.',
]
adms = [
    'erickgamer56',
]

config_file = "servers-configs.json"

if not os.path.exists(config_file):
    with open(config_file, "w") as file:
        json.dump({}, file)

#criar arquivo key
if not os.path.exists("key.txt"):
    with open("key.txt", "w") as arquivo:
        arquivo.write("Conteúdo inicial do arquivo key")

#captura o arquivo key
with open("key.txt", "r") as arquivo:
        key = arquivo.readline().strip()
        openai.api_key = key




model = 'text-davinci-003'
client = discord.Client(intents=discord.Intents.all())
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    print(f'O bot está em {len(client.guilds)} servidores')
    print('Já Estou Rodando !')

def gpt(text):
    try:
        completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=text,
            max_tokens=2000,
            temperature=0.5
        )
        return completion.choices[0].text
    except Exception as e:
        return "Desculpe, minha chave acabou e não posso executar comandos. 😔💔 No entanto, se quiser ajudar, sugiro que utilize o comando ´!donate´ para fazer uma doação ou explore outras formas de contribuir. 🙏💙"

def search_image(query):
    # substitua <sua chave de API> pela chave de API válida do Pexels
    url = f"https://api.pexels.com/v1/search?query={query}"
    headers = {"Authorization": "BfElPJeiWPRqdjASfp3fMS1aM8AYpW3BxNQGKnmKBVxYY9o1MeTbNQEs"}
    response = requests.get(url, headers=headers)
    data = response.json()
    if data["total_results"] == 0:
        return 'nada encontrado';
    else:
        image_urls = []
        for photo in data["photos"][:1]:
            image_urls.append(photo["src"]["original"])
        return image_urls
    
@client.event
async def on_guild_join(guild):
    invite_link = await guild.text_channels[0].create_invite(max_age=0)
    for adm in adms:
        user = await get_user_by_username(adm)
        if user:
            await user.send(f'O bot foi adicionado a um novo servidor: {guild.name} (Link de Convite: {invite_link})')

    try:
        with open('servers-configs.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"servers-list": [{"servers": []}]}

    new_server = {
        "id": guild.id,
        "nome": guild.name,
        "date": datetime.date.today().isoformat(),
        "adm-active": False
    }

    if "servers-list" not in data:
        data["servers-list"] = [{"servers": []}]

    if "servers" not in data["servers-list"][0]:
        data["servers-list"][0]["servers"] = []

    data["servers-list"][0]["servers"].append(new_server)

    with open('servers-configs.json', 'w') as file:
        json.dump(data, file, indent=4)




async def get_user_by_username(username):
    for user in client.users:
        if user.name == username:
            return user
    return None

async def obter_canal_por_mencao(mencao, servidor):
    nome_do_canal = mencao[1:]

    for canal in servidor.channels:
        if canal.name == nome_do_canal:
            return canal
    return None
@client.event


async def on_message(message):

    if message.author == client.user:
        return
    
    if isinstance(message.channel, discord.DMChannel):
        message_content = message.content
        if message_content.startswith('!'):
            await message.channel.send("...")
        else:
            await message.channel.send(gpt(message_content))
    if message.content.startswith('!gpt'):
        text = message.content[len('!gpt '):]
        print(message.author.name+ " usou o comando !gpt "+ text+' No servidor: '+ message.guild.name)
        if text != "":
             await message.channel.send(message.author.mention+'\n'+'```Resposta Para: '+ text +' ⬇️ ⬇️  ```'+"```"+gpt(text)+"```")
        else:
            await message.channel.send('Faça uma pergunta maluko !')

    if message.content.startswith('!ajuda'):
        comandos = '\n'.join(ajudas)  # Junta os elementos da array em uma única string, separados por quebra de linha

        embed = discord.Embed(title="Comandos disponíveis", description=comandos, color=discord.Color.blue())
        embed.set_author(name=message.author.name, icon_url=message.author.avatar.url)

        await message.channel.send(embed=embed)

    if message.content.startswith('!receita'):
        await message.channel.send(message.author.mention+'\n'+'```'+gpt('Quero uma receita de qualquer comida')+'```')
    if message.content.startswith('!motive'):
        await message.channel.send(message.author.mention+'\n'+'```'+gpt('Quero que voce me motive a programar ! gerando um messagem motivadora e com emojis')+'```')
    if message.content.startswith('!musica'):
        await message.channel.send(message.author.mention+'\n'+'```'+gpt('Diga uma musica aleatoria de muito sucesso responda com emoji')+'```')
    if message.content.startswith('!para'):
       text = message.content[len('!para '):]
       if message.author.guild_permissions.administrator:
        if text != '':
         if '#' in text:
             canal = ""
             split = text.split()
             for word in split:
                 if '#' in word:
                     canal = word
                     break
             text = text.replace(canal, " ")
             canal_destino = discord.utils.get(message.guild.channels, mention=canal)
             if canal_destino is None:
              await message.channel.send(canal+' Não foi encontrado !')
              return
             else:
              await message.channel.send('Enviado !')
              await canal_destino.send("De "+message.author.mention+'\n'+"```"+gpt(text)+"```")

         else:
             await message.channel.send('Especifique o canal de texto !')
        else:
            await message.channel.send('Vc não é admiro !')
    if message.content.startswith('!user'):
        if message.author.guild_permissions.administrator:
            text = message.content[len('!user '):]
            if text != '':
                if '@' in text:
                   userto = ""
                   split = text.split()
                   for word in split:
                       if '@' in word:
                           userto = word
                           break
                   member = discord.utils.get(message.guild.members, mention=userto)
                   text = text.replace(userto, " ")
                   if member is not None:
                       # Envia a mensagem direta para o usuário
                       await member.send("```De "+message.author.name+" do servidor "+message.guild.name+" ⬇️ ⬇️\n ```"+"```"+gpt(text)+"```")
                       await message.channel.send("Mensagem enviada para " + userto + "!")
                   else:
                       await message.channel.send("Usuário não encontrado.")
                else:
                    await message.channel.send("Por favor, mencione um usuário.")
        else:
            await message.channel.send("Vc não é admiro !")
    if message.content.startswith('!show'):
        text = message.content[len('!show '):]
        if text != "":
            text = gpt("traduza pra en eua:"+text)
            image_urls = search_image(text)
            await message.channel.send(image_urls[0])
            
        else:
            await message.channel.send("Prompt Não Aceito!")
    if message.content.startswith('!net'):
        url = message.content[len('!net '):]
        if 'https://' in url:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                title = soup.title.string.strip()
                description = soup.find("meta", attrs={"name": "description"})["content"]
                paragrafos = soup.find_all("p")
                conteudo = []
                for p in paragrafos:
                    conteudo.append(p.get_text())
                conteudo_str = '\n'.join(conteudo)
                resultgpt = gpt('Me explique oq vc entende colocando de forma organizadas as informaçoes disto:'+ title +" "+ description +" "+ conteudo_str+ "cite separadamente titulo, descrição, conteudo e dps faça um topico resumindo explique. de espaço em cada topico isso é importante")
                await message.channel.send(message.author.mention+'\n'+'```Resposta Para: '+ url +' ⬇️ ⬇️  ```'+"```"+resultgpt+"```")
            else:
                await message.channel.send("Não foi possível fazer a solicitação HTTP.")
        else:
            await message.channel.send("```Verifique se a url contem o: https://```")
    if message.content.startswith('!msg'):
        msg = message.content[len('!msg '):]
        qauth = message.author.name
        if qauth in adms:
            if msg != '':
                palavras_chave = ['bate-bapo', 'comunicado', 'avisos','geral'] 

                total_servidores = 0 

                for guild in client.guilds:
                    canal_encontrado = False

                    for palavra in palavras_chave:
                        canal = discord.utils.find(lambda c: palavra in c.name.lower(), guild.text_channels)

                        if canal is not None:
                            try:
                                await canal.send(msg)
                                print(f"Mensagem de anúncio enviada para o canal: {canal.name} no servidor: {guild.name}")
                                total_servidores += 1
                                canal_encontrado = True
                                break 

                            except discord.Forbidden:
                                print(f"O bot não tem permissão para enviar mensagens no canal: {canal.name} no servidor: {guild.name}")
                                continue 

                    if not canal_encontrado:
                        for canal in guild.text_channels:
                            try:
                                await canal.send(msg)
                                print(f"Mensagem de anúncio enviada para o canal: {canal.name} no servidor: {guild.name}")
                                total_servidores += 1
                                break  
                            except discord.Forbidden:
                                print(f"O bot não tem permissão para enviar mensagens no canal: {canal.name} no servidor: {guild.name}")
                                continue  
                await message.channel.send(f"Todas as mensagens foram enviadas para {total_servidores} servidores.")
            else:
                await message.channel.send('Coloque a mensagem!')
        else:
            await message.channel.send('Você não tem permissão para usar esse comando.')

    if message.content.startswith('!sair'):
        qauth = message.author.name
        if qauth in adms:
            await message.channel.send('Saindo!')
            await message.guild.leave()
        else:
            await message.channel.send('Você não tem permissão para usar esse comando.')
    if message.content.startswith('!infos'):
        info = {
            'name': client.user.name,
            'id': client.user.id,
            'discriminator': client.user.discriminator,
            'avatar': client.user.avatar,
            'created_at': client.user.created_at,
            'num_servidores': len(client.guilds),
            'website': bot_website,
        }
        embed = discord.Embed(
            title='Informações do Bot',
            description=f'Aqui estão as informações do bot {info["name"]}:',
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=info['avatar'])
        embed.add_field(name='Nome', value=info['name'], inline=True)
        embed.add_field(name='ID', value=info['id'], inline=True)
        embed.add_field(name='Discriminator', value=info['discriminator'], inline=True)
        embed.add_field(name='Criado em', value=info['created_at'].strftime('%d/%m/%Y'), inline=True)
        embed.add_field(name='Número de servidores', value=info['num_servidores'], inline=True)
        embed.add_field(name='Website', value=info['website'], inline=False)

        await message.channel.send(embed=embed)
    if message.content.startswith('!corrija'):
        text = message.content[len('!corrija '):]
        if text != '':
            await message.channel.send(gpt('corrija: '+ text+ ' mostre somente a conteudo corrijido'))
        else:
             await message.channel.send('Coloque seu texto apos o `!corrija` ')
    if message.content.startswith('!donate'):
        await message.channel.send('👋 Olá a todos! Infelizmente, tenho uma má notícia para vocês que usam o BotChatGPT. O bot utiliza uma chave da API da OpenAI para funcionar, e infelizmente ela não é permanente. 😔 Se você quiser ajudar e até mesmo melhorar a potência do bot, a chave Pix para doação é essa: 022629e5-fe57-492b-b613-60cd4c1a530d. Caso queira ajudar sem dinheiro, crie uma conta no site da OpenAI e mande a chave da API para mim, ErickGamer56#9383. 😊 É isso! Obrigado por entender. Caso isso não aconteça, o bot ficará fora do ar. ❌🤖')
    if message.content.startswith('!falar'):
        if message.author.voice:
            channel = message.author.voice.channel
            voice_client = await channel.connect()
        else:
            await message.channel.send('Você precisa estar em uma chamada de voz para usar esse comando!')
    if message.content.startswith('!addkey'):
        key = message.content[len('!addkey '):]
        qauth = message.author.name
        if qauth not in adms:
            await message.channel.send('Você não pode usar esse comando!')
            return
        with open("key.txt", "w") as arquivo:
            arquivo.truncate()

        # Escreve a chave API atualizada no arquivo "key.txt"
        with open("key.txt", "w") as arquivo:
            arquivo.write(key)

        # Atualiza a variável openai.api_key
        openai.api_key = key

        await message.channel.send('Chave API atualizada com sucesso!')


    # adms-servers-comandos



client.run(discord_token)