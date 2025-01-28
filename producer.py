import pika
import json
import time

credentials = pika.PlainCredentials('admin', 'senhasegura')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='62.72.9.213',  # IP público da VPS
        port=5672,
        credentials=credentials
    )
)

channel = connection.channel()

# Cria a fila 'automation'
channel.queue_declare(queue='automation')

def send_command(command):
    channel.basic_publish(
        exchange='',
        routing_key='automation',
        body=json.dumps({'command': command}),
        properties=pika.BasicProperties(
            delivery_mode=2  # Torna a mensagem persistente
        )
    )
    print(f" [x] Comando enviado: {command}")

# Exemplo de envio
if __name__ == "__main__":
    while True:
        cmd = input("Digite o comando (ou 'exit' para sair): ")
        if cmd.lower() == 'exit':
            break
        send_command(cmd)
    
    connection.close()