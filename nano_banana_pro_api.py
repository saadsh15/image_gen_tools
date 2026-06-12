import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

# Load environment variables from the .env file
load_dotenv()

def load_config(config_path="config.json"):
    """Loads settings from the JSON config file."""
    if not os.path.exists(config_path):
        # Create a default config if it doesn't exist
        default_config = {
            "prompt": """Here are the input images:
                1. The base shirt image(s).
                2. The `image_overlay` design.

                Using the logic provided in your system instructions, print the `image_overlay` onto the shirt. 
                Do not change the design of the overlay under any circumstances. Ensure the final two output images look like realistic, 
                high-quality product mockups with the exact design intact.""",
            "output_filename": "final_output.png",
            "generation_config": {
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40
            },
            "image_config": {
                "aspect_ratio": "16:9",
                "image_size": "2K"
            }
        }
        with open(config_path, "w") as f:
            json.dump(default_config, f, indent=4)
        print(f"Created default config at {config_path}")
        return default_config
    
    with open(config_path, "r") as f:
        return json.load(f)

def generate_image_with_context(config_path="config.json"):
    """
    Calls the Nano Banana Pro (gemini-3-pro-image) model.
    Reads prompt and settings from the provided config file and
    always includes two specific reference images and one overlay image in every prompt.
    Iterates to generate two images per run: one for a shirt, one for a hoodie.
    """
    config = load_config(config_path)
    base_prompt = config.get("prompt", "Combine the elements of these two images into a cohesive futuristic scene.")
    output_filename = config.get("output_filename", "final_output.png")

    # Hardcoded paths to the required realtime images and the overlay
    image_path_1 = "/home/saad/Projects/arzonama_bullshit/orignal/Generated Image June 10, 2026 - 3_04AM.jpg"
    image_path_2 = "/home/saad/Projects/arzonama_bullshit/orignal/Generated Image June 10, 2026 - 3_04AM(1).jpg"
    image_overlay = "/home/saad/Projects/arzonama_bullshit/overlay/Artwork upscalled water 1.png"

    if not os.path.exists(image_path_1):
        print(f"Error: Required image 1 '{image_path_1}' not found.")
        return
    if not os.path.exists(image_path_2):
        print(f"Error: Required image 2 '{image_path_2}' not found.")
        return
    if not os.path.exists(image_overlay):
        print(f"Error: Required overlay image '{image_overlay}' not found.")
        return

    # Initialize the client. This uses the GEMINI_API_KEY environment variable.
    client = genai.Client()

    # Load all input images
    print("Loading the reference images and the overlay...")
    img1 = Image.open(image_path_1)
    img2 = Image.open(image_path_2)
    overlay_img = Image.open(image_overlay)

    # Parse generation config values (temperature, top_p, top_k)
    gen_cfg = config.get("generation_config", {})
    temperature = gen_cfg.get("temperature", 0.7)
    top_p = gen_cfg.get("top_p", 0.95)
    top_k = gen_cfg.get("top_k", 40)

    # Parse image specific config values (aspect_ratio, image_size)
    img_cfg = config.get("image_config", {})
    aspect_ratio = img_cfg.get("aspect_ratio", "16:9")
    image_size = img_cfg.get("image_size", "2K")

    # Set up the GenerateContentConfig with the extracted settings
    api_config = types.GenerateContentConfig(
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=image_size
        )
    )

    print(f"Settings: Temperature={temperature}, top_p={top_p}, top_k={top_k}, aspect_ratio={aspect_ratio}, image_size={image_size}")

    apparel_types = ["shirt", "hoodie"]
    
    # Split the output filename to correctly inject the apparel type suffix
    name, ext = os.path.splitext(output_filename)
    if not ext:
        ext = ".png"

    # Generate an image for each apparel type
    for apparel in apparel_types:
        apparel_prompt = f"{base_prompt} Display this design clearly on a {apparel}."
        
        # Include the text prompt along with all three images
        contents = [apparel_prompt, img1, img2, overlay_img]
        
        current_output_file = f"{name}_{apparel}{ext}"
        
        print(f"\n--- Generating for: {apparel.upper()} ---")
        print(f"Sending request to Nano Banana Pro with prompt: '{apparel_prompt}'...")
        
        # Call the API for text-and-images-to-image
        response = client.models.generate_content(
            model="gemini-3.1-flash-image",
            contents=contents,
            config=api_config
        )

        # Process the response
        for part in response.parts:
            if part.text is not None:
                print("Response Text:", part.text)
            elif part.inline_data is not None:
                image = part.as_image()
                image.save(current_output_file)
                print(f"Image successfully generated and saved to {current_output_file}")

if __name__ == "__main__":
    # The script now drives its entire configuration from config.json
    generate_image_with_context("config.json")
