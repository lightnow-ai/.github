#!/usr/bin/env bash
set -euo pipefail
cd "$DIRECTORY"
case "$GITHUB_REPOSITORY" in
  lightnow-ai/lightnow-cli) component=cli; executable=lightnow ;;
  lightnow-ai/lightnow-proxy) component=proxy; executable=lightnow-proxy ;;
  *) exit 1 ;;
esac
python3 "$ACTION_DIR/qualified_wheel.py" distributions.zip context "$component" "$ARCHIVE_SHA" >wheel.json
wheel_sha=$(jq -er .wheelSha256 wheel.json)
version=$(jq -er .packageVersion wheel.json)
repository="ghcr.io/$GITHUB_REPOSITORY"
tag="wheel-$wheel_sha"
export DOCKER_CONFIG="$DIRECTORY/auth"
mkdir -m 700 "$DOCKER_CONFIG"
printf '%s' "$GHCR_TOKEN" | docker login ghcr.io --username "$GITHUB_ACTOR" --password-stdin

# Each product serializes registry publication. Releases and repeats reuse the
# qualified image, including its recorded transitive dependencies.
digest=$(python3 "$ACTION_DIR/registry.py" "$GITHUB_REPOSITORY" "$tag")
verify_runtime() {
  local image=$1
  local options=(--rm --platform linux/amd64 --network none --read-only --cap-drop ALL --security-opt no-new-privileges)
  local labels
  labels=$(docker image inspect "$image" --format '{{json .Config.Labels}}')
  jq -e --arg wheel "$wheel_sha" --arg product "$component" --arg repo "$GITHUB_REPOSITORY" \
    '.["ai.lightnow.client.wheel.sha256"] == $wheel and .["ai.lightnow.client.component"] == $product and
     .["org.opencontainers.image.source"] == ("https://github.com/" + $repo)' <<<"$labels" >/dev/null
  docker run "${options[@]}" --tmpfs /tmp "$image" "$executable" --help >/dev/null
  docker run "${options[@]}" --workdir "/client-bundle/$component" "$image" sha256sum --check --quiet SHA256SUMS
  installed=$(docker run "${options[@]}" "$image" "/opt/$component/bin/python" -c \
    'import importlib.metadata,sys; print(importlib.metadata.version(sys.argv[1]))' "lightnow-$component")
  test "$installed" = "$version"
}
if [[ -z "$digest" ]]; then
  docker build --platform linux/amd64 --target "$component" --file "$ACTION_DIR/Dockerfile" \
    --build-arg "COMPONENT=$component" --build-arg "WHEEL_SHA256=$wheel_sha" --tag "$repository:$tag" context
  verify_runtime "$repository:$tag"
  docker push "$repository:$tag"
  digest=$(python3 "$ACTION_DIR/registry.py" "$GITHUB_REPOSITORY" "$tag")
fi
[[ "$digest" =~ ^sha256:[0-9a-f]{64}$ ]]
image="$repository@$digest"
docker pull --platform linux/amd64 "$image"
verify_runtime "$image"
lock=$(docker run --rm --network none --read-only "$image" sha256sum "/client-bundle/$component/SHA256SUMS")
jq -n --arg image "$image" --arg tag "$tag" --arg lock "${lock%% *}" --slurpfile source source.json --slurpfile wheel wheel.json \
  '$wheel[0] + {schemaVersion:"platform.lightnow.ai/client-product-image/v1", image:$image, retentionTag:$tag,
    platform:"linux/amd64", dependencyLockSha256:$lock, source:$source[0]}' >client-product-image.json
