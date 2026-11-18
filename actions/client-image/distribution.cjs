const fs = require('node:fs');
const path = require('node:path');
const {createHash} = require('node:crypto');

module.exports = async ({github, context, core, sourceRun, directory}) => {
  const {owner, repo} = context.repo;
  if (owner !== 'lightnow-ai' || !['lightnow-cli', 'lightnow-proxy'].includes(repo) ||
      !/^[1-9][0-9]*$/.test(sourceRun) || !Number.isSafeInteger(Number(sourceRun))) {
    throw new Error('Unexpected product or source run');
  }
  const request = {owner, repo, run_id: Number(sourceRun)};
  const {data: run} = await github.rest.actions.getWorkflowRun(request);
  const ci = run.path === '.github/workflows/ci.yml' &&
    (run.event === 'pull_request' || (run.event === 'push' && run.head_branch === 'main'));
  const release = run.path === '.github/workflows/release.yml' && run.event === 'push' &&
    /^v[0-9]+\.[0-9]+\.[0-9]+/.test(run.head_branch);
  if (run.repository.full_name !== owner + '/' + repo || run.head_repository?.id !== run.repository.id ||
      run.status !== 'completed' || run.conclusion !== 'success' || !(ci || release)) {
    throw new Error('The product CI or release must have succeeded for this repository');
  }
  const artifacts = await github.paginate(github.rest.actions.listWorkflowRunArtifacts, {...request, per_page: 50});
  const matches = artifacts.filter(a => a.name === 'python-distributions' && !a.expired);
  if (matches.length !== 1 || !/^sha256:[a-f0-9]{64}$/.test(matches[0].digest) ||
      matches[0].size_in_bytes > 64 * 1024 * 1024) {
    throw new Error('Expected one retained python-distributions artifact with a native digest');
  }
  const a = matches[0];
  const download = await github.rest.actions.downloadArtifact({owner, repo, artifact_id: a.id, archive_format: 'zip'});
  const bytes = Buffer.from(download.data);
  if (bytes.length !== a.size_in_bytes || 'sha256:' + createHash('sha256').update(bytes).digest('hex') !== a.digest) {
    throw new Error('Original source archive size or digest differs');
  }
  fs.writeFileSync(path.join(directory, 'distributions.zip'), bytes, {flag:'wx'});
  fs.writeFileSync(path.join(directory, 'source.json'), JSON.stringify({
    repository: owner + '/' + repo, runId: run.id, runAttempt: run.run_attempt,
    revision: run.head_sha, artifactId: a.id, artifactSha256: a.digest.slice(7)
  }), {flag:'wx'});
  core.setOutput('artifact-sha', a.digest.slice(7));
};
