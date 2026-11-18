"""Resolve a GHCR image tag. Only a registry-confirmed missing manifest permits a build."""
import base64
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


def resolve(repository, tag):
    if repository not in ('lightnow-ai/lightnow-cli', 'lightnow-ai/lightnow-proxy'):
        raise ValueError('Unexpected image repository')
    basic = base64.b64encode((os.environ['GITHUB_ACTOR'] + ':' + os.environ['GHCR_TOKEN']).encode()).decode()
    query = urllib.parse.urlencode({'service': 'ghcr.io', 'scope': 'repository:' + repository + ':pull'})
    token_request = urllib.request.Request('https://ghcr.io/token?' + query, headers={'Authorization': 'Basic ' + basic})
    with urllib.request.urlopen(token_request, timeout=30) as response:
        token = json.load(response)['token']
    types = ['application/vnd.oci.image.manifest.v1+json', 'application/vnd.oci.image.index.v1+json',
             'application/vnd.docker.distribution.manifest.v2+json', 'application/vnd.docker.distribution.manifest.list.v2+json']
    request = urllib.request.Request('https://ghcr.io/v2/' + repository + '/manifests/' + tag,
                                     headers={'Authorization': 'Bearer ' + token, 'Accept': ', '.join(types)})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            digest = 'sha256:' + hashlib.sha256(response.read()).hexdigest()
            if digest != response.headers['Docker-Content-Digest']:
                raise ValueError('Registry manifest digest mismatch')
            return digest
    except urllib.error.HTTPError as err:
        if err.code == 404 and any(item.get('code') in ('MANIFEST_UNKNOWN', 'NAME_UNKNOWN')
                                   for item in json.load(err).get('errors', [])):
            return ''
        raise


if __name__ == '__main__':
    print(resolve(sys.argv[1], sys.argv[2]))
