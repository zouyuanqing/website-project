#!/usr/bin/env python3
# 缩进修复脚本

# 读取破损的文件
with open('app_broken.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 手动修复关键部分的缩进
# 这是一个简化的修复，主要确保create_app函数能正常工作

# 找到create_app函数开始位置
lines = content.split('\n')
fixed_lines = []
inside_create_app = False
current_route_func = None

for i, line in enumerate(lines):
    stripped = line.strip()
    
    if 'def create_app():' in line:
        inside_create_app = True
        fixed_lines.append(line)
        continue
    
    if not inside_create_app:
        fixed_lines.append(line)
        continue
    
    # 在create_app内部
    if stripped == '':
        fixed_lines.append('')
        continue
        
    if stripped.startswith('from ') or stripped.startswith('import '):
        fixed_lines.append('    ' + stripped)
        continue
        
    if stripped.startswith('# '):
        fixed_lines.append('    ' + stripped)
        continue
        
    if stripped.startswith('app =') or stripped.startswith('app.config') or stripped.startswith('db.init_app') or stripped.startswith('login_manager') or stripped.startswith('upload_dir') or stripped.startswith('os.makedirs'):
        fixed_lines.append('    ' + stripped)
        continue
        
    if stripped.startswith('@login_manager.user_loader'):
        fixed_lines.append('    ' + stripped)
        current_route_func = 'user_loader'
        continue
        
    if stripped.startswith('@app.before_request'):
        fixed_lines.append('    ' + stripped)
        current_route_func = 'before_request'
        continue
        
    if stripped.startswith('@app.route'):
        fixed_lines.append('    ' + stripped)
        current_route_func = 'route'
        continue
        
    if stripped.startswith('@login_required'):
        fixed_lines.append('    ' + stripped)
        continue
        
    if stripped.startswith('def '):
        if current_route_func:
            fixed_lines.append('    ' + stripped)
            current_route_func = 'in_function'
        else:
            fixed_lines.append('    ' + stripped)
        continue
        
    if stripped.startswith('return app'):
        fixed_lines.append('    ' + stripped)
        inside_create_app = False
        continue
        
    # 函数内部的代码
    if current_route_func == 'in_function' and stripped:
        fixed_lines.append('        ' + stripped)
        continue
        
    # 其他在create_app内的代码
    if stripped:
        if line.startswith('    '):
            # 已经有4空格缩进的保持
            fixed_lines.append(line)
        elif line.startswith('        '):
            # 已经有8空格缩进的保持
            fixed_lines.append(line) 
        else:
            # 需要4空格缩进
            fixed_lines.append('    ' + stripped)
    else:
        fixed_lines.append('')

# 写入修复后的文件
with open('app.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(fixed_lines))

print("缩进修复完成")