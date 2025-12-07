import json
import random
import string
import os
import argparse

def rand_string(length=None):
    """生成隨機字串，長度較短以便AFL++變異"""
    if length is None:
        length = random.randint(1, 5)  # 縮短長度
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def rand_value(depth=0):
    """生成隨機值，限制深度避免過於複雜"""
    if depth > 2:  # 降低最大深度從3到2
        return random.choice([1, "x", True, None, ""])
    
    # 增加基本類型的機率，降低複雜結構
    t = random.choices(
        ["obj", "array", "str", "num", "bool", "null"],
        weights=[1, 1, 3, 3, 2, 1]  # 字串和數字的權重較高
    )[0]
    
    if t == "obj":
        # 減少物件大小
        return {rand_string(): rand_value(depth+1) for _ in range(random.randint(1, 2))}
    if t == "array":
        # 減少陣列大小
        return [rand_value(depth+1) for _ in range(random.randint(1, 3))]
    if t == "str":
        return rand_string()
    if t == "num":
        return random.randint(-10, 100)
    if t == "bool":
        return random.choice([True, False])
    if t == "null":
        return None

def generate_large_nested_objects():
    """生成大型巢狀物件測試案例"""
    cases = []
    
    # Case 1: 簡單的超長字串值
    cases.append({"A": "A" * 10000})
    cases.append({"A": "A" * 50000})
    cases.append({"A": "A" * 100000})
    
    # Case 2: 巢狀物件中的超長字串值
    cases.append({"meta": {"mode": "debug"}, "data": {"value": "B" * 10000}})
    cases.append({"meta": {"mode": "debug"}, "data": {"value": "B" * 50000}})
    cases.append({"meta": {"mode": "debug"}, "data": {"value": "B" * 100000}})
    
    # Case 3: 多個巢狀層級，每層都有大字串
    cases.append({
        "level1": {
            "level2": {
                "level3": {
                    "data": "C" * 10000
                }
            }
        }
    })
    
    # Case 4: 多個鍵值對，每個值都很大
    cases.append({
        "field1": "D" * 5000,
        "field2": "E" * 5000,
        "field3": "F" * 5000
    })
    
    # Case 5: 巢狀物件加上多個大字串欄位
    cases.append({
        "meta": {
            "mode": "debug",
            "config": "G" * 10000
        },
        "data": {
            "value": "H" * 10000,
            "extra": "I" * 10000
        }
    })
    
    # Case 6: 深度巢狀加上大字串
    obj = {"data": "J" * 10000}
    for i in range(10):
        obj = {"level": obj}
    cases.append(obj)
    
    # Case 7: 陣列中包含大字串
    cases.append({"items": ["K" * 10000, "L" * 10000]})
    
    # Case 8: 混合巢狀結構
    cases.append({
        "config": {
            "settings": {
                "options": ["M" * 5000, "N" * 5000]
            }
        },
        "payload": "O" * 20000
    })
    
    return cases

def generate_edge_case_seeds():
    """生成邊界案例和特殊測試案例"""
    return [
        {},  # 空物件
        [],  # 空陣列
        {"a": 1},  # 最簡單的物件
        [1],  # 最簡單的陣列
        "",  # 空字串
        "a",  # 單字元
        0,  # 零
        -1,  # 負數
        True,  # 布林值
        False,
        None,  # null
        {"": ""},  # 空鍵值
        [[[]]],  # 巢狀陣列
        {"a": {"b": {"c": 1}}},  # 巢狀物件
        [1, "a", True, None],  # 混合類型
        {"meta": {"mode": "debug"}, "data": {"value": "BOOM"}},  # 雙層巢狀物件
    ]

