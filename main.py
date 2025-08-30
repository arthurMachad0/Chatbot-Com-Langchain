# Carregamento
from langchain_community.document_loaders import WebBaseLoader as wbl
from langchain_community.document_loaders import YoutubeLoader as ytl
from langchain_community.document_loaders import PyPDFLoader as pdfl

# Interação com o sistema Operacinal
import os

# Criação e Configuração do ChatBot
from langchain.prompts import ChatPromptTemplate as Template
from langchain_groq import ChatGroq

API_KEY = os.getenv('GROQ_API_KEY')
chat = ChatGroq(model = 'llama-3.3-70b-versatile')

def resposta_bot(mensagens, documento):
    mensagem_sistema = '''Você é um assistente amigável chamado Eleia.
    Você utiliza as seguintes informações para formular as suas respostas: {informacoes}, utilizando sempre pensamento profundo.'''

    mensagens_modelo = [('system', mensagem_sistema)]
    mensagens_modelo += mensagens
    template = Template.from_messages(mensagens_modelo)
    chain = template | chat
    
    return chain.invoke({'informacoes': documento}).content 

def CarregaSite():
    url_site = input('Digite a URL do site')
    loader = wbl(url_site)
    lista_documentos = loader.load()
    
    documento = ''
    for doc in lista_documentos:
        documento += doc.page_content

    return documento

def CarregaPDF(): # Para pdfs extensos como livros, desenvolver método de consumo através de RAG ( Estudar técnicas de Retrieive Augmented Generation )
    caminho = 'seu-caminho-para-pdf/arquivo.pdf'
    loader = pdfl(caminho)

    lista_documentos = loader.load()

    documento = ''
    for doc in lista_documentos:
        documento += doc.page_content
    return documento

def CarregaYTB():
    url_video = input('Digite a URL do vídeo: ')
    loader = ytl.from_youtube_url(url_video, language =['pt'])
    lista_documentos = loader.load()

    documento = ''
    for doc in lista_documentos:
        documento += doc.page_content
    return documento

print('Bem vindo ao Eleia!\nQuando quiser sair do chat escreva: x\n')

texto_selecao = (
    "Digite 1 se você quiser conversar com um site\n"
    "Digite 2 se você quiser conversar com um PDF\n"
    "Digite 3 se você quiser conversar com um vídeo do YouTube\n")

while True:
  selecao = input(texto_selecao)
  if selecao == '1':
    documento = CarregaSite()
    break
  if selecao == '2':
    documento = CarregaPDF()
    break
  if selecao == '3':
    documento = CarregaYTB()
    break
  print('Digite um valor entre 1 e 3')


mensagens = []
while True:
    pergunta = input('Usuário: ')
    if pergunta.lower() == 'x':
        break
    print(f'Usuário: {pergunta}')
    mensagens.append(('user', pergunta))
    resposta = resposta_bot(mensagens, documento)
    mensagens.append(('assistant', resposta)) 
    print(f'Eleia: {resposta}\n')

print('\nMuito obrigado por utilizar o eleia para sanar suas dúvidas!\nVolte sempre que precisar!')
print(f'Histórico de Conversação: {mensagens}')
