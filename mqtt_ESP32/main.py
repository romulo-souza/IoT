import network #simular um access point de wifi que permite que o microcontorlador se conecte a internet
import time #espera (tempo de delay)
from machine import Pin 
import dht
import ujson #unificar a msg em um objeto só (json)
from umqtt.simple import MQTTClient #cliente mqtt

#Parametros do Cliente MQTT
MQTT_Client_ID = "micropython-teste"
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_USER = "" #Sem user e password para deixar publico
MQTT_PASSWORD = ""
MQTT_TOPIC = "utfpr-dht"

#Config sensor e wifi
sensor = dht.DHT22(Pin(15))
print("Conectando ao WiFi", end="")
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect('Wokwi-GUEST', '') #rede padrão
while not wifi.isconnected():
    print(".", end="")
    time.sleep(0.1) #0.1s
print(" Connected")

#Realizar a conexao no server MQTT
print("Conectando ao Broker MQTT...", end="")
cliente = MQTTClient(MQTT_Client_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
cliente.connect()
print(" Conectado ao Broker")

#Leituras do dht e publicação das msg. Dados de leitura atuais, Dados da ultima leitura. Quando não houver alteração nos valores que foram lidos pelo DHT, nao ocorrerá transmissao de dados, a transmissao só é feita quando novos dados sao coletados pelo sensor
anterior = ""
while True:
    print("Medindo as condições do tempo...", end="")
    sensor.measure()
    #pegar os valores lidos e coloca-los em um JSON
    mensagem = ujson.dumps({
        "temperatura": sensor.temperature(),
        "umidade": sensor.humidity()
    })
    if mensagem != anterior:
        print("Atualizando...")
        print("Reportando alterações ao Topico MQTT {}: {}".format(MQTT_TOPIC, mensagem))
        #publicação da msg no broker
        cliente.publish(MQTT_TOPIC, mensagem)
        #como já foi feito uma alteração, agora anterior recebe a msg publicada
        anterior = mensagem
    else:
        print("Nenhuma mudança")

    #microcontrolador realizará uma nova leitura a cada 1s
    time.sleep(1)

#Endereço para acessar o broker publico (para realizar a conexão)
#https://www.hivemq.com/demos/websocket-client/
