"""
Типы данных для API Max
"""

from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field

# Типы событий (обновлений)


class UpdateType:
    MESSAGE_CREATED = "message_created"
    MESSAGE_CALLBACK = "message_callback"
    BOT_STARTED = "bot_started"
    MESSAGE_EDITED = "message_edited"
    MESSAGE_DELETED = "message_deleted"
    MESSAGE_CHAT_CREATED = "message_chat_created"

# Базовые модели


class User(BaseModel):
    user_id: int = Field(..., description="Идентификатор пользователя")
    name: str = Field(..., description="Отображаемое имя пользователя")
    username: Optional[str] = Field(None, description="Уникальное публичное имя пользователя")
    is_bot: bool = Field(..., description="Признак бота")
    last_activity_time: Optional[int] = Field(None, description="Время последней активности пользователя")
    description: Optional[str] = Field(None, description="Описание пользователя")
    avatar_url: Optional[str] = Field(None, description="URL аватара")
    full_avatar_url: Optional[str] = Field(None, description="URL полноразмерного аватара")
    first_name: Optional[str] = Field(..., description="Имя пользователя")
    last_name: Optional[str] = Field(..., description="Фамилия пользователя")


class BotCommand(BaseModel):
    name: str = Field(..., description="Название команды без слеша")
    description: str = Field(..., description="Описание команды")


class BotInfo(User):
    commands: Optional[List[BotCommand]] = Field(None, description="Список команд бота")


class MessageAttachment(BaseModel):
    type: str = Field(..., description="Тип вложения")
    payload: Dict[str, Any] = Field(..., description="Данные вложения")


class MarkupElement(BaseModel):
    ...


class MessageBody(BaseModel):
    text: Optional[str] = Field(None, description="Текст сообщения")
    mid: str = Field(..., description="Уникальный ID сообщения")
    seq: int = Field(..., description="ID последовательности сообщения в чате")
    attachments: Optional[List[MessageAttachment]] = Field(None, description="Вложения сообщения")
    markup: Optional[List[MarkupElement]] = Field(None, description="Разметка текста сообщения. https://dev.max.ru/docs-api#Форматирование%20текста")


class MessageRecipient(BaseModel):
    chat_id: int = Field(..., description="Идентификатор чата")
    chat_type: str = Field(..., description="Тип чата")
    user_id: int = Field(..., description="Идентификатор получателя")


class LinkedMessage(BaseModel):
    type: str = Field(..., description="reply|forward")
    message: 'Message' = Field(..., description="Сообщение")
    sender: 'User' = Field(..., description="Отправитель сообщения")
    chat_id: int = Field(..., description="Идентификатор чата")


class MessageStat(BaseModel):
    ...


class Message(BaseModel):
    """https://dev.max.ru/docs-api/objects/Message"""
    recipient: MessageRecipient = Field(..., description="Получатель сообщения")
    sender: Optional[User] = Field(..., description="Отправитель сообщения")
    body: Optional[MessageBody] = Field(...,
                                        description="Содержимое сообщения. Текст + вложения. Может быть null, если сообщение содержит только пересланное сообщение")
    timestamp: int = Field(..., description="Время отправки в Unix формате (миллисекунды)")
    link: Optional[LinkedMessage] = Field(None, description="Пересланное или ответное сообщение")
    stat: Optional[MessageStat] = Field(None, description="Статистика сообщения")
    url: Optional[str] = Field(None, description="Публичная ссылка на сообщение. Может быть null для диалогов или не публичных чатов")


class NewMessageBody(BaseModel):
    """https://dev.max.ru/docs-api/objects/NewMessageBody"""
    text: Optional[str] = Field(None, description="до 4000 символов. Новый текст сообщения")
    attachments: Optional[List[MessageAttachment]] = Field(None, description="Вложения сообщения")
    link: Optional[LinkedMessage] = Field(None, description="Ссылка на сообщение")
    format: Optional[str] = Field(None, description="Формат текста сообщения. Возможные значения: html, markdown")
    notify: Optional[bool] = Field(None, description="Оповещение о новом сообщении. По умолчанию true")


class Update(BaseModel):
    """https://dev.max.ru/docs-api/objects/Update"""
    update_type: str = Field(..., description="Тип обновления")
    timestamp: int = Field(..., description="Время обновления")
    message: Optional[Message] = Field(None, description="Сообщение, связанное с обновлением")
    user_locale: Optional[str] = Field(None, description="Языковая локаль. Например: ru-RU")
    callback_id: Optional[str] = Field(None, description="Идентификатор обратного вызова")
    payload: Optional[str] = Field(None, description="Полезные данные для обработки")
    chat_id: Optional[int] = Field(None, description="Идентификатор чата")
    user: Optional[User] = Field(None, description="Пользователь, который отправил сообщение")
    user_id: Optional[int] = Field(None, description="Идентификатор пользователя")
