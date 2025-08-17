from app.domain.entities import can_transition

def test_valid_transitions():
    assert can_transition("CREATED", "PAID")
    assert can_transition("CREATED", "CANCELLED")
    assert can_transition("PAID", "FULFILLED")
    assert can_transition("PAID", "CANCELLED")

def test_invalid_transitions():
    assert not can_transition("FULFILLED", "PAID")
    assert not can_transition("CANCELLED", "PAID")
    assert not can_transition("PAID", "CREATED")
