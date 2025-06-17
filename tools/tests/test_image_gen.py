from tools.mcp_server.asset.image_gen import generate_image
from pathlib import Path


def test_image_generate():
    prompt = """
    Max,gg_max,cartoon character,underwater scene,A playful bunny cartoon,A beautifully detailed,soft cartoon-style anthropomorphic gg_max in the iconic Studio Ghibli animation style,A happy bunny cartoon gg_max relaxing at the bottom of a swimming pool while using a smartphone. The bunny,with gentle,expressive eyes and long,floating ears,wears blue and yellow swim attire,comfortably lounging on the pool floor. The underwater environment has a magical,dreamy feel with sunlight filtering through the water surface,creating dancing light patterns all around. Small colorful fish swim curiously nearby,and vibrant underwater plants sway gently with the water's movement. The bunny appears perfectly at ease underwater,breathing normally in this fantasy setting,focused on the glowing screen of the waterproof phone. Bubbles occasionally escape from the bunny's mouth,adding to the whimsical underwater atmosphere. The scene captures the serene yet magical underwater world in typical Ghibli fashion,with soft blues and greens dominating the color palette,enhanced by the ethereal underwater lighting. High detail,pastel color palette,soft lighting,and a focus on the peaceful underwater beauty.
        """
    res = generate_image(prompt, Path("tests/gen_images"))
    print(res)
    assert res.succeed
