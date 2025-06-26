# 🤖 Gemini 2.0 Flash Telegram Bot

<div align="center">

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)
![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-orange.svg)

**بوت تيليجرام ذكي مدعوم بتقنية Gemini 2.0 Flash للذكاء الاصطناعي**

[التثبيت](#-التثبيت) • [الاستخدام](#-الاستخدام) • [الميزات](#-الميزات) • [التكوين](#️-التكوين)

</div>

## 🌟 نظرة عامة

بوت تيليجرام متقدم يستخدم أحدث تقنيات الذكاء الاصطناعي من Google Gemini 2.0 Flash، يوفر تجربة تفاعلية شاملة مع إمكانيات متعددة الوسائط.

## ✨ الميزات

### 🎯 الإمكانيات الأساسية
- **💬 محادثة ذكية**: تفاعل طبيعي باللغة العربية والإنجليزية
- **🖼️ تحليل الصور**: فهم وتحليل الصور المرسلة مع وصف مفصل
- **🎤 معالجة الصوت**: تحويل الرسائل الصوتية إلى نص والرد عليها
- **🎬 تحليل الفيديو**: فهم محتوى مقاطع الفيديو وتحليلها
- **🎨 توليد الصور**: إنشاء صور مخصصة باستخدام الذكاء الاصطناعي

### 🔧 الميزات التقنية
- **⚡ أداء سريع**: استخدام Gemini 2.0 Flash للاستجابة السريعة
- **🎨 توليد صور متقدم**: استخدام `gemini-2.0-flash-preview-image-generation`
- **🔄 معالجة غير متزامنة**: تعامل فعال مع الطلبات المتعددة
- **🛡️ معالجة الأخطاء**: نظام قوي لمعالجة الأخطاء
- **📊 تسجيل مفصل**: نظام تسجيل شامل لمراقبة الأداء

## 📋 متطلبات النظام

- Python 3.8 أو أحدث
- مفتاح API من Google Gemini
- توكن بوت تيليجرام
- اتصال إنترنت مستقر

## 🚀 التثبيت

### 1. استنساخ المشروع
```bash
git clone https://github.com/Jawsey/gemini-telegram-bot.git
cd gemini-telegram-bot
```

### 2. إنشاء بيئة افتراضية
```bash
python -m venv venv
source venv/bin/activate  # في Linux/Mac
# أو
venv\Scripts\activate     # في Windows
```

### 3. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 4. تكوين متغيرات البيئة
إنشاء ملف `.env` في المجلد الجذر:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
```

## ⚙️ التكوين

### الحصول على مفتاح Gemini API
1. اذهب إلى [Google AI Studio](https://aistudio.google.com/)
2. أنشئ حساب جديد أو سجل الدخول
3. احصل على مفتاح API مجاني
4. انسخ المفتاح إلى ملف `.env`

### إنشاء بوت تيليجرام
1. ابحث عن `@BotFather` في تيليجرام
2. أرسل `/newbot` واتبع التعليمات
3. احصل على توكن البوت
4. انسخ التوكن إلى ملف `.env`

## 🏃‍♂️ تشغيل البوت

```bash
python bot.py
```

## 📱 كيفية الاستخدام

### الأوامر الأساسية
- `/start` - بدء التشغيل ورسالة الترحيب
- `/help` - عرض المساعدة والأوامر المتاحة
- `/imagine [وصف]` - توليد صورة مخصصة

### أمثلة الاستخدام

#### توليد الصور
```
/imagine قط يلوح للكاميرا
/imagine منظر طبيعي جميل عند الغروب
/imagine سيارة رياضية حمراء لامعة
```

#### تحليل الصور
- أرسل أي صورة مع أو بدون تعليق
- سيقوم البوت بتحليلها ووصف محتواها

#### الرسائل الصوتية
- أرسل رسالة صوتية
- سيتم تحويلها إلى نص والرد عليها

## 🏗️ هيكل المشروع

```
gemini-telegram-bot/
├── bot.py              # الملف الرئيسي للبوت
├── requirements.txt    # متطلبات Python
├── README.md          # وثائق المشروع
├── .env.example       # مثال لملف البيئة
└── .gitignore         # ملفات Git المتجاهلة
```

## 🔧 التخصيص

### إضافة ميزات جديدة
يمكن بسهولة إضافة معالجات جديدة في دالة `_setup_handlers()`:

```python
def _setup_handlers(self):
    # إضافة معالجات مخصصة هنا
    self.app.add_handler(CommandHandler("custom", self.custom_command))
```

### تخصيص النماذج
يمكن تغيير النماذج المستخدمة:

```python
# للنصوص والتحليل
self.text_model = genai.GenerativeModel('gemini-2.0-flash-exp')
# لتوليد الصور - الموديل المخصص الجديد
self.image_gen_model = genai.GenerativeModel('gemini-2.0-flash-preview-image-generation')
```

## 🐛 معالجة الأخطاء

البوت يتضمن نظام معالجة أخطاء شامل:
- تسجيل مفصل للأخطاء
- رسائل خطأ واضحة للمستخدمين
- استرداد تلقائي من الأخطاء

## 📊 المراقبة

يمكن مراقبة أداء البوت من خلال:
- سجلات النظام المفصلة
- مراقبة استخدام API
- تتبع الأخطاء والاستثناءات

## 🤝 المساهمة

نرحب بالمساهمات! يرجى:

1. Fork المشروع
2. إنشاء فرع للميزة الجديدة (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push إلى الفرع (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

## 🆘 الدعم

إذا واجهت أي مشاكل:

1. تحقق من [الأسئلة الشائعة](#-الأسئلة-الشائعة)
2. ابحث في [Issues](https://github.com/Jawsey/gemini-telegram-bot/issues)
3. أنشئ Issue جديد إذا لم تجد حلاً

## 🙏 الشكر والتقدير

- [Google Gemini](https://gemini.google.com/) لتوفير واجهة برمجة التطبيقات
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) للمكتبة الممتازة
- المجتمع المفتوح المصدر للدعم المستمر

## 📈 الإحصائيات

![GitHub stars](https://img.shields.io/github/stars/Jawsey/gemini-telegram-bot.svg?style=social)
![GitHub forks](https://img.shields.io/github/forks/Jawsey/gemini-telegram-bot.svg?style=social)
![GitHub issues](https://img.shields.io/github/issues/Jawsey/gemini-telegram-bot.svg)

---

<div align="center">

**⭐ إذا أعجبك المشروع، لا تنس إعطاؤه نجمة! ⭐**

صُنع بـ ❤️ بواسطة [Jawsey](https://github.com/Jawsey)

</div>