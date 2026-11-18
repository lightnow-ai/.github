"""Extract the qualified product wheel from the original distribution archive."""
import argparse
import hashlib
import json
import re
from email.parser import BytesParser
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile


def extract(archive, destination, component, distribution_digest):
    if component not in ('cli', 'proxy'):
        raise ValueError('Unsupported client')
    raw = archive.read_bytes()
    if hashlib.sha256(raw).hexdigest() != distribution_digest:
        raise ValueError('Distribution artifact digest mismatch')
    package = 'lightnow_' + component
    with ZipFile(BytesIO(raw)) as dist:
        wheels = [item for item in dist.infolist() if item.filename.endswith('.whl')]
        if len(wheels) != 1:
            raise ValueError('Expected one product wheel')
        info = wheels[0]
        match = re.fullmatch(package + r'-([A-Za-z0-9_.!+]+)-py3-none-any\.whl', info.filename)
        if not match or info.file_size > 32 * 1024 * 1024:
            raise ValueError('Unexpected wheel filename or size')
        data = dist.read(info)
    version = match[1]
    with ZipFile(BytesIO(data)) as wheel:
        metadata = [item for item in wheel.infolist() if item.filename.endswith('.dist-info/METADATA')]
        if len(metadata) != 1 or metadata[0].filename != f'{package}-{version}.dist-info/METADATA' or metadata[0].file_size > 1024 * 1024:
            raise ValueError('Unexpected wheel metadata')
        fields = BytesParser().parsebytes(wheel.read(metadata[0]))
        if fields.get_all('Name') != ['lightnow-' + component] or fields.get_all('Version') != [version]:
            raise ValueError('Product or version mismatch')
    destination.mkdir()
    (destination / info.filename).write_bytes(data)
    return {'component': component, 'packageVersion': version, 'filename': info.filename,
            'wheelSha256': hashlib.sha256(data).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('archive', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('component')
    parser.add_argument('distribution_digest')
    args = parser.parse_args()
    print(json.dumps(extract(args.archive, args.destination, args.component, args.distribution_digest)))
