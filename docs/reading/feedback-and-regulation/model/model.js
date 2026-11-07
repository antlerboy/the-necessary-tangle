(function (root) {
  'use strict';
  function calculate(k, e0, tolerance, horizon) {
    if (![k, e0, tolerance, horizon].every(Number.isFinite) || k < 0 || k > 3 || tolerance < 0 || !Number.isInteger(horizon) || horizon < 0) throw new RangeError('Invalid model inputs');
    const values = Array.from({length: horizon + 1}, (_, n) => ({n, error: e0 * Math.pow(1 - k, n)}));
    const inside = values.map(p => Math.abs(p.error) <= tolerance);
    let regime;
    if (k === 0) regime = 'A nonzero error remains unchanged.';
    else if (k < 1) regime = 'A nonzero error decays without changing sign.';
    else if (k === 1) regime = 'A nonzero error reaches zero in one step.';
    else if (k < 2) regime = 'A nonzero error alternates and decays.';
    else if (k === 2) regime = 'A nonzero error alternates without decay: bounded, but not asymptotically stable.';
    else regime = 'A nonzero error alternates and grows without bound.';
    return {values, inside, regime, asymptotic: k > 0 && k < 2, allInside: inside.every(Boolean), finalInside: inside[inside.length - 1]};
  }
  const api = {calculate};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.ResponseModel = api;
})(typeof window === 'undefined' ? globalThis : window);
