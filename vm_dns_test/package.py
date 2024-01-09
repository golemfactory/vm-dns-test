import base64
import json

from yapapi.payload.manifest import Manifest
from yapapi.payload import vm
from yapapi.payload.package import resolve_package_url
from yapapi.payload.vm import DEFAULT_REPOSITORY_URL

IMAGE_TAG = "blueshade/vm-dns-test:latest"

async def get_package():
    resolved_package = await resolve_package_url(
        DEFAULT_REPOSITORY_URL, image_tag=IMAGE_TAG
    )
    img_hash = resolved_package.split(":")[2]
    manifest_obj = await Manifest.generate(img_hash, ["https://pypi.dev.golem.network"])
    manifest = json.dumps(manifest_obj.dict(by_alias=True))
    encoded_manifest = base64.b64encode(manifest.encode("utf-8")).decode("ascii")
    return await vm.manifest(encoded_manifest, capabilities=["vpn", "inet", "manifest-support"])
