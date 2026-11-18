const assert = require('node:assert/strict');
const {createHash} = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');
const resolve = require('./distribution.cjs');

test('only consumes a successful native distribution from the product repository', async t => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'product-image-'));
  t.after(() => fs.rmSync(directory, {recursive:true, force:true}));
  const bytes = Buffer.from('original distribution archive');
  const digest = 'sha256:' + createHash('sha256').update(bytes).digest('hex');
  const artifact = {name:'python-distributions',id:81,expired:false,digest,size_in_bytes:bytes.length};
  const run = {id:72,run_attempt:1,head_sha:'a'.repeat(40),status:'completed',conclusion:'success',
    repository:{full_name:'lightnow-ai/lightnow-cli',id:15},head_repository:{id:15},
    path:'.github/workflows/ci.yml',event:'pull_request'};
  const options = {context:{repo:{owner:'lightnow-ai',repo:'lightnow-cli'}},core:{setOutput(){}},
    sourceRun:'72',directory,github:{rest:{actions:{getWorkflowRun:async()=>({data:run}),
      downloadArtifact:async()=>({data:bytes})}},paginate:async()=>[artifact]}};
  for (const fields of [{head_repository:{id:16}}, {conclusion:'cancelled'}, {path:'other.yml'}]) {
    const original = {...run};
    Object.assign(run, fields);
    await assert.rejects(resolve(options), /must have succeeded/);
    Object.assign(run, original);
  }
  artifact.digest = 'sha256:' + 'f'.repeat(64);
  await assert.rejects(resolve(options), /size or digest/);
  artifact.digest = digest;
  await resolve(options);
  assert.deepEqual(fs.readFileSync(path.join(directory,'distributions.zip')), bytes);
  assert.equal(JSON.parse(fs.readFileSync(path.join(directory,'source.json'))).artifactId, 81);
});
