# Kahve Dükkanı Konum Optimizasyonu

## Genel Bakış
Bu proje, Chicago'daki halk kütüphanelerinin konumlarını kullanarak kahve dükkanları için optimal konumları belirler.

## Özellikler
- Chicago açık veri portalından halk kütüphanesi verilerini çeker
- PuLP kullanarak optimizasyon modellemesi yapar
- Optimal kahve dükkanı konumlarının haritasını oluşturur

## Kurulum

1. Depoyu klonlayın
2. Sanal bir ortam oluşturun
3. Bağımlılıkları yükleyin:
   ```
   pip install -r requirements.txt
   ```

## Kullanım
Ana scripti çalıştırın:
```
python main.py
```

## Bağımlılıklar
- folium
- geopy
- pulp
- requests
