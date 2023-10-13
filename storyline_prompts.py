import asyncio
import json
from langchain.callbacks.base import AsyncCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
topic_list_template = """
You are an agent orchestrator
<instructions>
When you execute tasks, have the ability create agents using “define agent” function
Later, call agent by @mention
Behave like a program
Maintain questions response experience, avoid going sideways on any topic except those specified in <agents> section
Strictly follow these instructions at all times
Output data only in the format specified by in <agents> section
Avoid explaining anything, instead simply run commands
</instructions>
<agents>
<define agent @ideas (topic)
definition = ""
You are an expert on generating video scripts from descriptions
You accept a prompt from the user in the format "10 facts about topic"
Ideas have to be coherent and tell and interesting story about the topic
You generate those 10 ideas and output as follows
[
{{
"name": "idea name",
"description": "explain the idea in 20-30 words",
}}
]
""
</define>
"""
scene_template = """
You are an agent orchestrator
<instructions>
When you execute tasks, have the ability create agents using “define agent” function
Later, call agent by @mention
Behave like a program
Maintain questions response experience, avoid going sideways on any topic except those specified in <agents> section
Output data only in the format specified by in <agents> section
Avoid explaining anything, instead simply run commands
Remove agent's name after calling
Strictly follow these instructions at all times
</instructions>
<metacommands>
/eval – is a meta-command for you.
When you see /eval in the routine descriptions down below, evaluate in place, do not talk to the user. Avoid showing the /eval command to the user, simply run it.
Take whatever command follows and print the evaluation of the execution of that command.
For instance, /eval @plan (process, system, goal) means you have to run the @plan agent with the given data and print only the results
</metacommands>
<agents>
<define agent @scene (story_point, topic_list)
definition = “”
You are an expert on generating descriptions of scenes for various topics based on the topic and the topic_list that are given for context
Make sure to keep the story coherent following the order of the objects
story_point is a JSON dictionary object, topic_list is a list of dictionaries
Generate a short narrative story for the story_point, in 100 words or less
Provide interesting facts, observations about story_point
Output as the following JSON object:
{{
“name”: “idea name”,
“story_point”: “copy the next from story_point to have a reference”,
“scene”: “short narrative story for the story_point, in 100 words or less”
}}
Avoid adding any other text or comments
""
</define>
</agents>
"""
image_template = """
You are an agent orchestrator.
<instructions>
When executing tasks, utilize the "define agent" function to create agents.
Invoke an agent by @mentioning them.
Operate in a programmatic manner.
Ensure a consistent question-response experience, only focusing on topics specified in the <agents> section.
Present data exclusively in the format outlined in the <agents> section.
Refrain from elaborations; simply execute commands.
Erase the agent's name post invocation.
Adhere to these guidelines unfailingly.
</instructions>
<metacommands>
Upon spotting /eval in the subsequent routine descriptions, compute it without notifying the user. Don't reveal the /eval command; just execute it. Evaluate the ensuing command and display only its result. E.g., /eval @plan (process, system, goal) necessitates triggering the @plan agent with the provided data, then showcasing solely the outcomes.
</metacommands>
<agents>
<define agent @image (description)
definition = ""
You specialize in formulating prompts for image generation models in line with given descriptions.
Upon receiving a prompt_description:
Analyze the description and extract the first principles to determine the core elements.
Use those principles to form a detailed and intricate image prompt.
Ensure that the prompt is highly descriptive, emphasizing the crucial elements to guide the image generation model.
Template for image_prompt based on the examples provided: "[Main Subject/Character], [Specific Details], [Background/Environment], [Colors], [Emotions/Theme], [Art Style/Technique], [Specific Artist/Style References (if any)], [Composition/Frame], [Additional Details], [Art Medium/Type]"
{{
"name": "idea name",
"image_prompt": "detailed and intricately described prompt suitable for image generation based on the template"
}}
Refrain from including any extraneous text or remarks.
""
</define>
</agents>
"""
def generete_ideas(topic):
    messages = [
        SystemMessagePromptTemplate.from_template(topic_list_template),
        HumanMessagePromptTemplate.from_template("@ideas {topic}"),
    ]
    prompt = ChatPromptTemplate.from_messages(messages)
    chain = LLMChain(prompt=prompt,
                     llm=ChatOpenAI(model_name="gpt-4",
                                    temperature=0,
                                    )
                     )
    topic_list = chain(inputs={"topic": topic})
    return json.loads(topic_list["text"])
def generete_scene(story_point, topic_list):
    messages = [
        SystemMessagePromptTemplate.from_template(scene_template),
        HumanMessagePromptTemplate.from_template(
            "@scene (story_point={story_point}, topic_list={topic_list})"),
    ]
    prompt = ChatPromptTemplate.from_messages(messages)
    chain = LLMChain(prompt=prompt,
                     llm=ChatOpenAI(model_name="gpt-4",
                                    temperature=0,
                                    )
                     )
    scene = chain(inputs={"story_point": story_point,
                          "topic_list": topic_list})
    return json.loads(scene["text"])

def generete_script(topic_list):
    script = []
    for topic in topic_list:
        script.append(generete_scene(topic, topic_list))
    return script

def generete_image_prompt(scene):
    scene = scene["scene"]
    messages = [
        SystemMessagePromptTemplate.from_template(image_template),
        HumanMessagePromptTemplate.from_template(
            "@image ({scene})"),
    ]
    prompt = ChatPromptTemplate.from_messages(messages)
    chain = LLMChain(prompt=prompt,
                     llm=ChatOpenAI(model_name="gpt-4",
                                    temperature=0,
                                    )
                     )
    image_prompt = chain(inputs={"scene": scene})
    return json.loads(image_prompt["text"])["image_prompt"]


def generete_all_image_prompts(script):
    image_prompts = []
    for scene in script:
        print(scene)
        image_prompts.append(generete_image_prompt(scene))
    return image_prompts


if __name__ == "__main__":
    topic = "brazil"
    ideas = generete_ideas(topic)
    print("ideas")
    print("\n")
    print(ideas)
    print("\n")
    script = generete_script(ideas)
    print("script")
    print("\n")
    print(script)
    print("\n")
    image_prompts = generete_all_image_prompts(script)
    print("image_prompts")
    print("\n")
    print(image_prompts)
    print("\n")