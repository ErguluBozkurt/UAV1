import picamera
import time

def video_ceki(video_suresi):
    try:
        # Kamera nesnesini başlat
        with picamera.PiCamera() as camera:
            # Video çözünürlüğünü ayarla (isteğe bağlı)
            # camera.resolution = (width, height)
            
            # Video kaydının başlamasını bekle
            time.sleep(2)
            
            # Video çekimini başlat
            video_adı = 'kayit.mp4'
            camera.start_recording(video_adı)
            
            # Belirlenen süre kadar video çekimini devam ettir
            camera.wait_recording(video_suresi)
            
            # Video çekimini durdur
            camera.stop_recording()
            
            print(f"{video_suresi} saniyelik video başarıyla kaydedildi: {video_adı}")

    except Exception as e:
        print(f"Hata oluştu: {str(e)}")

# 5 saniyelik video çekimi için
video_ceki(5)
