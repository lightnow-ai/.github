import hashlib
import io
from pathlib import Path
import tempfile
import unittest
import zipfile

from qualified_wheel import extract


class QualifiedWheel(unittest.TestCase):
    def test_verify_and_extract_only_qualified_component(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            wheel = io.BytesIO()
            with zipfile.ZipFile(wheel, 'w') as package:
                package.writestr('lightnow_cli-1.2.3.dist-info/METADATA', 'Name: lightnow-cli\nVersion: 1.2.3\n')
            archive = root / 'dist.zip'
            with zipfile.ZipFile(archive, 'w') as dist:
                dist.writestr('lightnow_cli-1.2.3-py3-none-any.whl', wheel.getvalue())
                dist.writestr('irrelevant.tar.gz', b'ignored')
            digest = hashlib.sha256(archive.read_bytes()).hexdigest()
            with self.assertRaises(ValueError):
                extract(archive, root / 'wrong-hash', 'cli', '0' * 64)
            with self.assertRaises(ValueError):
                extract(archive, root / 'wrong-product', 'proxy', digest)
            result = extract(archive, root / 'context', 'cli', digest)
            self.assertEqual(result['wheelSha256'], hashlib.sha256(wheel.getvalue()).hexdigest())
            self.assertEqual(list((root / 'context').iterdir()), [root / 'context' / result['filename']])