def generate_malformed_json_seeds():
    """生成畸形/錯誤的 JSON（原始字串，不使用 json.dump）"""
    return [
        # 括號不匹配
        '{"a": 1',
        '{"a": 1}}',
        '[1, 2',
        '[1, 2]]',
        
        # 逗號問題
        '{"a": 1,}',
        '[1, 2,]',
        '{"a": 1, "b": 2,}',
        '{"a":, "b": 1}',
        
        # 引號問題
        "{'a': 1}",  # 單引號
        '{"a": \'b\'}',
        '{"a: 1}',  # 缺少引號
        '{a: 1}',
        
        # 特殊值
        '{"a": undefined}',
        '{"a": NaN}',
        '{"a": Infinity}',
        '{"a": -Infinity}',
        
        # 控制字元和特殊字元
        '{"a": "\x00"}',
        '{"a": "\n\r\t"}',
        '{"\\": 1}',
        
        # Unicode 問題
        '{"a": "\\uDEAD"}',  # 無效的 surrogate pair
        '{"a": "\\u123"}',  # 不完整的 unicode
        
        # 深度巢狀（可能觸發 stack overflow）
        '[' * 100 + ']' * 100,
        '{' * 50 + '"a":1' + '}' * 50,
        
        # 超長字串
        '{"a": "' + 'x' * 10000 + '"}',
        
        # 重複的鍵
        '{"a": 1, "a": 2}',
        
        # 空白和格式問題
        '',
        ' ',
        '\n',
        '   {}   ',
        
        # 數字格式錯誤
        '{"a": 01}',  # 前導零
        '{"a": .5}',  # 沒有前導零
        '{"a": 1.}',  # 沒有小數部分
        '{"a": +1}',  # 正號
        '{"a": 0x10}',  # 十六進位
        
        # 其他格式錯誤
        'null null',
        '{"a": "b" "c"}',
        '[1 2]',
        '{"a"}',
    ]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='生成AFL++的JSON測試種子檔案')
    parser.add_argument('-n', '--num', type=int, default=50, 
                        help='要生成的種子檔案數量 (預設: 50)')
    parser.add_argument('--simple', action='store_true',
                        help='只生成簡單的邊界案例種子（忽略 -n 參數）')
    parser.add_argument('--malformed', action='store_true',
                        help='包含畸形/錯誤的 JSON 種子')
    parser.add_argument('--large', action='store_true',
                        help='生成大型測資（巢狀物件與長字串）')
    args = parser.parse_args()
    
    os.makedirs("seeds", exist_ok=True)
    
    if args.large:
        # 生成大型測資
        large_cases = generate_large_nested_objects()
        print(f"正在生成 {len(large_cases)} 個大型測資種子檔案...")
        for i, case in enumerate(large_cases):
            with open(f"seeds/large_{i}.json", "w") as f:
                json.dump(case, f)
        print(f"完成！已生成 {len(large_cases)} 個大型測資種子檔案至 seeds/ 目錄")
    elif args.simple:
        # 只生成邊界案例
        edge_cases = generate_edge_case_seeds()
        print(f"正在生成 {len(edge_cases)} 個邊界案例種子檔案...")
        for i, case in enumerate(edge_cases):
            with open(f"seeds/edge_{i}.json", "w") as f:
                json.dump(case, f)
        print(f"完成！已生成 {len(edge_cases)} 個邊界案例種子檔案至 seeds/ 目錄")
    else:
        # 收集所有種子
        edge_cases = generate_edge_case_seeds()
        malformed_cases = generate_malformed_json_seeds() if args.malformed else []
        
        num_edge = len(edge_cases)
        num_malformed = len(malformed_cases)
        num_random = max(0, args.num - num_edge - num_malformed)
        
        print(f"正在生成種子檔案...")
        print(f"  - {num_edge} 個邊界案例（有效 JSON）")
        if args.malformed:
            print(f"  - {num_malformed} 個畸形案例（無效 JSON）")
        print(f"  - {num_random} 個隨機案例（有效 JSON）")
        
        idx = 0
        
        # 先生成邊界案例（有效 JSON）
        for i, case in enumerate(edge_cases):
            with open(f"seeds/{idx:04d}.json", "w") as f:
                json.dump(case, f)
            idx += 1
        
        # 生成畸形案例（直接寫入字串）
        if args.malformed:
            for i, case in enumerate(malformed_cases):
                with open(f"seeds/{idx:04d}.json", "w") as f:
                    f.write(case)
                idx += 1
        
        # 再生成隨機案例（有效 JSON）
        for i in range(num_random):
            with open(f"seeds/{idx:04d}.json", "w") as f:
                json.dump(rand_value(), f)
            idx += 1
        
        total = num_edge + num_malformed + num_random
        print(f"完成！已生成 {total} 個種子檔案至 seeds/ 目錄")
