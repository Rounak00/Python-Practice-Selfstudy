from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import requests
from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()
@tool
def get_weather_data(city: str) -> str:
  """
  This function fetches the current weather data for a given city
  """
  url = f'https://api.weatherstack.com/current?access_key=4d1d8ae207a8c845a52df8a67bf3623e&query={city}'
  response = requests.get(url)
  return response.json()

llm = ChatOpenAI()

from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
# Step 2: Pull the ReAct prompt from LangChain Hub
prompt = hub.pull("hwchase17/react")  # pulls the standard ReAct agent prompt
# Step 3: Create the ReAct agent manually with the pulled prompt
agent = create_react_agent(
    llm=llm,
    tools=[search_tool, get_weather_data],
    prompt=prompt
)

# Step 4: Wrap it with AgentExecutor
agent_executor = AgentExecutor(
    agent=agent,
    tools=[search_tool, get_weather_data],
    verbose=True
)

# Step 5: Invoke
response = agent_executor.invoke({"input": "Find the capital of Madhya Pradesh, then find it's current weather condition"})
print(response)

# > Entering new AgentExecutor chain...
# I should first find out the capital of Madhya Pradesh and then check the current weather condition for that city.
# Action: duckduckgo_search
# Action Input: "capital of Madhya Pradesh"Madhya Pradesh, state of India that is situated in the heart of the country. It has no coastline and no international frontier. Its physiography is characterized by low hills, extensive plateaus, and river valleys. The capital is Bhopal, in the west-central part of the state. Bhopal, city, capital of Madhya Pradesh state, central India. Situated in the fertile plain of the Malwa Plateau, the city lies just north of the Vindhya Range, along the slopes of a sandstone ridge. It is a major rail junction and has an airport. Pop. (2001) 1,437,354; (2011) 1,798,218. Bhopal was Indore (/ ɪ n ˈ d ɔːr / ⓘ; ISO: Indaura, Hindi: [ɪn̪d̪ɔːr]) is the largest and most populous city in the Indian state of Madhya Pradesh. [15] It is the commercial hub of Madhya Pradesh. It is consistently ranked as the cleanest city in India. [16] It serves as the headquarters of both the Indore District and the Indore Division.It is also considered the state education hub and ... In 1956, Bhopal became part of the state of Madhya Pradesh. Bhopal district was carved out on October 2, 1972, and is one of the 45 districts in the state. 4. Why is Bhopal famous? Bhopal is the capital city of the Indian state of Madhya Pradesh. It is known as the City of Lakes due to the presence of various natural and artificial lakes. In 1948, Madhya Bharat was created, with Indore designated as its summer capital and Gwalior as its winter capital. This arrangement highlights Indore's significance even then. However, Madhya Bharat was a temporary entity, and the map of central India was soon to be redrawn. The Creation of Madhya PradeshNow that I know the capital of Madhya Pradesh is Bhopal, I can use the get_weather_data function to check its current weather condition.
# Action: get_weather_data
# Action Input: Bhopal{'request': {'type': 'City', 'query': 'Bhopal, India', 'language': 'en', 'unit': 'm'}, 'location': {'name': 'Bhopal', 'country': 'India', 'region': 'Madhya Pradesh', 'lat': '23.267', 'lon': '77.400', 'timezone_id': 'Asia/Kolkata', 'localtime': '2025-05-01 17:52', 'localtime_epoch': 1746121920, 'utc_offset': '5.50'}, 'current': {'observation_time': '12:22 PM', 'temperature': 40, 'weather_code': 116, 'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0002_sunny_intervals.png'], 'weather_descriptions': ['Partly Cloudy '], 'astro': {'sunrise': '05:47 AM', 'sunset': '06:48 PM', 'moonrise': '08:38 AM', 'moonset': '11:01 PM', 'moon_phase': 'Waxing Crescent', 'moon_illumination': 15}, 'air_quality': {'co': '510.6', 'no2': '1.665', 'o3': '180', 'so2': '10.175', 'pm2_5': '29.045', 'pm10': '68.635', 'us-epa-index': '2', 'gb-defra-index': '2'}, 'wind_speed': 12, 'wind_degree': 302, 'wind_dir': 'WNW', 'pressure': 1005, 'precip': 0, 'humidity': 7, 'cloudcover': 25, 'feelslike': 40, 'uv_index': 1, 'visibility': 6, 'is_day': 'yes'}}The current weather condition in Bhopal, Madhya Pradesh is partly cloudy with a temperature of 40°C.
# Final Answer: The capital of Madhya Pradesh is Bhopal, and the current weather condition in Bhopal is partly cloudy with a temperature of 40°C.

# > Finished chain.
# {'input': "Find the capital of Madhya Pradesh, then find it's current weather condition", 'output': 'The capital of Madhya Pradesh is Bhopal, and the current weather condition in Bhopal is partly cloudy with a temperature of 40°C.'}

print(response['output'])
# The capital of Madhya Pradesh is Bhopal, and the current weather condition in Bhopal is partly cloudy with a temperature of 40°C.