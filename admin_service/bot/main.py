import asyncio
import logging
import sys
import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
)
from config import settings
from admin_config import settings as admin_settings
from handlers.routes.start_router import router as start_router
from aiogram.filters import Command

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/team-requests")
async def handle_team_request(request: Request):
    try:
        data = await request.json()

        required_fields = ["leader_id", "team_name", "org_name"]
        if not all(field in data for field in required_fields):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        group_message = await bot.send_message(
            chat_id=admin_settings.GROUP_CHAT_ID,
            text=f"🆕 Запрос на добавление организации:\n\n"
                 f"👤 User ID: {data['leader_id']}\n"
                 f"🏷 хочет создать команду - : {data['team_name']}\n"
                 f"🏢 Но нет такой организации в бд - Org: {data['org_name']} добавить ли такую в бд ?",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="✅ Approve",
                            callback_data=f"approve:{data['team_name']}:{data['org_name']}:{data['leader_id']}",
                        ),
                        InlineKeyboardButton(
                            text="❌ Reject",
                            callback_data=f"reject:{data['team_name']}",
                        )
                    ]
                ]
            )
        )

        for admin_id in admin_settings.admin_ids:
            try:
                await bot.send_message(
                    admin_id,
                    f"🆕 Запрос на добавление организации в базу данных:\n\n"
                    f"👤 User ID: {data['leader_id']}\n"
                    f"🏷 Team: {data['team_name']}\n"
                    f"🏢 Org: {data['org_name']}",
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text="✅ Approve",
                                    callback_data=f"approve:{data['team_name']}:{data['org_name']}:{data['leader_id']}",
                                ),
                                InlineKeyboardButton(
                                    text="❌ Reject",
                                    callback_data=f"reject:{data['team_name']}",
                                ),
                            ]
                        ]
                    ),
                )
            except Exception as e:
                logging.error(f"Failed to send message to admin {admin_id}: {str(e)}")

        return {"status": "success"}

    except Exception as e:
        logging.error(f"Error in handle_team_request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@dp.callback_query(F.data.startswith("approve:"))
async def approve_team_request(callback: CallbackQuery):
    try:
        _, team_name, org_name, leader_id = callback.data.split(":")

        async with httpx.AsyncClient() as client:

            org_response = await client.post(
                f"{admin_settings.RSK_ORGS_URL}/organizations/create/",
                json={"name": org_name},
                headers={"X-Admin-Token": admin_settings.ADMIN_SECRET_KEY},
                timeout=10.0,
            )

            if org_response.status_code not in (200, 201):
                raise Exception(f"Organization creation failed: {org_response.text}")

        await callback.answer("✅ Одобрено администратором")
        await callback.message.reply("добавлено")


    except Exception as e:
        logging.error(f"Error in approve_team_request: {str(e)}")
        await callback.answer("❌ Ошибка при обработке запроса")
        await callback.message.reply("Произошла ошибка при обработке вашего запроса")


@dp.callback_query(F.data.startswith("reject:"))
async def reject_team_request(callback: CallbackQuery):
    try:
        _, team_name = callback.data.split(":")
        await callback.answer("❌ Запрос отклонен")
        await callback.message.edit_text(
            f"{callback.message.text}\n\n❌ Отклонено администратором",
            reply_markup=None,
        )
    except Exception as e:
        logging.error(f"Error in reject_team_request: {str(e)}")
        await callback.answer("❌ Ошибка при обработке запроса")

@dp.message(Command("chat_id"))
async def cmd_chat_id(message: Message):
    chat = message.chat
    if chat.type == "private":
        chat_type = "личные сообщения"
    elif chat.type == "group":
        chat_type = "обычная группа"
    elif chat.type == "supergroup":
        chat_type = "супергруппа"
    elif chat.type == "channel":
        chat_type = "канал"
    else:
        chat_type = "неизвестный тип чата"
        
    response = (
        f"📌 Информация о чате:\n\n"
        f"🆔 ID чата: <code>{chat.id}</code>\n"
        f"📛 Тип: {chat_type}\n"
        f"🏷 Название: {chat.title if chat.title else 'нет'}\n"
        f"👤 Ваш ID: <code>{message.from_user.id}</code>"
    )
    
    await message.reply(response, parse_mode="HTML")


async def run_api():
    import uvicorn

    config = uvicorn.Config(app, host="0.0.0.0", port=8009, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def run_bot():
    dp.include_router(start_router)
    await dp.start_polling(bot)


async def main():
    await asyncio.gather(run_api(), run_bot())


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
    asyncio.run(main())
