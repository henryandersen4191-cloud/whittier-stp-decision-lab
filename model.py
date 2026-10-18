"""Transparent teaching model. Values are invented, not market research."""
import math

BUDGET = 200_000
SEGMENTS = {
    'Performance runners': {'icon':'🏃', 'buyers': 18000, 'reference': 150, 'elasticity': 1.2, 'cost': 65, 'fit': {'Performance':1.20,'Sustainability':0.85,'Comfort':0.95,'Value':0.80}},
    'Eco-conscious buyers': {'icon':'🌱', 'buyers': 16000, 'reference': 140, 'elasticity': 0.9, 'cost': 65, 'fit': {'Performance':0.85,'Sustainability':1.25,'Comfort':0.95,'Value':0.85}},
    'Everyday comfort': {'icon':'👟', 'buyers': 26000, 'reference': 110, 'elasticity': 1.0, 'cost': 65, 'fit': {'Performance':0.85,'Sustainability':0.95,'Comfort':1.20,'Value':1.00}},
    'Budget students': {'icon':'🎒', 'buyers': 22000, 'reference': 80, 'elasticity': 1.5, 'cost': 65, 'fit': {'Performance':0.80,'Sustainability':0.85,'Comfort':0.95,'Value':1.25}},
}
RESPONSES = {'Hold course': (1.0, 0), 'Match competitor promotion': (1.15, 10), 'Emphasize differentiation': (1.08, 4)}

def calculate(targets, positioning, price, allocations, event=False, response='Hold course'):
    if not targets or len(set(targets)) != len(targets) or any(t not in SEGMENTS for t in targets):
        raise ValueError('Choose at least one valid segment.')
    if positioning not in next(iter(SEGMENTS.values()))['fit'] or response not in RESPONSES:
        raise ValueError('Invalid strategy.')
    if not math.isfinite(price) or not 50 <= price <= 200:
        raise ValueError('Price must be between $50 and $200.')
    if set(allocations) != set(targets) or any(not math.isfinite(v) or v < 0 for v in allocations.values()) or sum(allocations.values()) > BUDGET:
        raise ValueError('Allocate no more than $200,000 to selected segments.')
    rows = []
    for name in targets:
        s = SEGMENTS[name]
        spend = allocations[name]
        reach = spend / (spend + 50000) if spend else 0
        price_factor = max(0.25, min(1.5, 1 - s['elasticity'] * (price - s['reference']) / s['reference']))
        # Rival discounts affect the two named segments only.
        affected = event and name in ('Everyday comfort', 'Budget students')
        competitor = 0.75 if affected else 1.0
        response_factor, extra_cost = RESPONSES[response] if affected else (1.0, 0)
        units = round(s['buyers'] * 0.12 * reach * s['fit'][positioning] * price_factor * competitor * response_factor)
        revenue = units * price
        contribution = units * (price - s['cost'] - extra_cost) - spend
        rows.append(dict(segment=name, spend=spend, reach=reach, price_factor=price_factor, competitor=competitor, response_factor=response_factor, units=units, revenue=revenue, contribution=contribution))
    return rows

def totals(rows):
    return {k: sum(r[k] for r in rows) for k in ('units','revenue','contribution','spend')}
