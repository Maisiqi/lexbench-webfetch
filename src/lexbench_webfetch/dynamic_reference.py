"""Field contracts for independently observed, finite dynamic practice pages."""
from .rule_policy import SCORER_POLICY
import re


def entry_field_orders(fields):
    """Supported visible record layouts, independent of provider and case IDs.

    These are tuples, not arbitrary permutations or substring windows. Shipping
    badges precede product names in DOM extraction and follow prices in captures.
    Unknown schemas fail closed in the entry matcher.
    """
    fields = frozenset(fields)
    for rule in SCORER_POLICY['optional_entry_layouts']:
        if set(rule['required']) <= fields <= set(rule['allowed']):
            body = tuple(field for field in rule['body_order'] if field in fields)
            edge = rule['edge_field']
            return [body + (edge,), (edge,) + body] if edge in fields else [body]
    return [tuple(layout) for layout in SCORER_POLICY['entry_layouts']
            if frozenset(layout) == fields]


def entry_facts(case_id, entries):
    rule = SCORER_POLICY['dynamic_cases'].get(case_id)
    if rule is None:
        raise ValueError('Unknown dynamic case')
    fields = rule['fields']
    facts=[]
    for i,entry in enumerate(entries,1):
        values=[line.strip() for line in entry.splitlines() if line.strip()]
        entry_fields = fields
        optional = rule.get('optional_fields', [])
        if optional:
            entry_fields = [field for field in fields
                            if field not in {item['field'] for item in optional}]
            for item in optional:
                index = item['index']
                value = values[index] if -len(values) <= index < len(values) else None
                if value is not None and (
                        value.startswith(item['prefix']) if 'prefix' in item
                        else value == item['equals']):
                    entry_fields.append(item['field'])
        if len(values)!=len(entry_fields):raise ValueError(f'Incomplete or unexpected fields: {case_id} entry {i}')
        for field,value in zip(entry_fields,values):
            value = value.removeprefix(SCORER_POLICY['dynamic_field_prefixes'].get(field, ''))
            alternatives=[value]
            # Numeric count + its label can be adjacent in Markdown extraction.
            # Keep the whole number/unit, never remove arbitrary word boundaries.
            if field in SCORER_POLICY['dynamic_compact_fields'] and re.fullmatch(
                    SCORER_POLICY['dynamic_compact_fields'][field], value):
                alternatives.append(re.sub(r'\s+','',value))
            facts.append({'id':f'entry-{i}-{field}','alternatives':alternatives})
    return facts
