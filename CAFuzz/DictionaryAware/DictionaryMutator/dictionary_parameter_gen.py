import os
import json
import random
import string

class ParameterGenerator:
    def __init__(self):
        # 클래스 초기화 시 필요한 설정이 있다면 이곳에 작성
        pass

    def generate_random_string(self, prefix, max_len):
        """
        prefix 포함 최대 길이를 만족하는 랜덤 문자열을 생성한다.
        """
        remaining_len = max_len - len(prefix)
        chars = string.ascii_letters + string.digits + "_"
        random_length = random.randint(1, remaining_len) if remaining_len > 0 else 0
        suffix = "".join(random.choice(chars) for _ in range(random_length))
        return prefix + suffix

    def generate_random_value(self, param_def):
        """
        파라미터 정의(param_def)에 맞게 랜덤 값을 생성한다.
        """
        param_type = param_def["type"]
        
        if param_type == "enum":
            return random.choice(param_def["possible_values"])
        
        elif param_type == "enum_string":
            return random.choice(param_def["possible_values"])
        
        elif param_type == "range":
            return random.randint(param_def["min"], param_def["max"])
        
        elif param_type == "string":
            prefix = param_def.get("prefix", "")
            max_len = param_def.get("max_len", 20)
            return self.generate_random_string(prefix, max_len)
        
        else:
            return None

    def generate_parameters(self, command_code, constraints_dict):
        """
        command_code에 해당하는 파라미터 목록을 생성한다.
        """
        if command_code not in constraints_dict:
            return []
        
        param_defs = constraints_dict[command_code]["params"]
        generated_params = []
        for pdef in param_defs:
            generated_params.append(self.generate_random_value(pdef))
        
        return generated_params

    def run_generation(self):
        """
        dictionarys 폴더의 JSON을 랜덤으로 선택한 뒤,
        해당 JSON에 있는 모든 command_code에 대해 파라미터를 생성해 출력한다.
        """
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        dictionary_names = [
            "CFE_ES.json",
            "CFE_EVS.json",
            "CFE_SB.json",
            "CFE_TBL.json",
            "CFE_TIME.json"
        ]

        random_number = random.randint(0, 4)
        dictionary_name = dictionary_names[random_number]
        file_name = os.path.join(script_dir, "..", "dictionarys", dictionary_name)

        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)

        constraints_dict = data["constraints"]

        for cmd_code in constraints_dict:
            params = self.generate_parameters(cmd_code, constraints_dict)
            print(f"Command Code: {cmd_code}, Generated Params: {params}")
