import asyncio
import logging
import os
import io
import tempfile
from pathlib import Path
from typing import Optional

import google.generativeai as genai
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
import requests
from PIL import Image
import speech_recognition as sr
from pydub import AudioSegment

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class GeminiTelegramBot:
    def __init__(self, telegram_token: str, gemini_api_key: str):
        self.telegram_token = telegram_token
        self.gemini_api_key = gemini_api_key
        
        genai.configure(api_key=gemini_api_key)
        
        self.text_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.image_gen_model = genai.GenerativeModel('gemini-2.0-flash-preview-image-generation')
        
        self.app = Application.builder().token(telegram_token).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("imagine", self.imagine_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        self.app.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        self.app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, self.handle_voice))
        self.app.add_handler(MessageHandler(filters.VIDEO, self.handle_video))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        welcome_message = """
🤖 مرحباً بك في البوت الذكي المدعوم بـ Gemini 2.0 Flash!

🎯 **إمكانيات البوت:**
• 💬 محادثة ذكية بالنصوص
• 🖼️ تحليل وفهم الصور
• 🎤 التعامل مع الرسائل الصوتية
• 🎨 توليد الصور بأمر /imagine
• 🎬 تحليل مقاطع الفيديو

📝 **كيفية الاستخدام:**
• أرسل أي نص للمحادثة
• أرسل صورة مع تعليق للتحليل
• أرسل رسالة صوتية للتفاعل
• استخدم /imagine [وصف] لتوليد صورة

🚀 ابدأ المحادثة الآن!
        """
        await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = """
🆘 **مساعدة البوت**

**الأوامر المتاحة:**
• `/start` - بدء التشغيل
• `/help` - عرض المساعدة  
• `/imagine [وصف]` - توليد صورة

**أمثلة لتوليد الصور:**
• `/imagine قط يلوح للكاميرا`
• `/imagine منظر طبيعي جميل عند الغروب`
• `/imagine سيارة رياضية حمراء`

**الميزات:**
• تحليل الصور المرسلة
• تحويل الصوت إلى نص والرد عليه
• محادثة ذكية بالذكاء الاصطناعي
        """
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def imagine_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("⚠️ يرجى إدخال وصف للصورة بعد الأمر\n\nمثال: `/imagine قط يلوح للكاميرا`", parse_mode=ParseMode.MARKDOWN)
            return
        
        prompt = " ".join(context.args)
        await update.message.reply_text("🎨 جاري توليد الصورة... قد يستغرق الأمر بضع ثوان")
        
        try:
            response = await self.generate_image(prompt)
            if response and hasattr(response, 'parts') and response.parts:
                for part in response.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        image_data = part.inline_data.data
                        image = Image.open(io.BytesIO(image_data))
                        
                        bio = io.BytesIO()
                        image.save(bio, format='PNG')
                        bio.seek(0)
                        
                        await update.message.reply_photo(
                            photo=bio,
                            caption=f"🎨 **الصورة المولدة:**\n📝 الوصف: {prompt}",
                            parse_mode=ParseMode.MARKDOWN
                        )
                        return
            
            # التحقق من النص أيضاً في حالة إرجاع رابط الصورة
            if response and response.text:
                await update.message.reply_text(f"🎨 تم توليد الصورة!\n\n{response.text}")
                return
                
            await update.message.reply_text("❌ عذراً، لم أتمكن من توليد الصورة. حاول مرة أخرى.")
            
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            await update.message.reply_text("❌ حدث خطأ أثناء توليد الصورة. حاول مرة أخرى لاحقاً.")
    
    async def generate_image(self, prompt: str):
        try:
            generation_config = genai.GenerationConfig(
                temperature=0.8,
                top_p=0.95,
                max_output_tokens=8192,
            )
            
            # استخدام موديل توليد الصور المخصص
            response = await asyncio.to_thread(
                self.image_gen_model.generate_content,
                prompt,
                generation_config=generation_config
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error in generate_image: {e}")
            return None
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_text = update.message.text
        
        try:
            await update.message.reply_text("🤔 جاري التفكير...")
            
            response = await asyncio.to_thread(
                self.text_model.generate_content,
                user_text
            )
            
            if response.text:
                response_text = response.text
                if len(response_text) > 4096:
                    for i in range(0, len(response_text), 4096):
                        await update.message.reply_text(response_text[i:i+4096])
                else:
                    await update.message.reply_text(response_text)
            else:
                await update.message.reply_text("❌ لم أتمكن من فهم الرسالة. حاول مرة أخرى.")
        
        except Exception as e:
            logger.error(f"Error handling text: {e}")
            await update.message.reply_text("❌ حدث خطأ أثناء معالجة الرسالة.")
    
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            await update.message.reply_text("🖼️ جاري تحليل الصورة...")
            
            photo = update.message.photo[-1]
            file = await context.bot.get_file(photo.file_id)
            
            image_bytes = io.BytesIO()
            await file.download_to_memory(image_bytes)
            image_bytes.seek(0)
            
            image = Image.open(image_bytes)
            
            prompt = "صف هذه الصورة بالتفصيل واشرح ما تراه فيها"
            if update.message.caption:
                prompt = f"{update.message.caption}"
            
            response = await asyncio.to_thread(
                self.text_model.generate_content,
                [prompt, image]
            )
            
            if response.text:
                await update.message.reply_text(f"🔍 **تحليل الصورة:**\n\n{response.text}", parse_mode=ParseMode.MARKDOWN)
            else:
                await update.message.reply_text("❌ لم أتمكن من تحليل الصورة.")
                
        except Exception as e:
            logger.error(f"Error handling photo: {e}")
            await update.message.reply_text("❌ حدث خطأ أثناء تحليل الصورة.")
    
    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            await update.message.reply_text("🎤 جاري تحليل الرسالة الصوتية...")
            
            voice = update.message.voice or update.message.audio
            file = await context.bot.get_file(voice.file_id)
            
            with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as temp_audio:
                await file.download_to_memory(temp_audio)
                temp_audio_path = temp_audio.name
            
            wav_path = temp_audio_path.replace('.ogg', '.wav')
            audio = AudioSegment.from_ogg(temp_audio_path)
            audio.export(wav_path, format="wav")
            
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                
            try:
                text = recognizer.recognize_google(audio_data, language='ar-SA')
                await update.message.reply_text(f"🎤 **النص المستخرج:**\n{text}")
                
                response = await asyncio.to_thread(
                    self.text_model.generate_content,
                    text
                )
                
                if response.text:
                    await update.message.reply_text(f"🤖 **الرد:**\n{response.text}")
                    
            except sr.UnknownValueError:
                await update.message.reply_text("❌ لم أتمكن من فهم الصوت. حاول التحدث بوضوح أكثر.")
            except sr.RequestError:
                await update.message.reply_text("❌ خطأ في خدمة تحويل الصوت إلى نص.")
            
            os.unlink(temp_audio_path)
            if os.path.exists(wav_path):
                os.unlink(wav_path)
                
        except Exception as e:
            logger.error(f"Error handling voice: {e}")
            await update.message.reply_text("❌ حدث خطأ أثناء معالجة الرسالة الصوتية.")
    
    async def handle_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            await update.message.reply_text("🎬 جاري تحليل الفيديو...")
            
            video = update.message.video
            file = await context.bot.get_file(video.file_id)
            
            video_bytes = io.BytesIO()
            await file.download_to_memory(video_bytes)
            video_bytes.seek(0)
            
            prompt = "صف محتوى هذا الفيديو"
            if update.message.caption:
                prompt = f"{update.message.caption}"
            
            response = await asyncio.to_thread(
                self.text_model.generate_content,
                [prompt, {"mime_type": video.mime_type, "data": video_bytes.getvalue()}]
            )
            
            if response.text:
                await update.message.reply_text(f"🎬 **تحليل الفيديو:**\n\n{response.text}", parse_mode=ParseMode.MARKDOWN)
            else:
                await update.message.reply_text("❌ لم أتمكن من تحليل الفيديو.")
                
        except Exception as e:
            logger.error(f"Error handling video: {e}")
            await update.message.reply_text("❌ حدث خطأ أثناء تحليل الفيديو.")
    
    def run(self):
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

async def main():
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        logger.error("يرجى تعيين متغيرات البيئة TELEGRAM_BOT_TOKEN و GEMINI_API_KEY")
        return
    
    bot = GeminiTelegramBot(TELEGRAM_TOKEN, GEMINI_API_KEY)
    
    logger.info("🚀 بدء تشغيل البوت...")
    bot.run()

if __name__ == '__main__':
    asyncio.run(main())
