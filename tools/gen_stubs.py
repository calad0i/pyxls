#!/usr/bin/env python3

import re
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    stubgen, outdir, gen_wrap = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
    gen_wrap = int(gen_wrap)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.check_call(
            [sys.executable, stubgen, '-m', 'raw', '-r', '-O', tmp, '-q'],
        )
        raw_dir = Path(tmp) / 'raw'
        pkg_dir = outdir / 'raw' if not gen_wrap else outdir
        pkg_dir.mkdir(exist_ok=True)
        for pyi in raw_dir.glob('*.pyi'):
            if gen_wrap and pyi.name not in ('ir_builder.pyi', 'c_api.pyi'):
                continue
            text = pyi.read_text()
            target = 'xls.raw' if not gen_wrap else 'xls'
            text = re.sub(r'(?<!(\w|\.))raw(?!\w)', target, text)
            if gen_wrap:
                (pkg_dir / f'_{pyi.name}').write_text(text)
            else:
                (pkg_dir / pyi.name).write_text(text)
    (outdir / 'py.typed').touch(exist_ok=True)


if __name__ == '__main__':
    main()
