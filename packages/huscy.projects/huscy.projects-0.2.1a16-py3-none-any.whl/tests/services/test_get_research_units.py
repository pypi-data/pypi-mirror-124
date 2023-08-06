import pytest
from itertools import cycle

from model_bakery import baker

from huscy.projects.services import get_research_units

pytestmark = pytest.mark.django_db


def test_get_research_units():
    names = ['Project1', 'This is a project', 'A new project']
    baker.make('projects.ResearchUnit', name=cycle(names), _quantity=len(names))

    result = get_research_units()

    assert sorted(names) == list(result.values_list('name', flat=True))
