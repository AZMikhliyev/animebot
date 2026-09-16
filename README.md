# Anime Kod-Bot — 0dan 100gacha qo'llanma

## 1-QISM: Telegram tomonda tayyorgarlik

### 1. Bot yaratish
1. Telegram'da **@BotFather** ni oching.
2. `/newbot` buyrug'ini yuboring.
3. Botga ism bering (masalan: `Anime Kod Bot`).
4. Username bering — `bot` bilan tugashi shart (masalan: `animekod_bot`).
5. BotFather sizga **token** beradi — bu ko'rinishda bo'ladi:
   `123456789:AAExampleTokenHere12345`
   Buni saqlab qo'ying, hech kimga bermang.

### 2. Yashirin (private) kanal yaratish
1. Telegram'da yangi **kanal** yarating (guruh emas, kanal!).
2. Kanal turi — **Private** qiling.
3. Kanalga istalgan nom bering (masalan: "Anime Bazasi").

### 3. Botni kanalga admin qilib qo'shish
1. Kanal sozlamalariga kiring → **Administrators** → **Add Admin**.
2. Yaratgan botingizni qidirib toping va qo'shing.
3. Botga kamida shu huquqlarni bering: **Post Messages**, **Edit Messages**, **Delete Messages**.
   (copy_message ishlashi uchun bot kanalda admin bo'lishi shart.)

### 4. Kanal ID'sini olish
1. Kanalga istalgan bitta xabar yozing (masalan "test").
2. O'sha xabarni **@userinfobot** yoki **@getidsbot** ga forward qiling.
3. Sizga kanal ID'si ko'rinadi — u har doim manfiy son bo'ladi va odatda
   `-100` bilan boshlanadi, masalan: `-1001234567890`.

### 5. O'zingizning Telegram ID'ingizni olish
1. **@userinfobot** ga `/start` yozing.
2. U sizga ID raqamingizni beradi (masalan: `123456789`).
3. Shu raqam — sizning **ADMIN_ID**'ingiz. Botni faqat siz (va xohlasangiz
   boshqa ishonchli odamlar) boshqarishi uchun kerak.

---

## 2-QISM: Kompyuterda kodni ishga tushirish

### 6. Python o'rnatilganini tekshirish
Terminalda:
```bash
python3 --version
```
Agar yo'q bo'lsa, python.org saytidan o'rnating (3.10+ tavsiya etiladi).

### 7. Loyihani joylash
Barcha fayllarni (`bot.py`, `config.py`, `database.py`, `requirements.txt`,
`.env.example`) bitta papkaga joylang, masalan `anime_bot/`.

### 8. Kerakli kutubxonalarni o'rnatish
```bash
cd anime_bot
pip install -r requirements.txt
```

### 9. `.env` faylini sozlash
`.env.example` faylidan nusxa oling va `.env` deb nomlang:
```bash
cp .env.example .env
```
Keyin `.env` faylini oching va o'z ma'lumotlaringizni kiriting:
```
BOT_TOKEN=sizning_token_shu_yerda
CHANNEL_ID=-1001234567890
ADMIN_IDS=123456789
```
(Bir nechta admin bo'lsa, vergul bilan ajrating: `ADMIN_IDS=123456789,987654321`)

### 10. Botni ishga tushirish
```bash
python3 bot.py
```
Terminal'da "Bot ishga tushdi, baza tayyor." degan yozuv chiqsa — bot ishlayapti.

---

## 3-QISM: Botdan foydalanish

### 11. Anime qo'shish (faqat admin uchun)
1. Kanalga kerakli anime qismini (video, hujjat va h.k.) post qiling.
2. O'sha postni kanaldan botga (shaxsiy chatga) **forward** qiling.
3. Bot sizdan kod so'raydi — masalan `AN001` deb yozing.
4. Bot "✅ Saqlandi!" deb javob beradi. Tayyor — endi shu kod ishlaydi.

### 12. Foydalanuvchi tomonidan
Foydalanuvchi botga shunchaki kodni yozadi (masalan `AN001`), bot esa
kanaldagi mos videoni **copy_message** orqali (kanal nomi ko'rinmasdan)
foydalanuvchiga yuboradi.

### 13. Boshqa admin buyruqlari
- `/list` — barcha kodlar ro'yxatini ko'rsatadi.
- `/count` — nechta anime borligini aytadi.
- `/delete AN001` — kodni o'chiradi.

---

## 4-QISM: Botni doimiy ishlab turishi uchun (production)

### 14. Serverга joylash
Uy kompyuterida botni doim ochiq qoldirish shart emas — arzon VPS (masalan
Hetzner, Timeweb, yoki mahalliy hosting) olib, shu yerda ishga tushiring.

### 15. Botni background'da ishlatish (Linux serverda)
```bash
nohup python3 bot.py &
```
Yoki yaxshiroq usul — **systemd service** yoki **screen/tmux** ishlatish,
shunda server qayta yuklanganda ham bot avtomatik ishga tushadi.

### 16. Majburiy obuna (force-subscribe) — ixtiyoriy kengaytma
Agar foydalanuvchilarni avval asosiy kanalga obuna bo'lishga majburlashni
xohlasangiz, `getChatMember` metodidan foydalanib, foydalanuvchi kod
yozishidan oldin obunani tekshirish funksiyasini qo'shishingiz mumkin —
buni xohlasangiz alohida qo'shib beraman.

---

## Muhim eslatmalar
- Kanal albatta **private** bo'lishi kerak — aks holda odamlar to'g'ridan-to'g'ri
  kanaldan ko'rib, botga ehtiyoj qolmaydi.
- `copy_message` kanal manzilini yashiradi, `forward_message` esa kanal
  nomini ko'rsatadi — shuning uchun kodda `copy_message` ishlatilgan.
- `.env` faylini hech qachon ommaga ochiq joyga (GitHub'ga public repo
  sifatida) yuklamang — bot tokeningiz o'g'irlanishi mumkin.
