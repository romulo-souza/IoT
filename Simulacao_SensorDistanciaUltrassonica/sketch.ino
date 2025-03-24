#define PIN_TRIG 3
#define PIN_ECHO 2

void setup() {
  Serial.begin(115200);
  pinMode(PIN_TRIG, OUTPUT); //envia informação para o sensor para ele produzir a onda ultrassonica e realizar a mediçao 
  pinMode(PIN_ECHO, INPUT); //Recebe a medição da distancia (sera uma entrada no nosso sistema)
}

void loop() {
  digitalWrite(PIN_TRIG, HIGH); //inicia a transmissao do sinal do trigger
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);  //desliga o trigger para fazer a leitura do retorna da onda produzida pelo sinal do trigger, senao ele nao para de enviar sinal

  int distance = pulseIn(PIN_ECHO, HIGH); //, pulseIn() é usado para medir o tempo que o sinal ultrassônico levou para ir e voltar após refletir em um obstáculo.
  Serial.print("Distância em cm: ");
  Serial.println(distance/58); //segundo a documentaçao do sensor

  delay(5000);//delay de 5 segundos para fazer uma nova leitura
}
