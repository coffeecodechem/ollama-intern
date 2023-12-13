import json
import requests
import subprocess
import platform


class OllamaIntern:
    def __init__(self, model, system, stop_param, template, options):
        self.model = model
        self.stop_param = stop_param
        self.template = template
        self.options = options
        self.system = system
        self.os_context = platform.system()

    def ask_for_code(self, prompt):
        full_prompt = self.template.format(
            system=self.system,
            stop_param=self.stop_param,
            os_context=self.os_context,
            prompt=prompt,
        )
        return self.ask_ollama(full_prompt)

    def ask_ollama(self, full_prompt):
        if full_prompt is None:
            print("Prompt is None")
            return None

        print(f"Full prompt\n{full_prompt}")
        print()
        url = "http://localhost:11434/api/generate"
        data = {
            "model": self.model,
            "prompt": full_prompt,
            "options": self.options,
            "raw": True,
            "stream": False,
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response


# model = "neuralhermes2.5-mistral7b"
model = "deepseek-7b-instruct"
stop_param = "### End ###"
system = "Create the best code according to the instruction. Put the code inside clean triple single-quotes. "
template = """{system} Always end the response with {stop_param}
### Instruction:
Using {os_context} command, {prompt}
### Best code:
'''"""
options = {"stop": [stop_param]}

intern = OllamaIntern(model, system, stop_param, template, options)

prompt = input("Instruction: ")


user_confirmation = "r"
while user_confirmation == "r":
    response = intern.ask_for_code(prompt)

    dict_resp = json.loads(response.text)
    # print(dict_resp["response"])
    code = dict_resp["response"].strip("'\n")
    print("Code to be executed: ")
    print(code)
    user_confirmation = input(
        "Are you sure you want to execute the command? 'R' to regenerate (y/n/r): "
    )
    if user_confirmation.lower() == "y":
        # Run the command and capture its output
        try:
            output = subprocess.check_output(code, shell=True)
            decoded_output = output.decode("utf-8")
            print(decoded_output)
        except Exception as e:
            print("An error occurred while executing the command:\n", str(e))
    elif user_confirmation.lower() != "r":
        print("Command execution cancelled.")
        break
