/* Recorded prerequisites and their evidence; no relationships are inferred. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else {
    root.TANGLE_DEPENDENCY_MODEL = api;
    if (root.TANGLE_DATA) root.TANGLE_DEPENDENCIES = api.create(root.TANGLE_DATA);
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const withdrawn = new Set(['rejected', 'superseded', 'legacy_unresolved']);
  const truth = (value) => value === true || value === 'true' || value === 'yes';
  const unpack = (value) => {
    if (Array.isArray(value)) return value;
    try { const parsed = JSON.parse(value || '[]'); return Array.isArray(parsed) ? parsed : []; }
    catch (_) { return []; }
  };
  function create(data) {
    const redirects = data.canonical_redirects || {};
    const canonical = (id) => {
      const seen = new Set();
      while (redirects[id] && !seen.has(id)) { seen.add(id); id = redirects[id]; }
      return id;
    };
    const nodes = new Map((data.nodes || []).filter((node) => node.public_visibility === 'public'
      && canonical(node.id) === node.id).map((node) => [node.id, node]));
    const types = new Map((data.relation_types || []).map((row) => [row.relation_type, row]));
    const strict = new Set([...types.values()].filter((row) => truth(row.strict_dependency)).map((row) => row.relation_type));
    const edges = (data.edges || []).map((edge) => ({ ...edge, source: canonical(edge.source), target: canonical(edge.target) }))
      .filter((edge) => nodes.has(edge.source) && nodes.has(edge.target) && edge.source !== edge.target);
    const incoming = new Map(), outgoing = new Map();
    for (const edge of edges) {
      if (!incoming.has(edge.target)) incoming.set(edge.target, []);
      if (!outgoing.has(edge.source)) outgoing.set(edge.source, []);
      incoming.get(edge.target).push(edge); outgoing.get(edge.source).push(edge);
    }
    const necessary = (edge) => strict.has(edge.relation_type) && !withdrawn.has(edge.claim_status);
    function direct(id) {
      id = canonical(id);
      return {
        predecessors: [...new Set((incoming.get(id) || []).filter(necessary).map((edge) => edge.source))],
        dependents: [...new Set((outgoing.get(id) || []).filter(necessary).map((edge) => edge.target))],
      };
    }
    function trace(id, side, depth = 1) {
      id = canonical(id); depth = Math.max(1, Math.min(3, Math.floor(Number(depth)) || 1));
      const groups = new Map(), cycles = [];
      const queue = [{ id, path: [], seen: new Set([id]) }];
      let steps = 0;
      while (queue.length && steps++ < 10000) {
        const state = queue.shift();
        if (state.path.length >= depth) continue;
        const candidates = (side === 'predecessors' ? incoming.get(state.id) : outgoing.get(state.id)) || [];
        for (const edge of candidates.filter(necessary)) {
          const next = side === 'predecessors' ? edge.source : edge.target;
          const path = [...state.path, edge];
          if (state.seen.has(next)) { cycles.push(path); continue; }
          if (!groups.has(next)) groups.set(next, { node: nodes.get(next), distance: path.length, paths: [] });
          const group = groups.get(next);
          group.distance = Math.min(group.distance, path.length);
          const key = path.map((claim) => claim.id).join('|');
          if (group.paths.length < 10 && !group.paths.some((prior) => prior.map((claim) => claim.id).join('|') === key)) group.paths.push(path);
          queue.push({ id: next, path, seen: new Set([...state.seen, next]) });
        }
      }
      return { entries: [...groups.values()].sort((a, b) => a.distance - b.distance || a.node.label.localeCompare(b.node.label)), cycles, truncated: queue.length > 0 };
    }
    function related(id) {
      id = canonical(id); const groups = new Map();
      for (const edge of [...(incoming.get(id) || []), ...(outgoing.get(id) || [])]) {
        const other = edge.source === id ? edge.target : edge.source;
        if (!groups.has(other)) groups.set(other, { node: nodes.get(other), edges: [] });
        if (!groups.get(other).edges.some((prior) => prior.id === edge.id)) groups.get(other).edges.push(edge);
      }
      return [...groups.values()].sort((a, b) => a.node.label.localeCompare(b.node.label));
    }
    return { nodes, edges, types, canonical, strict, necessary, direct, trace, related, unpack,
      sources: new Map((data.sources || []).map((row) => [row.id, row])),
      evidence: new Map((data.evidence || []).map((row) => [row.id, row])),
      profiles: new Map((data.profiles || []).map((row) => [canonical(row.node_id), row])),
    };
  }
  return { create, unpack };
});
