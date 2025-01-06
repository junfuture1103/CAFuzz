import os
import json
import random
import string

def generate_random_string(prefix, max_len):
    """
    prefix 붙은 문자열을 생성하고, prefix 포함 최대 길이를 넘지 않는 랜덤 문자열을 반환한다.
    """
    # prefix 길이를 제외한 나머지 부분에서 사용할 수 있는 최대 길이 계산
    remaining_len = max_len - len(prefix)
    # 사용 가능한 문자는 알파벳, 숫자, 밑줄 등 자유롭게 가정
    chars = string.ascii_letters + string.digits + "_"
    # remaining_len 범위 내에서 임의의 길이를 선정하여 문자열 생성
    random_length = random.randint(1, remaining_len) if remaining_len > 0 else 0
    suffix = "".join(random.choice(chars) for _ in range(random_length))
    return prefix + suffix

def generate_random_value(param_def):
    """
    파라미터 정의(param_def)를 보고 그에 맞는 랜덤 값을 생성한다.
    """
    param_type = param_def["type"]
    
    if param_type == "enum":
        # possible_values에서 랜덤 선택
        return random.choice(param_def["possible_values"])
    
    elif param_type == "enum_string":
        # 문자열 후보에서 랜덤 선택
        return random.choice(param_def["possible_values"])
    
    elif param_type == "range":
        # 범위 내 랜덤 정수
        return random.randint(param_def["min"], param_def["max"])
    
    elif param_type == "string":
        # prefix와 길이 제한이 있음
        prefix = param_def.get("prefix", "")
        max_len = param_def.get("max_len", 20)
        return generate_random_string(prefix, max_len)
    
    else:
        # 그 외 타입은 정의되지 않았다고 가정
        return None

def generate_parameters(command_code, constraints_dict):
    """
    특정 command_code에 대한 파라미터 목록을 생성하여 반환한다.
    """
    if command_code not in constraints_dict:
        return []
    
    param_defs = constraints_dict[command_code]["params"]
    generated_params = []
    for pdef in param_defs:
        generated_params.append(generate_random_value(pdef))
    
    return generated_params

def main():
    # 현재 스크립트의 디렉토리 위치를 기준으로 경로를 생성
    script_path = os.path.abspath(__file__)            # 현재 파이썬 파일의 절대 경로
    script_dir = os.path.dirname(script_path)          # 디렉토리 경로 추출

    dictionary_name = "CFE_ES.json"
    file_name = os.path.join(script_dir, "dictionarys", dictionary_name)

    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    constraints_dict = data["constraints"]
    
    # 예시: 모든 command_code에 대해 파라미터를 생성해본다
    for cmd_code in constraints_dict:
        params = generate_parameters(cmd_code, constraints_dict)
        print(f"Command Code: {cmd_code}, Generated Params: {params}")

if __name__ == "__main__":
    main()
