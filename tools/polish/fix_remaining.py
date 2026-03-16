#!/usr/bin/env python3
"""Fix remaining light-mode class remnants in 10 specific pages."""
import re, os

TARGETS = [
    'apps/web/src/pages/AiriaEverywhereHub.tsx',
    'apps/web/src/pages/AuditLog.tsx',
    'apps/web/src/pages/CloseCalendar.tsx',
    'apps/web/src/pages/Connectors.tsx',
    'apps/web/src/pages/Dashboard.tsx',
    'apps/web/src/pages/GradientAIDashboard.tsx',
    'apps/web/src/pages/MultimodalStoryteller.tsx',
    'apps/web/src/pages/RaceControl.tsx',
    'apps/web/src/pages/Settings.tsx',
    'apps/web/src/pages/UINavigator.tsx',
]

REPLACEMENTS = [
    (r'bg-indigo-50\b', 'bg-[#111118]'),
    (r'border-indigo-200\b', 'border-[#2A2A3A]'),
    (r'text-blue-300\b', 'text-blue-400'),
    (r'text-indigo-600\b', 'text-blue-400'),
    (r'bg-gray-50\b', 'bg-[#1A1A24]'),
    (r'bg-white\b', 'bg-[#111118]'),
    (r'text-gray-800\b', 'text-gray-200'),
    (r'bg-gray-100\b', 'bg-[#1A1A24]'),
    (r'hover:bg-gray-50\b', 'hover:bg-[#1A1A24]'),
]

for path in TARGETS:
    if not os.path.exists(path):
        print(f'SKIP (not found): {path}')
        continue
    with open(path) as f:
        content = f.read()
    original = content
    for pattern, replacement in REPLACEMENTS:
        content = re.sub(pattern, replacement, content)
    if content != original:
        with open(path, 'w') as f:
            f.write(content)
        print(f'FIXED: {path}')
    else:
        print(f'CLEAN: {path}')

print('Done.')
