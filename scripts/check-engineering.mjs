import { readFile, readdir } from 'node:fs/promises';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
const root = resolve(import.meta.dirname, '../public/picture-dictionary/engineering');
const base = 'https://skillworks.dev/picture-dictionary/engineering/';
const read = async name => JSON.parse(await readFile(resolve(root,name),'utf8'));
const manifest = await read('manifest.json');
const required = ['architecture','requirements','adr','work-packages','timeline','tests','deployments','monitoring-baseline','costs','risks-blockers','current-state','next-actions'];
assert.equal(manifest.schema_version,'1.0.0');
assert.equal(manifest.schema,base+'schema.json');
assert.ok(manifest.entrypoint);
for (const id of required) assert.ok(manifest.documents.some(d=>d.id===id),`Missing ${id}`);
for (const doc of manifest.documents) {
  assert.ok(!doc.path.includes('..') && !doc.path.includes('/'));
  assert.equal(doc.url,base+doc.path);
  assert.ok(doc.version && doc.status && Number.isFinite(Date.parse(doc.updated_at)));
  const content = await readFile(resolve(root,doc.path),'utf8');
  if (!doc.path.endsWith('.json')) continue;
  const value=JSON.parse(content);
  assert.equal(value.schema_version,'1.0.0');
  assert.equal(value.project,'picture-dictionary-kids');
  assert.ok(value.status && Number.isFinite(Date.parse(value.updated_at)));
  assert.equal(doc.updated_at,value.updated_at,`Stale manifest: ${doc.id}`);
  assert.equal(doc.status,value.status,`Stale status: ${doc.id}`);
}
const lines=(await readFile(resolve(root,'timeline.jsonl'),'utf8')).trim().split('\n');
let previous=0;
for(const line of lines) {
  const event=JSON.parse(line);
  for(const field of ['at','agent','operation','files','commit','basis','result','test_evidence','failures','unverified_assumptions','rollback']) assert.ok(field in event,`Missing event field: ${field}`);
  const at=Date.parse(event.at);assert.ok(at>=previous);previous=at;
  assert.ok(event.at.endsWith('Z'),'Timeline must use UTC');
}
for(const file of await readdir(root)) {
  const content=await readFile(resolve(root,file),'utf8');
  assert.ok(!/sk-(?:proj-)?[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|Bearer\s+[A-Za-z0-9._-]{20,}|postgres(?:ql)?:\/\//.test(content),`Possible credential in ${file}`);
}
console.log(`Engineering records validated: ${manifest.documents.length} documents, ${lines.length} events`);
