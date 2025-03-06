__version__ = "1.2.8"

import yaml
import json
import os
import folder_paths
import importlib

cwd_path = os.path.dirname(os.path.realpath(__file__))
comfy_path = folder_paths.base_path

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

importlib.import_module('.py.routes', __name__)
importlib.import_module('.py.server', __name__)
nodes_list = ["util", "seed", "prompt", "loaders", "adapter", "inpaint", "preSampling", "samplers", "fix", "pipe", "xyplot", "image", "logic", "api", "deprecated"]
# locale = {}
for module_name in nodes_list:
    imported_module = importlib.import_module(".py.nodes.{}".format(module_name), __name__)
    NODE_CLASS_MAPPINGS = {**NODE_CLASS_MAPPINGS, **imported_module.NODE_CLASS_MAPPINGS}
    NODE_DISPLAY_NAME_MAPPINGS = {**NODE_DISPLAY_NAME_MAPPINGS, **imported_module.NODE_DISPLAY_NAME_MAPPINGS}
    # transfer python nodes to locale file
    # for i in imported_module.NODE_CLASS_MAPPINGS:
    #     locale[i] = {
    #         "display_name": imported_module.NODE_DISPLAY_NAME_MAPPINGS[i] if i in imported_module.NODE_DISPLAY_NAME_MAPPINGS else i,
    #         "inputs":{},
    #         "outputs":{},
    #     }
    #     node_class = imported_module.NODE_CLASS_MAPPINGS[i]
    #     input_types = node_class.INPUT_TYPES()
    #     if "required" in input_types:
    #         for j in input_types["required"]:
    #             locale[i]['inputs'][j] = {"name": j}
    #     if "optional" in input_types:
    #         for j in input_types["optional"]:
    #             locale[i]['inputs'][j] = {"name": j}
    #     count = 0
    #     if "RETURN_NAMES" in node_class.__dict__:
    #         for j in node_class.RETURN_NAMES:
    #             locale[i]['outputs'][str(count)] = {"name": j}
    #             count+=1

# en_json_path = os.path.join(cwd_path,'locales/en/nodeDefs.json')
# with open(en_json_path, 'w', encoding='utf-8') as f:
#     json.dump(locale, f, ensure_ascii=False, indent=2)


#Wildcards
from .py.libs.wildcards import read_wildcard_dict
wildcards_path = os.path.join(os.path.dirname(__file__), "wildcards")
if not os.path.exists(wildcards_path):
    os.mkdir(wildcards_path)
    
# Add custom wildcards example
example_path = os.path.join(wildcards_path, "example.txt")
if not os.path.exists(example_path):
    with open(example_path, 'w') as f:
        text = "blue\nred\nyellow\ngreen\nbrown\npink\npurple\norange\nblack\nwhite"
        f.write(text)
read_wildcard_dict(wildcards_path)

#Styles
styles_path = os.path.join(os.path.dirname(__file__), "styles")
samples_path = os.path.join(os.path.dirname(__file__), "styles", "samples")
if os.path.exists(styles_path):
    if not os.path.exists(samples_path):
        os.mkdir(samples_path)
else:
    os.mkdir(styles_path)
    os.mkdir(samples_path)

# Add custom styles example
example_path = os.path.join(styles_path, "your_styles.json.example")
if not os.path.exists(example_path):
    import json
    data = [
        {
            "name": "Example Style",
            "name_cn": "示例样式",
            "prompt": "(masterpiece), (best quality), (ultra-detailed), {prompt} ",
            "negative_prompt": "text, watermark, logo"
        },
    ]
    # Write to file
    with open(example_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# get comfyui revision
from .py.libs.utils import compare_revision

new_frontend_revision = 2546
web_default_version = 'v2' if compare_revision(new_frontend_revision) else 'v1'
# web directory
config_path = os.path.join(cwd_path, "config.yaml")
if os.path.isfile(config_path):
    with open(config_path, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        if data and "WEB_VERSION" in data:
            directory = f"web_version/{data['WEB_VERSION']}"
            with open(config_path, 'w') as f:
                yaml.dump(data, f)
        elif web_default_version != 'v1':
            if not data:
                data = {'WEB_VERSION': web_default_version}
            elif 'WEB_VERSION' not in data:
                data = {**data, 'WEB_VERSION': web_default_version}
            with open(config_path, 'w') as f:
                yaml.dump(data, f)
            directory = f"web_version/{web_default_version}"
        else:
            directory = f"web_version/v1"
    if not os.path.exists(os.path.join(cwd_path, directory)):
        print(f"web root {data['WEB_VERSION']} not found, using default")
        directory = f"web_version/{web_default_version}"
    WEB_DIRECTORY = directory
else:
    directory = f"web_version/{web_default_version}"
    WEB_DIRECTORY =  directory

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', "WEB_DIRECTORY"]

print(f'\033[34m[ComfyUI-Easy-Use] server: \033[0mv{__version__} \033[92mLoaded\033[0m')
print(f'\033[34m[ComfyUI-Easy-Use] web root: \033[0m{os.path.join(cwd_path, directory)} \033[92mLoaded\033[0m')
