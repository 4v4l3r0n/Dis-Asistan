# Kişisel Verilerin Korunması (KVKK) Aydınlatma Metni

**Proje:** DişAsistan — Ağız ve Diş Sağlığı AI Chatbot (PRJIC20250202)  
**Kanun:** 6698 Sayılı Kişisel Verilerin Korunması Kanunu (KVKK)

---

## 1. Veri Sorumlusu ve Amaç
Bu aydınlatma metni, **DişAsistan** yapay zeka sohbet robotu uygulaması üzerinden ağız ve diş sağlığı konularında bilgi alma sürecinde işlenebilecek kişisel verileriniz ve özel nitelikli kişisel verileriniz (sağlık verileri) hakkında sizleri bilgilendirmek amacıyla hazırlanmıştır.

## 2. İşlenen Veriler ve Dikkat Edilmesi Gerekenler
- Sohbet sırasında paylaştığınız mesajlar, konuşma bağlamının korunması amacıyla yerel **PostgreSQL** veritabanında oturum kimliği (`sessionId`) ile birlikte saklanmaktadır.
- Bu uygulama **eğitim ve bilgilendirme amaçlı bir prototiptir**. Sohbet esnasında lütfen **T.C. kimlik numarası, ad-soyad, açık adres, telefon numarası veya gerçek tıbbi rapor/görüntü** gibi doğrudan kimliğinizi belirleyici kişisel veriler paylaşmayınız.
- Dil modeli olarak **Google Gemini API (Ücretsiz Katman / Free Tier)** kullanıldığı durumlarda, gönderilen metinler Google'ın API gizlilik koşulları kapsamında işlenebilir; bu nedenle gerçek ve hassas kişisel sağlık verilerinizi girmemeniz önemle tavsiye edilir.

## 3. Tıbbi Sorumluluk Reddi
Bu chatbot tarafından sunulan yanıtlar **tıbbi tanı, teşhis veya tedavi yerine geçmez**. Ağız ve diş sağlığı ile ilgili her türlü şikayetinizde mutlaka bir **diş hekimine veya yetkili bir sağlık kuruluşuna** başvurunuz.

## 4. İlgili Kişinin Hakları
6698 sayılı KVKK'nın 11. maddesi uyarınca kişisel verilerinizin işlenip işlenmediğini öğrenme, verilerin silinmesini veya yok edilmesini talep etme haklarına sahipsiniz.
