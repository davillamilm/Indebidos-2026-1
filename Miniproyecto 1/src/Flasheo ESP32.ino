#include <TensorFlowLite_ESP32.h>
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "arduinoFFT.h"
#include "open.h" 

const int MIC_PIN = 1;
const int LED_PIN = 48; 
const int SAMPLE_RATE = 16000; 
const float UMBRAL_CONFIANZA = 0.95; 

const uint16_t FFT_SAMPLES = 512; 
float vReal[FFT_SAMPLES];
float vImag[FFT_SAMPLES];
ArduinoFFT<float> FFT = ArduinoFFT<float>(vReal, vImag, FFT_SAMPLES, SAMPLE_RATE);

float audio_buffer[SAMPLE_RATE];

tflite::ErrorReporter* error_reporter = nullptr;
const tflite::Model* model = nullptr;
tflite::MicroInterpreter* interpreter = nullptr;
TfLiteTensor* input = nullptr;
TfLiteTensor* output = nullptr;

constexpr int kTensorArenaSize = 500 * 1024; 
uint8_t* tensor_arena = nullptr;

void setup() {
  Serial.begin(115200);
  delay(3000); 

  Serial.println("\n--- INICIANDO SISTEMA TINYML ---");

  tensor_arena = (uint8_t*) ps_malloc(kTensorArenaSize);
  if (tensor_arena == nullptr) {
    Serial.println("ERROR: No se pudo reservar memoria en PSRAM.");
    Serial.println("Verifica que la PSRAM esté habilitada en Arduino IDE:");
    Serial.println("  Tools > PSRAM > 'OPI PSRAM'");
    while (true);
  }
  Serial.println("Tensor arena en PSRAM: OK");


  pinMode(MIC_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW); 

  Serial.println("[1/5] Configurando reporte de errores...");
  static tflite::MicroErrorReporter micro_error_reporter;
  error_reporter = &micro_error_reporter;

  Serial.println("[2/5] Cargando modelo de IA...");
  model = tflite::GetModel(modelo_abrir); 
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    TF_LITE_REPORT_ERROR(error_reporter, "ERROR: La versión del modelo no coincide");
    return;
  }

  Serial.println("[3/5] Cargando operaciones matemáticas...");
  static tflite::AllOpsResolver resolver;

  Serial.println("[4/5] Configurando el intérprete...");
  static tflite::MicroInterpreter static_interpreter(
      model, resolver, tensor_arena, kTensorArenaSize, error_reporter);
  interpreter = &static_interpreter;

  Serial.println("[5/5] Asignando memoria a los tensores (Esto puede tardar)...");
  TfLiteStatus allocate_status = interpreter->AllocateTensors();
  if (allocate_status != kTfLiteOk) {
    Serial.println("ERROR CRÍTICO: No se pudo asignar memoria. Reduce kTensorArenaSize.");
    while(true); 
  }
  
  input = interpreter->input(0);
  output = interpreter->output(0);
  
  Serial.println("\n--- DIAGNÓSTICO DEL MODELO ---");
  
  Serial.print("Tipo de dato esperado (Type): ");
  Serial.println(input->type); 
  Serial.print("Bytes totales reservados para la entrada: ");
  Serial.println(input->bytes);
  
  Serial.print("Forma del tensor (Dimensiones): [ ");
  for (int d = 0; d < input->dims->size; d++) {
    Serial.print(input->dims->data[d]);
    Serial.print(" ");
  }
  Serial.println("]");
  Serial.println("------------------------------\n");

  Serial.println("\n>>> SISTEMA LISTO. ESPERANDO VOZ <<<\n");
}

void loop() {
  Serial.println("\n------------------------------------------------");
  Serial.println("Escribe la palabra 'capturar' y presiona Enter...");
  
  bool esperando = true;
  while (esperando) {
    if (Serial.available() > 0) {
      String comando = Serial.readStringUntil('\n');
      comando.trim(); 
      
      if (comando.equalsIgnoreCase("capturar")) {
        esperando = false; 
      }
    }
    delay(50); 
  }

  Serial.println("\n>>> ¡HABLA AHORA! (Grabando 1 segundo) <<<");
  
  for (int i = 0; i < SAMPLE_RATE; i++) {
    unsigned long start_time = micros();
    
    int raw_value = analogRead(MIC_PIN);
    audio_buffer[i] = (raw_value / 2047.5) - 1.0; 

    while ((micros() - start_time) < (1000000 / SAMPLE_RATE)) {}
  }

  Serial.println("--- Audio capturado. Aplicando Transformada de Fourier (FFT)... ---");

  int step_size = (SAMPLE_RATE - FFT_SAMPLES) / 63; 

  for (int fila = 0; fila < 64; fila++) {
    int start_index = fila * step_size;
    
    for (int i = 0; i < FFT_SAMPLES; i++) {
      vReal[i] = audio_buffer[start_index + i];
      vImag[i] = 0.0; 
    }

    FFT.windowing(FFTWindow::Hamming, FFTDirection::Forward);
    FFT.compute(FFTDirection::Forward);
    FFT.complexToMagnitude(); 

    for (int columna = 0; columna < 64; columna++) {
      float magnitud = vReal[columna + 1]; 
      input->data.f[(fila * 64) + columna] = magnitud; 
    }
  }

  Serial.println("--- Audio capturado. Pensando... ---");

  TfLiteStatus invoke_status = interpreter->Invoke();
  if (invoke_status != kTfLiteOk) {
    Serial.println("ERROR: Falló la IA");
    return;
  }

  float probabilidad_abrir = output->data.f[0]; 
  Serial.print("Confianza 'Abrir': "); 
  Serial.print(probabilidad_abrir * 100); 
  Serial.println("%");

  if (probabilidad_abrir > UMBRAL_CONFIANZA) {
    Serial.println(">>> RESULTADO: SIGA <<<");
    digitalWrite(LED_PIN, HIGH);
    delay(2000);                 
    digitalWrite(LED_PIN, LOW);  
  } else {
    Serial.println(">>> RESULTADO: DENEGADO <<<");
  }
}
