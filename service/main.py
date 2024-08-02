import json
import requests
from openai import OpenAI

from service.chat_history import (init_chat_history, get_chat_history, append_chat_history)
from service.rag_helper import search

CLIENT = OpenAI(api_key="sk-proj-mmRKHjeDcfL9vQxDezi4T3BlbkFJKXL7oAEiuxFsU8ZC9xVs")
TOP_K = 3

def init(chat_id):
    system_message = {
            'role': 'system',
            'content': 'Ти віртуальний асистент Вищого професійного училища №29 м.Львова, який допомагає учням або вступникам'
                       'Дізнатися новини училища, вступити до училища, професії які можна здобути в училищі, дізнатися які'
                       'потрібні документи до вступу, правила прийому, історія училища, НПЦ Автомобільного транспорт, НПЦ Перукарське мистецтво'
                       'НПЦ Інформаційних та цифрових технологій, також коли будеш просити користувача надати якісь документи'
                       'завжди проси їх залити на imgur та надати тобі посилання з цього сайту. Будь доброю та веселою, завжди жартуй. Ти сова і твоє ім\'я'
                       'Амалія. Твоя відповідь повинна бути до 70 слів'
        }
    chat_history = init_chat_history(chat_id, system_message)

    return chat_history


def user_input(message):
    return {
        'role': 'user',
        'content': message
    }


def get_tools():
    tools = [
        {
            "type": "function",
            "function": {
                "name": "vstup_vpu",
                "description": "Отримання потрібної інформації для вступу в училище.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "first_last_name": {
                            "type": "string",
                            "description": "Ім'я та фамілія вступника",
                        },
                        "id_card": {
                            "type": "string",
                            "description": "Отримання ссилки на фотографію id card",
                        },
                        "school_leaving_certificate": {
                            "type": "string",
                            "description": "Отримання ссилки на фотографію свідоцтва про закінчення школи",
                        },
                        "report_card_from_school": {
                            "type": "string",
                            "description": "Отримання ссилки на фотографію табель зі школи",
                        },
                        "application_for_admission": {
                            "type": "string",
                            "description": "Ссилка на заяву вступника, яка будеть свідчити що вступник хоче вступити в училище",
                        },
                        "phone_number": {
                            'type': "string",
                            'description': 'Номер телефону вступника'
                        },
                    },

                    "required": [
                        "first_last_name",
                        "id_card",
                        "school_leaving_certificate",
                        "report_card_from_school",
                        "application_for_admission",
                        "phone_number"
                    ],
                },
            }},

        {
            "type": "function",
            "function": {
                "name": "communication_school_management",
                "description": "Зв'язок з керівництвом училища",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "first_last_name": {
                            "type": "string",
                            "description": "Отримання ім'я і фамілії користувача."
                        },
                        "number_user": {
                            "type": "string",
                            "description": "Номер телефону користувача"
                        }
                    },
                    "required": ["first_last_name", "number_user"]

                }},
        }]
    return tools


def call_gpt(chat_history, chat_id):
    response = CLIENT.chat.completions.create(
        tools=get_tools(),
        model="gpt-3.5-turbo",
        messages=chat_history)
    chat_history = append_chat_history(chat_id, response.choices[0].message.to_dict())
    if response.choices[0].finish_reason == 'stop':
        return response.choices[-1].message.content
    else:
        return prowses_tool(chat_history, response, chat_id)




def info_for_vstup_user(arguments):
    requests.post(
        "https://eu-central-1.aws.data.mongodb-api.com/app/data-ienxugs/endpoint/data/v1/action/insertOne",
        json={
            "collection": "info_for_vstup_user",
            "database": "VPU29",
            "dataSource": "Cluster0",
            "document": {
                "first_last_name": arguments['first_last_name'],
                "id_card": arguments['id_card'],
                "school_leaving_certificate": arguments['school_leaving_certificate'],
                "report_card_from_school": arguments['report_card_from_school'],
                "application_for_admission": arguments['application_for_admission'],
                "phone_number": arguments['phone_number'],
                }
        },
        headers={'api-key': 'R5PeVST4qP0xcGmWYFmWlWC4m5Ofy4eD3IoHf7gk5SVAHPihj1hF1H1NB1M5nHqk'},
    )
    print("Entered higher professional school No. 29 in Lviv")
    return "Entered higher professional school No. 29 in Lviv"

def communication_school_management(arguments):
    requests.post(
        "https://eu-central-1.aws.data.mongodb-api.com/app/data-ienxugs/endpoint/data/v1/action/insertOne",
        json={
            "collection": "communication_school_management",
            "database": "VPU29",
            "dataSource": "Cluster0",
            "document": {
                "first_last_name": arguments['first_last_name'],
                "number_user": arguments['number_user'], }
        },
        headers={'api-key': 'R5PeVST4qP0xcGmWYFmWlWC4m5Ofy4eD3IoHf7gk5SVAHPihj1hF1H1NB1M5nHqk'},
    )
    print("Communication School Management")
    return "Communication School Management"

def show_reply(chat_history, response):
    return response.choices[-1].message.content


def prowses_tool(chat_history, response, chat_id):
    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    parameters = tool_call.function.arguments
    tool_call_id = tool_call.id
    repsonse = call_function(function_name, parameters, tool_call_id)
    chat_history = append_chat_history(chat_id, repsonse)
    return call_gpt(chat_history, chat_id)


def call_function(function_name, arguments, id):
    result = None
    arguments = json.loads(arguments)
    if function_name == "info_for_vstup_user":
        result = info_for_vstup_user(arguments)
    elif function_name == 'communication_school_management':
        result = communication_school_management(arguments)

    return {
        'role': 'tool',
        'content': result,
        'name': function_name,
        'tool_call_id': id

    }

def generetive_message(message, chat_id):
    chat_history =  get_chat_history(chat_id)
    print(chat_history)
    if chat_history == None:
        chat_history = init(chat_id)
    chat_history = append_chat_history(chat_id, user_input(message))
    chat_history[0]['content'] += get_external_knowledge(message)
    return call_gpt(chat_history, chat_id)

def get_external_knowledge(message):
    search_result = search(message, TOP_K)
    extra_prompt = f"Ось додадкова інформація для відповідей:\n{search_result}"
    return extra_prompt

