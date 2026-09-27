# Çoklu Hizmet Randevu Sistemi

Kuaför, berber, danışmanlık, pilates gibi randevuyla çalışan işletmeler için geliştirilmiş, çoklu hizmet ve uzman desteğine sahip bir online randevu platformu. Python/Flask tabanlı sunucu tarafı, Jinja2 şablon motoru ile render edilen sayfalar ve admin panelinde Chart.js ile görselleştirilen istatistikler içerir.

🔗 **Canlı Demo:** [randevu-sistemi-f456.onrender.com](https://randevu-sistemi-f456.onrender.com)
📸 **Ekran Görüntüleri:** <img width="1498" height="707" alt="image" src="https://github.com/user-attachments/assets/a25be946-cb8e-4b14-92e6-1d6daa5cd9cf" />
<img width="1156" height="682" alt="image" src="https://github.com/user-attachments/assets/a9a75c8a-42ce-4e31-b41c-08e5965f5f28" />



> ⏳ Not: Proje Render'ın ücretsiz planında barındırılıyor; bir süre trafik almazsa uyku moduna geçer ve ilk istek 30–60 saniye kadar gecikebilir. Bu normaldir.

---

## ✨ Özellikler

### Kullanıcılar için
- **Çoklu Hizmet Kataloğu** — Ana sayfada kart görünümünde listelenen hizmetler arasından seçim yapma.
- **Randevu Oluşturma** — Hizmete özel uzman listesi, uygun tarih (Pazar günleri hariç otomatik hesaplanan takvim) ve saat aralığı seçimi.
- **Randevu Sorgulama** — Üyelik gerektirmeden, isim-soyisim ile önceki randevuları görüntüleme ve iptal etme.
- **Değerlendirme Sistemi** — Tamamlanan randevular için yıldızlı puan ve yorum bırakma; yorumlar ana sayfada herkese açık gösterilir.

### Yönetici için
- **Özet Dashboard** — Toplam randevu, tahmini ciro ve aktif hizmet sayısı; Chart.js ile hizmet bazlı satış grafiği.
- **Hizmet & Uzman Yönetimi** — Yeni hizmet/uzman ekleme, mevcut hizmetleri silme.
- **Randevu Yönetimi** — Randevu durumunu "Bekliyor/Tamamlandı" olarak güncelleme, randevu silme.
- **Yorum Moderasyonu** — Gelen müşteri yorumlarını görüntüleme ve silme.

---

## 🛠️ Kullanılan Teknolojiler

| Katman | Teknoloji |
|---|---|
| Backend | Python, Flask |
| Şablon Motoru | Jinja2 |
| Veritabanı | _(muhtemelen SQLAlchemy + SQLite/PostgreSQL — proje sahibinin doğrulaması gerekir)_ |
| Grafikler | Chart.js |
| Barındırma | Render |

> Not: Bu README yalnızca HTML şablonları (`templates/`) incelenerek hazırlanmıştır. `app.py`, `requirements.txt` ve veritabanı modelleri projeye eklendiğinde bu bölümün netleştirilmesi gerekir.

---

## 📂 Proje Yapısı (şablonlar)

```
randevu-sistemi/
├── templates/
│   ├── index.html            # Ana sayfa — hizmet listesi ve yorumlar
│   ├── detay.html             # Seçilen hizmet için randevu formu
│   ├── basarili.html           # Randevu onay sayfası
│   ├── randevularim.html        # Randevu sorgulama ve değerlendirme
│   ├── admin_login.html          # Yönetici giriş ekranı
│   └── admin_panel.html           # Yönetici dashboard'u
├── app.py                          # Flask uygulaması (route'lar, veritabanı bağlantısı)
└── requirements.txt                 # Python bağımlılıkları
```

---

## 🚀 Kurulum

> Aşağıdaki adımlar tipik bir Flask projesi için genel şablondur; `app.py` ve `requirements.txt` dosyalarının depoya eklenmesiyle birlikte güncellenmelidir.

```bash
# Sanal ortam oluştur
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Ortam değişkenlerini ayarla (bkz. Güvenlik notu)
export ADMIN_PASSWORD="güçlü-bir-şifre"
export SECRET_KEY="rastgele-uzun-bir-anahtar"

# Uygulamayı çalıştır
flask run
```

---

## 🔒 Güvenlik Notu

- Yönetici paneli şifre tabanlı korunuyor. Şifre **kod içine sabit (hardcoded) yazılmamalı**, ortam değişkeni (`ADMIN_PASSWORD` gibi) üzerinden okunmalı ve arayüzde hiçbir yerde ipucu olarak gösterilmemelidir.
- Flask `SECRET_KEY` değeri de ortam değişkeninden gelmeli, repoya commit edilmemelidir.
- Randevu sorgulama yalnızca isim-soyisme dayalı olduğundan, aynı isme sahip kullanıcılar birbirinin randevu bilgilerine erişebilir — üretime alınmadan önce bu akışın gözden geçirilmesi önerilir.

---

## 🗺️ Yol Haritası

- [ ] Yönetici kimlik doğrulamasının ortam değişkenine taşınması.
- [ ] Randevu sorgulamanın isim yerine telefon + doğrulama koduyla güçlendirilmesi.
- [ ] `requirements.txt` ve `app.py` dosyalarının depoya eklenmesi.
- [ ] Randevu çakışma kontrolü (aynı uzman/saat için çift kayıt engeli).

---

## 📄 Lisans

Bu proje eğitim/portfolyo amaçlı geliştirilmiştir.

---

**Geliştirici:** Elif Aytekin
**İletişim:** Elifaytekinn@icloud.com
