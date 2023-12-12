import json
import requests
import subprocess


def ask_ollama(model, full_prompt, options):
    if full_prompt is None:
        print("Prompt is None")
        return None

    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": full_prompt,
        "options": options,
        "raw": True,
        "stream": False,
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    # print(response.text)
    return response


# model = "neuralhermes2.5-mistral7b"
model = "deepseek-7b-instruct"
stop_param = "### End ###"
template = """{system} Always end the response with {stop_param}
### Instruction:
{prompt}
### Best code:
'''"""

system = "Create the best code according to the instruction. Put the code inside clean triple single-quotes. "
prompt = "Windows Command Prompt command to list current directory"
options = {"stop": [stop_param]}
full_prompt = template.format(system=system, stop_param=stop_param, prompt=prompt)
print(f"Full prompt:\n{full_prompt}", end="")
response = ask_ollama(
    model,
    full_prompt,
    options=options,
)

dict_resp = json.loads(response.text)
print(dict_resp["response"])
code = dict_resp["response"].strip("'\n")
print("Code to be executed: ")
print(code)
user_confirmation = input("Are you sure you want to execute the command? (y/n):")
if user_confirmation.lower() == "y":
    # Run the command and capture its output
    try:
        output = subprocess.check_output(code, shell= True)
        decoded_output= output.decode('utf-8')
        print(decoded_output)
    except Exception as e:
        print("An error occurred while executing the command:\n", str(e))
else:
    print("Command execution cancelled.")