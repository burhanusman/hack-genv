import replicate
from urllib.request import urlretrieve
from PIL import Image
from concurrent.futures import ThreadPoolExecutor


cl = replicate.Client(api_token="r8_DiLrYycfLirwy9wNkWG2CRubyo1lHBt1JTCES")

output = cl.run(
    "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
    input={"prompt": "a vision of paradise. unreal engine"}
)
print(output)

urlretrieve(output[0], "/tmp/out.png")
with Image.open("/tmp/out.png") as im:
    im.show()


def generate_image(prompt):
    input_payload={"prompt": prompt}
    output_link = cl.run(
    "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
    input=input_payload)
    return output_link



def generate_list_of_images(list_of_prompts):
    with ThreadPoolExecutor() as executor:
        output_links = list(executor.map(generate_image, list_of_prompts))
    output_links=[item[0] for item in output_links]
    return output_links



