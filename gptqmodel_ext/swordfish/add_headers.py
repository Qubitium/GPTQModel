import os, re
from pathlib import Path

header = '''// SPDX-FileCopyrightText: 2026 AlpinDale and the dphnAI/sonar contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
//
// Swordfish: Blackwell (sm100/sm110) weight-quantized GEMM kernels.
// Vendored from https://github.com/dphnAI/sonar and used under the terms of
// the GNU Affero General Public License v3.0 or later. See LICENSE in this
// directory or /licenses/SWORDFISH at the project root for the full license.
//
'''

root = Path(__file__).parent
for path in root.rglob('*'):
    if path.is_dir() or path.name in {'LICENSE', 'add_headers.py'}:
        continue
    if path.suffix not in {'.cu', '.cuh', '.h', '.hpp', '.cpp'}:
        continue
    text = path.read_text()
    if 'SPDX-License-Identifier: AGPL' in text:
        continue
    # Preserve #pragma once or first comment line
    if text.startswith('#pragma once'):
        new_text = header + text
    elif text.startswith('//'):
        # append after first contiguous block of // comments? simpler: prepend
        new_text = header + text
    elif text.startswith('/*'):
        # insert before
        new_text = header + text
    else:
        new_text = header + text
    path.write_text(new_text)
    print('tagged', path)
