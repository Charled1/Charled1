# Proje Manifestosu: Başyapıt v13.0 - Bir Otonom Ticaret Zekasının Doğuşu

**Yazar:** Masterpiece Bot Team  
**Versiyon:** 13.0 (Nihai Modüler Mimari)  
**Durum:** ✅ Tamamlandı ve Operasyonel

Bu repo, "Başyapıt" adını verdiğimiz otonom ticaret botunun evrimini özetler. Proje, basit bir script'ten kendi kendini optimize eden bir sisteme uzanan uzun bir yolculuğun sonucudur.

## 1. Projenin Amacı

Amacımız, değişen piyasa koşullarına uyum sağlayabilen, riskini profesyonelce yöneten ve öğrenerek gelişen bir ticaret platformu yaratmaktı. Statik kuralların sınırını aşan bu sistem, piyasayı süzerek fırsatları değerlendirir ve zamanla daha başarılı stratejiler üretir.

## 2. Evrim Süreci

Projeyi aşağıdaki beş büyük fazda inşa ettik:

### Faz 1: Tek Dosyalı "Altın Strateji"
Başlangıçta tüm mantık tek bir `main.py` içerisindeydi ve sabit parametrelerle çalışan bir strateji kullanıyorduk.

### Faz 2: `config.yaml` ve Backtest
Parametreleri koddan ayırarak esneklik kazandık ve basit bir backtester yazdık. Stratejilerimizi geçmiş veriler üzerinde deneyebildik.

### Faz 3: Pozisyon Yönetimi
`position_manager.py` ile kademeli kâr alma ve takip eden stop gibi profesyonel çıkış tekniklerini uyguladık. Kod karmaşıklığı artmaya başladı.

### Faz 4: Modüllerin Doğuşu
Projeyi `core/` ve `utils/` klasörlerine bölerek bakımı kolay, genişleyebilir bir mimari kurduk. `trading_ceo.py` sistemi orkestre ederken diğer modüller hesaplama, veri temizleme ve risk yönetimi gibi görevleri üstlendi.

### Faz 5: Öğrenme Organizasyonu
`strategy_optimizer.py` ve `learning_organization.py` modülleri, stratejileri otomatik olarak test edip iyileştiren bir mekanizma sağladı. Sistem yeni yaklaşımları haftalık toplantılarla deniyor ve sizin onayınızla güncelliyor.

## 3. En Başarılı Hibrit Strateji
Bu evrim sonucunda "Usta" (4 saatlik tarama) ve "Keskin Nişancı" (15 dakikalık retest) yaklaşımlarını birleştiren hibrit model en iyi performansı gösterdi.

## 4. Sistemi Tekrar Kurmak İçin Adımlar
Aşağıdaki yol haritası, Başyapıt'ı sıfırdan inşa etmek isteyenler için rehber niteliğindedir:

1. **Temel Strateji**: Basit bir `main.py` ile başlayın ve tek bir strateji çalıştırın.
2. **Yapılandırma**: Parametreleri `config.yaml`'a aktarın, backtester ile test edin.
3. **Pozisyon Yönetimi**: `position_manager.py` kullanarak kademeli kâr alma ve takip eden stop ekleyin.
4. **Modüller**: Kodu `core/` ve `utils/` klasörlerinde modüler hale getirin.
5. **Öğrenme Organizasyonu**: Stratejileri otomatik optimize eden `strategy_optimizer` ve `learning_organization` modüllerini devreye alın.

Bu README, projenin geçmişini ve tekrar nasıl inşa edilebileceğini özetlemektedir. Detaylı kod için modül dosyalarına göz atabilirsiniz.

## 5. Çalıştırma

1. `requirements.txt` dosyasındaki paketleri kurun:

   ```bash
   pip install -r requirements.txt
   ```

2. `config.yaml` dosyasını kendi bilgilerinizle doldurun. Örnek yapı:

   ```yaml
   telegram:
     token: "YOUR_TELEGRAM_TOKEN"
     chat_id: 123456789

   risk:
     account_balance: 10000
     risk_percent: 1.0
     max_daily_loss_percent: 5.0
   ```

3. Ardından uygulamayı başlatın:

   ```bash
   python main.py
   ```
