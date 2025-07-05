from flask import Flask, request, jsonify
import serial
import threading
import struct
import time
import RPi.GPIO as GPIO  # GPIO kütüphanesini ekledik

# --- Flask Uygulamasını Başlatma ---
app = Flask(__name__)  # Yazım hatası düzeltildi: _name_ -> __name__

# --- YENİ EKLENEN KISIM: GPIO Ayarları ---
PIN_PULSE = 6  # 1 saniyelik sinyal için kullanılacak GPIO pini

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN_PULSE, GPIO.OUT)
GPIO.output(PIN_PULSE, GPIO.LOW) # Başlangıçta pinin kapalı olduğundan emin olalım

# --- UART Ayarları ---
try:
    # Raspberry Pi 3 ve sonrası için UART portu genellikle 'ttyS0' veya 'ttyAMA0' olur.
    # Hangisinin doğru olduğunu `ls -l /dev/` komutuyla kontrol edebilirsiniz.
    ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
    print("[UART] Bağlantı başarıyla açıldı: /dev/ttyAMA0")
except serial.SerialException as e:
    print(f"[UART HATASI] Port başlatılamadı: {e}")
    ser = None # Hata durumunda ser'i None olarak ayarlıyoruz

# --- Global Değişkenler ve Kontrol Mantığı ---
current_command = {"steer": 0, "speed": 0}
target_command = {"steer": 0, "speed": 0}
lock = threading.Lock() # Değişkenlere güvenli erişim için

# Hızlanma ve Yavaşlama Değerleri
acceleration = 25
deceleration = 100
stop_acceleration = 100 # Durma ivmesi (daha hızlı durması için)

last_command_time = time.time() # Son komutun zamanını tutar

# --- Yardımcı Fonksiyonlar (Mevcut kodunuzdan) ---
def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def move_towards(current, target, step):
    if current < target:
        return clamp(current + step, current, target)
    elif current > target:
        return clamp(current - step, target, current)
    return current

def calculate_step(current, target, interval):
    if target == 0 and current != 0:
        return stop_acceleration * interval
    elif abs(target) < abs(current): # Yavaşlama durumu
        return deceleration * interval
    return acceleration * interval # Hızlanma durumu

# --- YENİ EKLENEN KISIM: GPIO Pulse Fonksiyonu ---
def pulse_gpio_pin():
    """PIN_PULSE'u 1 saniye HIGH yapıp LOW yapar. Sunucuyu bloklamaz."""
    print(f"[GPIO] Pin {PIN_PULSE} -> HIGH (1 saniye)")
    GPIO.output(PIN_PULSE, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(PIN_PULSE, GPIO.LOW)
    print(f"[GPIO] Pin {PIN_PULSE} -> LOW")

# --- UART Veri Gönderim Döngüsü (Mevcut kodunuzdan) ---
def send_uart_loop():
    global current_command, target_command, last_command_time, ser
    interval = 0.1  # 100ms'de bir veri gönder

    if ser is None:
        print("[UART] Port başlatılamadığı için UART döngüsü çalışmıyor.")
        return

    while True:
        now = time.time()
        with lock:
            # Belirli bir süre komut gelmezse aracı durdur (güvenlik önlemi)
            if now - last_command_time > 0.5: # 0.5 saniye
                target_command["speed"] = 0
                target_command["steer"] = 0

            # Hız ve yönü hedefe doğru yumuşakça değiştir
            speed_step = calculate_step(current_command["speed"], target_command["speed"], interval)
            current_command["speed"] = move_towards(current_command["speed"], target_command["speed"], speed_step)
            current_command["steer"] = target_command["steer"] # Yönü anlık değiştiriyoruz

            steer = int(current_command["steer"])
            speed = int(current_command["speed"])

        try:
            # Veri paketini oluştur ve gönder
            frame = struct.pack('<HhhH', 0xABCD, steer, speed, (0xABCD ^ steer ^ speed) & 0xFFFF)
            if ser.is_open:
                ser.write(frame)
                # print(f"[UART] Gönderildi: steer={steer}, speed={speed}") # Hata ayıklama için
            else:
                print("[UART] Port kapalı, döngü sonlandırılıyor.")
                break
        except Exception as e:
            print(f"[UART HATASI] Yazma hatası: {e}")
            break
        time.sleep(interval)

# --- Flask API Endpoint (İki işlevi birleştiren kısım) ---
@app.route('/control', methods=['POST'])
def control():
    global target_command, last_command_time
    data = request.get_json()
    if not data or 'command' not in data:
        return jsonify({"status": "error", "message": "Geçersiz istek"}), 400

    cmd = data.get("command", "")
    print(f"[KOMUT] Alındı: {cmd}")

    # YENİ EKLENEN KISIM: pulse_gpio komutunu kontrol et
    if cmd == "pulse_gpio":
        # GPIO işlemini ayrı bir thread'de başlatarak ana sunucunun bloklanmasını engelle
        pulse_thread = threading.Thread(target=pulse_gpio_pin)
        pulse_thread.start()
        return jsonify({"status": "success", "message": "Pulse komutu alındı."})

    # Mevcut hareket komutlarınız
    with lock:
        last_command_time = time.time()
        if cmd == "forward":
            target_command["steer"] = 0
            target_command["speed"] = 100 # Hız değerini isteğinize göre ayarlayın
        elif cmd == "backward":
            target_command["steer"] = 0
            target_command["speed"] = -100
        elif cmd == "left":
            target_command["steer"] = -100
            target_command["speed"] = 80 # Dönerken ileri gitmesi için
        elif cmd == "right":
            target_command["steer"] = 100
            target_command["speed"] = 80 # Dönerken ileri gitmesi için
        elif cmd == "stop":
            target_command["steer"] = 0
            target_command["speed"] = 0
        else:
            return jsonify({"status": "warning", "message": f"Bilinmeyen komut: {cmd}"})

    return jsonify({"status": "command_received", "command": cmd})

# --- Ana Uygulama Başlatıcısı ---
if __name__ == '__main__': # Yazım hatası düzeltildi: _main_ -> __main__
    # UART döngüsünü arka planda çalışan bir thread olarak başlat
    uart_thread = threading.Thread(target=send_uart_loop, daemon=True)
    uart_thread.start()
    
    try:
        # Flask sunucusunu ağdaki tüm cihazların erişebilmesi için başlat
        app.run(host='0.0.0.0', port=5000)
    finally:
        # Programdan çıkarken (Ctrl+C) kaynakları temizle
        print("\nProgram sonlandırılıyor. Kaynaklar temizleniyor...")
        GPIO.cleanup()
        print("[GPIO] Pinler temizlendi.")
        if ser and ser.is_open:
            ser.close()
            print("[UART] Bağlantı kapatıldı.")
        print("Temizlik tamamlandı.")