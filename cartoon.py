import json
import math
import os
from generate_panels import generate_panels  # Assuming this module exists
from stability_ai import text_to_image  # Assuming this module exists
from add_text import add_text_to_panel  # Assuming this module exists
from create_strip import create_strip  # Assuming this module exists
from pdf import images_to_pdf  # Assuming this module exists
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from PIL import Image

# ==========================================================================================

# Clarifai configuration
PAT = 'a15d1d4c51754807b874c48b83c92693'
USER_ID = 'openai'
APP_ID = 'chat-completion'
MODEL_ID = 'GPT-4'
MODEL_VERSION_ID = '6c58be10ca3441bca2e9a956d28a47ce'

# Clarifai setup
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
metadata = (('authorization', 'Key ' + PAT),)
userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

# ==========================================================================================

def generate_scenario_from_topic(topic, num_pages):
    total_panels = num_pages * 6
    prompt = f"""
    You are a story creator. You need to create a continuous story based on the given topic.
    The story should be split into multiple parts, one for each comic page.
    Each part should be detailed enough to generate 6 comic panels. Number the panels continuously from 1 to {num_pages * 6} without any page markers.

    Topic: {topic}
    Number of Pages: {num_pages}

    Generate the story.
    """


    request = service_pb2.PostModelOutputsRequest(
        user_app_id=userDataObject,
        model_id=MODEL_ID,
        version_id=MODEL_VERSION_ID,  # optional
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    text=resources_pb2.Text(
                        raw=prompt
                    )
                )
            )
        ]
    )

    response = stub.PostModelOutputs(request, metadata=metadata)

    if response.status.code != status_code_pb2.SUCCESS:
        raise Exception(f"Request failed, status code: {response.status.code}")

    scenario = response.outputs[0].data.text.raw
    return scenario

def generate_comic_pages(scenario, style, num_pages):
    print("PRINT_SCN: ",type(scenario))
    
    panels = generate_panels(scenario)
    '''
    panels_per_page = 6
    total_panels = len(panels)
    for panel in panels:
        print(panel)
        
    total_pages = total_panels // panels_per_page
    print("tot_pag:",total_pages)
    
    if total_pages < num_pages:
        num_pages = total_pages
    print("num_pag:",num_pages)

    comic_pages = []
    for i in range(num_pages):
        start_index = i * panels_per_page
        end_index = min(start_index + panels_per_page, total_panels)
        page_panels = panels[start_index:end_index]

        print(f"Processing page {i+1}/{num_pages}, panels {start_index + 1} to {end_index}")

        panel_images = []
        
        for j, panel in enumerate(page_panels):
            panel_prompt = panel["description"] + ", cartoon box, " + style
            print(f"Generating panel {start_index + j + 1} with prompt: {panel_prompt}")
            panel_image = text_to_image(panel_prompt)
            if panel_image:
                panel_image_with_text = add_text_to_panel(panel["text"], panel_image)
                panel_images.append(panel_image_with_text)
            else:
                print(f"Failed to generate image for panel {start_index + j + 1}")

        if panel_images:
            comic_pages.append(create_strip(panel_images))
        else:
            print(f"No images generated for page {i+1}")

    return comic_pages

def save_comic_pages(comic_pages):
    if not os.path.exists('output1'):
        os.makedirs('output1')
    
    for i, page in enumerate(comic_pages):
        page.save(f"output1/page-{i + 1}.png")'''

# ==========================================================================================

def main():
    TOPIC = "Action"
    NUM_PAGES = 4
    STYLE = "american comic, colored"
    
    print(f"Generate a comic with style '{STYLE}' for the topic: '{TOPIC}', with {NUM_PAGES} pages")

    # Generate scenario from topic
    scenario = generate_scenario_from_topic(TOPIC, NUM_PAGES)
    
    print("Generated Scenario: ", scenario)

    # Generate comic pages based on the scenario
    comic_pages = generate_comic_pages(scenario, STYLE, NUM_PAGES)

    # Save the generated comic pages
    #save_comic_pages(comic_pages)
    #images_to_pdf('output1', 'output.pdf')

if __name__ == "__main__":
    main()
