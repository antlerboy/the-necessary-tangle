"""Restore reviewed 0.42 inputs after platform-dependent historical rebuilding."""
import math

# Exact coordinates from the reviewed public candidate at 3c35fe1.
REVIEWED_COORDINATES = {'person_fpcs_a_cobham': {'y': -0.9387390654767223}, 'person_fpcs_c_reynolds': {'y': 0.5625993894710698}, 'person_fpcs_d_m_raup': {'y': -0.38087823430893253}, 'person_fpcs_j_a_wheeler': {'y': 0.09976197526300373}, 'person_fpcs_m_j_feigenbaum': {'x': -0.9774656349169486}, 'person_fpcs_m_kimura': {'y': -0.4158866646748052}, 'person_fpcs_s_bowles': {'y': 0.6921719587045205}, 'person_fpcs_w_fontana': {'y': 1.1285104307758118}, 'publication_fpcs_024': {'y': -0.8887005768508881}, 'publication_fpcs_030': {'y': -0.3512994231491119}, 'publication_fpcs_058': {'x': -0.925443510633127}, 'publication_fpcs_065': {'y': 0.40968661679220464}, 'publication_fpcs_070': {'y': 0.3606298055769115}}
EVIDENCE_IDS = (
    'ev41_feedback_maxwell_dynamics',
    'ev41_feedback_rwb_usage',
    'ev41_feedback_ashby_usage',
    'ev41_regulation_ashby_scope',
)


def restore_reviewed_baseline(data):
    """Restore only the observed last-bit coordinates and four evidence positions."""
    nodes = data['nodes']
    replacements = []
    for ident, coordinates in REVIEWED_COORDINATES.items():
        matches = [row for row in nodes if row.get('id') == ident]
        if len(matches) != 1:
            raise ValueError('Expected one reviewed node: ' + ident)
        row = matches[0]
        for field, reviewed in coordinates.items():
            value = row.get(field)
            if type(value) is not float or not math.isfinite(value) or abs(value-reviewed) > 1e-14:
                raise ValueError('Unexpected reviewed coordinate: ' + ident + ' ' + field)
            replacements.append((row, field, reviewed))

    evidence = data['evidence']
    positions = [i for i, row in enumerate(evidence) if row.get('id') in EVIDENCE_IDS]
    if positions not in ([37, 38, 39, 40], [206, 207, 208, 209]):
        raise ValueError('Unexpected 0.41 evidence positions or duplicates')
    selected = [evidence[i] for i in positions]
    if tuple(row.get('id') for row in selected) != EVIDENCE_IDS:
        raise ValueError('Unexpected 0.41 evidence identities or order')
    if any(row.get('connection_pass') != 'feedback_regulation_20261107' for row in selected):
        raise ValueError('Unexpected 0.41 evidence provenance')
    remaining = [row for i, row in enumerate(evidence) if i not in positions]
    if len(remaining) < 38 or remaining[36].get('id') != 'ev_wiener_feedback_cybernetics' or remaining[37].get('id') != 'ev29_weaver-conditions-on-averages':
        raise ValueError('Unexpected neighbouring evidence records')

    for row, field, reviewed in replacements:
        row[field] = reviewed
    data['evidence'] = remaining[:37] + selected + remaining[37:]
