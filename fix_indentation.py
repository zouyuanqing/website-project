#!/usr/bin/env python3
"""
修复app.py中的缩进问题
"""

def fix_indentation():
    # 读取文件
    with open('app.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    in_function = False
    in_route = False
    indent_level = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # 跳过空行
        if not stripped:
            fixed_lines.append(line)
            continue
            
        # 检测函数开始
        if stripped.startswith('def ') and not line.startswith('    def'):
            in_function = True
            indent_level = 1
            fixed_lines.append('    ' + stripped + '\n')
            continue
            
        # 检测路由装饰器
        if stripped.startswith('@app.route') or stripped.startswith('@login_required'):
            in_route = True
            indent_level = 1
            fixed_lines.append('    ' + stripped + '\n')
            continue
            
        # 在函数内部
        if in_function or in_route:
            # 检测函数结束（下一个函数或路由开始）
            if (stripped.startswith('@app.route') or 
                stripped.startswith('@login_required') or 
                (stripped.startswith('def ') and not line.startswith('        '))):
                in_function = False
                in_route = True if stripped.startswith('@app.route') or stripped.startswith('@login_required') else False
                indent_level = 1
                fixed_lines.append('    ' + stripped + '\n')
                continue
                
            # 根据当前缩进级别调整
            current_indent = len(line) - len(line.lstrip())
            
            # 如果是注释，保持适当缩进
            if stripped.startswith('#'):
                if current_indent < 4:
                    fixed_lines.append('        ' + stripped + '\n')
                else:
                    fixed_lines.append(line)
                continue
                
            # 控制结构需要额外缩进
            if any(stripped.startswith(kw) for kw in ['if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except', 'finally:', 'with ']):
                if current_indent < 8:
                    fixed_lines.append('        ' + stripped + '\n')
                    indent_level = 3
                else:
                    fixed_lines.append(line)
                continue
                
            # 函数内的普通语句
            if current_indent < 8:
                fixed_lines.append('        ' + stripped + '\n')
            else:
                fixed_lines.append(line)
        else:
            # 顶级代码
            fixed_lines.append(line)
    
    # 写入修复后的文件
    with open('app_fixed.py', 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("缩进修复完成，输出到 app_fixed.py")

if __name__ == '__main__':
    fix_indentation()