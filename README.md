# 🚗 GhostRadar-AI: Traffic Speed & License Plate Detection

Bu proje, **OpenCV**, **YOLOv8** ve **EasyOCR** teknolojilerini kullanarak video görüntüleri üzerinden gerçek zamanlı trafik analizi yapar. Araçları tespit eder, hızlarını hesaplar ve plakalarını okur. "Hayalet Mod (Ghost Mode)" sayesinde ekranda gereksiz çerçeveler (bounding box) oluşturmadan sadece verileri görselleştirir.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![YOLOv8](https://img.shields.io/badge/AI-YOLOv8-green)
![OpenCV](https://img.shields.io/badge/Vision-OpenCV-red)
![EasyOCR](https://img.shields.io/badge/OCR-EasyOCR-yellow)

## 🌟 Özellikler

* **Nesne Tespiti ve Takibi:** YOLOv8 (Nano) modeli ile araçları (Araba, Kamyon, Otobüs, Motosiklet) yüksek doğrulukla tespit eder ve takip eder.
* **Hız Hesaplama:** Piksel/Metre kalibrasyonu ve FPS tabanlı zaman ölçümü ile aracın tahmini hızını (km/h) hesaplar.
* **Plaka Okuma (LPR):** Haar Cascade ile plaka konumunu bulur, görüntü işleme ile netleştirir ve EasyOCR ile metne dönüştürür.
* **Hayalet Mod (Ghost UI):** Araçların etrafında kaba kutular çizmek yerine, sadece verileri (Hız ve Plaka) araç üzerinde süzülen bir yazı olarak gösterir.
* **Dinamik Kalibrasyon:** Video çözünürlüğüne ve kamera açısına göre ayarlanabilir mesafe parametreleri.

## 🛠️ Kurulum

Projeyi bilgisayarınıza klonlayın ve gerekli kütüphaneleri yükleyin.

1.  **Projeyi İndirin:**
    ```bash
    git clone [https://github.com/KULLANICI_ADIN/GhostRadar-AI.git](https://github.com/KULLANICI_ADIN/GhostRadar-AI.git)
    cd GhostRadar-AI
    ```

2.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install opencv-python ultralytics easyocr numpy
    ```
    *(Not: EasyOCR için PyTorch gereklidir, otomatik yüklenir.)*

3.  **Gerekli Dosyalar:**
    * `main.py`: Ana proje dosyası.
    * `haarcascade_russian_plate_number.xml`: Plaka tespiti için gerekli XML dosyası (Proje klasöründe olmalı).
    * `video.mp4`: Test edilecek video dosyası.

## 🚀 Kullanım

`main.py` dosyasını çalıştırın:

```bash
python main.py

