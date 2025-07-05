import socket
import serial
import time
import threading

# --- AYARLAR ---
SERIAL_PORT = '/dev/ttyUSB1'
BAUD_RATE = 9600
HOST_IP = '0.0.0.0'
PORT_NUMBER = 5500
# --- AYARLAR SONU ---

# handle_command fonksiyonu aynı kalabilir, sadece writer parametresini alacak
def handle_command(command_str, writer_stream):
    print(f"[KOMUT ALINDI] Android'den: {command_str}")
    if command_str.startswith("START_AUTONOMOUS:"):
        try:
            coords_str = command_str.split(":")[1]
            lat_str, lon_str = coords_str.split(",")
            target_lat = float(lat_str)
            target_lon = float(lon_str)
            print(f"  -> Otonom sürüş komutu. Hedef: Lat={target_lat}, Lon={target_lon}")
            print("  -> (Simülasyon: Otonom sürüş başlatıldı.)")

            response = "ACK:AUTONOMOUS_STARTED\n"
            writer_stream.write(response)
            writer_stream.flush()
            print(f"  -> Onay gönderildi: {response.strip()}")
        except Exception as e:
            print(f"  -> HATA: Komut işlenirken hata: {e}")
    else:
        print(f"  -> Bilinmeyen komut: {command_str}")


# --- YENİ FONKSİYON: Sadece Android'den komut dinlemek için ---
def listen_for_commands(client_socket, writer_stream, connection_active):
    """Bu thread, Android'den gelen komutları sürekli dinler."""
    try:
        reader_stream = client_socket.makefile('r', encoding='utf-8', newline='\n')
        while connection_active.is_set():
            # readline() burada bloklayacak, bir komut gelene kadar bekleyecek.
            # Bu artık bir sorun değil çünkü GPS gönderimi başka bir thread'de devam ediyor.
            command = reader_stream.readline()
            if not command: # İstemci bağlantıyı kapattıysa boş string döner
                print("[İLETİŞİM] Android komut kanalı kapandı (boş veri).")
                break
            handle_command(command.strip(), writer_stream)
    except (socket.error, BrokenPipeError, ConnectionResetError) as e:
        print(f"[İLETİŞİM] Android komut dinleme hatası (bağlantı koptu): {e}")
    finally:
        print("[THREAD] Komut dinleme thread'i sonlanıyor.")
        connection_active.clear() # Diğer thread'in de durmasını sağla


# --- YENİ FONKSİYON: Sadece Arduino'dan veri alıp Android'e göndermek için ---
def send_gps_data(writer_stream, arduino_serial, connection_active):
    """Bu thread, Arduino'dan veri okuyup Android'e gönderir."""
    try:
        while connection_active.is_set():
            if arduino_serial.in_waiting > 0:
                try:
                    line = arduino_serial.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        print(f"[GPS GÖNDERİLİYOR] -> {line}")
                        writer_stream.write(line + '\n')
                        writer_stream.flush()
                except serial.SerialException as se:
                    print(f"HATA: Arduino seri okuma hatası: {se}")
                    break # Arduino ile iletişim koparsa bu thread'i sonlandır
            time.sleep(0.1) # CPU'yu yormamak için kısa bir bekleme
    except (socket.error, BrokenPipeError) as e:
        print(f"[İLETİŞİM] Android'e GPS gönderme hatası (bağlantı koptu): {e}")
    finally:
        print("[THREAD] GPS gönderme thread'i sonlanıyor.")
        connection_active.clear() # Diğer thread'in de durmasını sağla


def start_server():
    try:
        arduino_serial = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Seri port ({SERIAL_PORT}) başarıyla açıldı.")
    except serial.SerialException as e:
        print(f"[KRİTİK HATA] Seri port açılamadı: {e}. Program sonlandırılıyor.")
        return

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST_IP, PORT_NUMBER))
    server_socket.listen(1)
    print(f"Sunucu {HOST_IP}:{PORT_NUMBER} adresinde başlatıldı, bağlantı bekleniyor...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"\n[BAĞLANTI] Android'den bağlantı kabul edildi: {client_address}")

            # --- ANA DÖNGÜ DEĞİŞİKLİĞİ ---
            # Her iki thread'in de çalışıp çalışmadığını kontrol etmek için bir "Event" nesnesi
            connection_active = threading.Event()
            connection_active.set() # Event'i "çalışıyor" durumuna getir

            # Android'e veri yazmak için tek bir stream oluşturalım
            writer_stream = client_socket.makefile('w', encoding='utf-8', newline='\n')

            # Thread'leri oluştur
            command_thread = threading.Thread(target=listen_for_commands, args=(client_socket, writer_stream, connection_active))
            gps_thread = threading.Thread(target=send_gps_data, args=(writer_stream, arduino_serial, connection_active))

            # Thread'leri başlat
            command_thread.start()
            gps_thread.start()

            # İki thread de bitene kadar burada bekle (yani bağlantı kopana kadar)
            command_thread.join()
            gps_thread.join()

            print(f"[BAĞLANTI KESİLDİ] {client_address}. Temizlik yapılıyor ve yeni bağlantı bekleniyor...")
            try:
                writer_stream.close()
                client_socket.close()
            except Exception as e:
                print(f"Soket kapatılırken hata oluştu: {e}")

    except KeyboardInterrupt:
        print("\nKullanıcı tarafından durduruluyor (Ctrl+C).")
    finally:
        print("Sunucu kapatılıyor...")
        server_socket.close()
        if arduino_serial.is_open:
            arduino_serial.close()
        print("Tüm kaynaklar serbest bırakıldı.")

if __name__ == '__main__':
    start_server()