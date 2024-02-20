from nemoguardrails import LLMRails, RailsConfig
from workshop_common import set_local_directory
from icecream import ic

# make sure python is looking in the right spot for the files we need.
set_local_directory()

config_path = './config-with-flow'

# load the configuration
config = RailsConfig.from_path(config_path)
rails = LLMRails(config=config)


# send a message to the model
response = rails.generate(messages=[{
    "role": "user",
    "content": "Hello!"
}])

ic(response)
