# import pyyaml module
import yaml
from yaml.loader import SafeLoader

# Open the file and load the file
def readYaml():
    with open('harvesting.yaml') as f:
        data = yaml.load(f, Loader=SafeLoader)
        print(data)
    return data
