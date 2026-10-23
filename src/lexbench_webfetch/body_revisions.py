"""Derive revised body scopes from exact frozen references without copying captures."""
from copy import deepcopy
import hashlib
import re

from .body_coverage import tokens


def _binding(text):
    return {'sha256': hashlib.sha256(text.encode()).hexdigest(), 'chars': len(text)}


def project_body_reference(case, projection, expected_source_sha256):
    """Apply reviewed character ranges, verifying their materialized text at export."""
    original = case.get('body_requirements')
    version = original.get('version') if isinstance(original, dict) else None
    projection_fields = {'source_sha256', 'source_chars', 'regions'}
    if version in (4, 5):
        projection_fields.add('ending')
    if (not isinstance(original, dict) or version not in (3, 4, 5)
            or not isinstance(projection, dict)
            or set(projection) != projection_fields
            or (version == 3 and 'ending' in original)
            or not isinstance(expected_source_sha256, str)
            or not re.fullmatch('[0-9a-f]{64}', expected_source_sha256)
            or projection['source_sha256'] != expected_source_sha256
            or type(projection['source_chars']) is not int or projection['source_chars'] < 6
            or not isinstance(projection['regions'], list)
            or not 1 <= len(projection['regions']) <= 5):
        raise ValueError('Invalid body reference projection')
    source = case.get('ground_truth_main_content')
    if source is not None and (not isinstance(source, str) or
            _binding(source) != {'sha256': expected_source_sha256, 'chars': projection['source_chars']}):
        raise ValueError('Body projection source differs from frozen reference')

    def materialize(row, region=False):
        fields = {'start', 'end', 'text_binding'}
        if region:
            fields |= {'id', 'label', 'source_text_binding'}
        if (not isinstance(row, dict) or set(row) != fields
                or type(row['start']) is not int or type(row['end']) is not int
                or not 0 <= row['start'] < row['end'] <= projection['source_chars']):
            raise ValueError('Invalid body projection range')
        keys = ('text', 'source_text') if region else ('text',)
        for key in keys:
            binding = row[key + '_binding']
            if (not isinstance(binding, dict) or set(binding) != {'sha256', 'chars'}
                    or not isinstance(binding['sha256'], str)
                    or not re.fullmatch('[0-9a-f]{64}', binding['sha256'])
                    or type(binding['chars']) is not int or binding['chars'] < 1):
                raise ValueError('Invalid body projection text binding')
        result = {'source_char_range': [row['start'], row['end']]}
        if region:
            if any(not isinstance(row[k], str) or not row[k].strip() for k in ('id', 'label')):
                raise ValueError('Body projection regions need an identity and label')
            result.update(id=row['id'], label=row['label'],
                          segmentation_method='reviewed_frozen_source_ranges')
        if source is None:
            result.update({key + '_binding': deepcopy(row[key + '_binding']) for key in keys})
        else:
            text = source[row['start']:row['end']].strip()
            values = {'text': ' '.join(tokens(text)), 'source_text': text} if region else {'text': text}
            for key, text in values.items():
                if _binding(text) != row[key + '_binding']:
                    raise ValueError('Body projection text differs from reviewed binding')
                result[key] = text
        return result

    regions = [materialize(row, True) for row in projection['regions']]
    if (len({r['id'] for r in regions}) != len(regions)
            or any(a['end'] > b['start'] for a, b in zip(projection['regions'], projection['regions'][1:]))):
        raise ValueError('Body projection regions must be unique, ordered and nonoverlapping')
    ending = None
    if version in (4, 5):
        ending = materialize(projection['ending'])
        if not any(r['start'] <= projection['ending']['start'] < projection['ending']['end'] <= r['end']
                   for r in projection['regions']):
            raise ValueError('Body projection ending must belong to a retained region')
    body = deepcopy(original)
    body.update(version=3 if version == 3 else 5, regions=regions,
                minimum_region_passes=len(regions), minimum_floor=body['minimum_coverage'],
                segmentation_method='reviewed_frozen_source_ranges',
                reference_projection={'source_sha256': expected_source_sha256,
                                      'source_chars': projection['source_chars']})
    if ending is not None:
        body['ending'] = ending
    # Keep the original full reference for historical F1 diagnostics. Only the
    # declared coverage scope changes, and every retained character is source-bound.
    case['body_requirements'] = body
