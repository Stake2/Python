import openai

openai.api_key = "###################"

response = openai.Completion.create(
	engine = "davinci",
	prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: What is RAM?\nAI:",
	temperature = 0.9,
	max_tokens = 150,
	top_p = 1,
	frequency_penalty = 0.0,
	presence_penalty = 0.6,
	stop = ["\n", " Human:", " AI:"]
)

print(response)