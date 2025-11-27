import cv2
from ultralytics import YOLO
import easyocr
import numpy as np


MESAFE = 55    
CY1 = 600      
CY2 = 400      
OFFSET = 50     

print("RADAR STARTING...")
model = YOLO('yolov8n.pt') 

reader = easyocr.Reader(['en'], gpu=True) 
plate_cascade = cv2.CascadeClassifier('xml.xml')

cap = cv2.VideoCapture("video3.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0: fps = 30

arac_siniflari = [2, 3, 5, 7] 
arac_giris_frame = {} 
arac_hizlari = {}     
arac_plakalari = {} 

def plakayi_netlestir_ve_oku(arac_resmi):
    try:
        gray = cv2.cvtColor(arac_resmi, cv2.COLOR_BGR2GRAY)
        plates = plate_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(plates) > 0:
            for (px, py, pw, ph) in plates:
                plaka_resmi = gray[py:py+ph, px:px+pw]
                plaka_resmi = cv2.bilateralFilter(plaka_resmi, 11, 17, 17)
                _, plaka_resmi = cv2.threshold(plaka_resmi, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                
                result = reader.readtext(plaka_resmi)
                for (_, text, prob) in result:
                    if prob > 0.4 and len(text) > 4:
                        return text.upper(), (px, py, pw, ph)
        else:
            result = reader.readtext(gray)
            for (_, text, prob) in result:
                if prob > 0.4 and len(text) > 5:
                    return text.upper(), None
    except:
        return "", None
    return "", None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1280, 720))
    current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)

    results = model.track(frame, persist=True, verbose=False)
    
    if results[0].boxes is not None and results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.int().cpu().tolist()
        class_ids = results[0].boxes.cls.int().cpu().tolist()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        
        for box, class_id, track_id in zip(boxes, class_ids, track_ids):
            if class_id in arac_siniflari:
                x1, y1, x2, y2 = box
                cx = int((x1 + x2) / 2)
                cy = int(y2) 

                if (CY1 - OFFSET) < cy < (CY1 + OFFSET):
                    if track_id not in arac_giris_frame:
                        arac_giris_frame[track_id] = current_frame
                
                if (CY2 - OFFSET) < cy < (CY2 + OFFSET):
                    if track_id in arac_giris_frame:
                        gecen_frame = current_frame - arac_giris_frame[track_id]
                        if gecen_frame > 2:
                            sure = gecen_frame / fps
                            hiz = (MESAFE / sure) * 3.6 
                            
                            if 10 < hiz < 300:
                                arac_hizlari[track_id] = int(hiz)
                                
                                if track_id not in arac_plakalari:
                                    h, w, _ = frame.shape
                                    c_y1, c_y2 = max(0, y1), min(h, y2)
                                    c_x1, c_x2 = max(0, x1), min(w, x2)
                                    arac_resmi = frame[c_y1:c_y2, c_x1:c_x2]
                                    okunan, koord = plakayi_netlestir_ve_oku(arac_resmi)
                                    if okunan:
                                        arac_plakalari[track_id] = (okunan, koord)
                                    else:
                                        arac_plakalari[track_id] = ("...", None)
                        del arac_giris_frame[track_id]

            
                info_text = ""
                
               
                if track_id in arac_hizlari:
                    hiz_verisi = f"{arac_hizlari[track_id]} km/h"
                    info_text += hiz_verisi
                
                    
                    if track_id in arac_plakalari:
                        plaka_metni, plaka_koord = arac_plakalari[track_id]
                        if plaka_metni != "...":
                            info_text += f" | {plaka_metni}"
                            
                            
                            if plaka_koord is not None:
                                px, py, pw, ph = plaka_koord
                                cv2.rectangle(frame, (x1 + px, y1 + py), (x1 + px + pw, y1 + py + ph), (255, 100, 0), 1)

                    
                    (tw, th), _ = cv2.getTextSize(info_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
                    
                    
                    text_x = x1
                    text_y = y1 - 10
                    
                    cv2.rectangle(frame, (text_x, text_y - 30), (text_x + tw, text_y), (0, 0, 0), -1)
                    cv2.putText(frame, info_text, (text_x, text_y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("EDS-SYS", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()