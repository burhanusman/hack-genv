from langchain.prompts.chat import ChatPromptTemplate,SystemMessagePromptTemplate,HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0.3)


def first_level_request(concept):
    template = "You know a lot of world facts."
    human_template = "List 10 facts about {concept}"
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    formated_prompt=chat_prompt.format_messages(concept=concept)
    resp_chat = chat.predict_messages(formated_prompt)
    return resp_chat

def get_facts(first_response):
    return ["green places", "many mountains", "Blue river"]

def get_script(fact):
    template = "You can elongate on ideas"
    human_template = "Explain this fact:{fact}"
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    formated_prompt=chat_prompt.format_messages(fact=fact)
    resp_chat = chat.predict_messages(formated_prompt)
    return resp_chat

def get_scripts(facts):
    scripts=[]
    for fact in facts:
        scripts.append(get_script(fact))
    return scripts

def get_output(user_prompt):
    first_response=first_level_request("brazil")
    facts=get_facts(first_response)
    scripts=get_scripts(facts)
    return scripts