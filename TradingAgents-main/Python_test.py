from openai import OpenAI

client = OpenAI(api_key="your-openai-api-key-here")  # Replace with your key
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Test message"}]
    )
    print("Key works! Response:", response.choices[0].message.content)
except Exception as e:
    print("Error:", e)
    
