from tracardi.domain.context import Context
from tracardi.domain.entity import Entity
from tracardi.domain.event import Event
from tracardi.domain.profile import Profile
from tracardi.domain.session import Session
from tracardi.domain.profile_traits import ProfileTraits
from tracardi_plugin_sdk.service.plugin_runner import run_plugin
from tracardi_string_validator.plugin import StringValidatorAction


def test_plugin():
    init = {
        'validation_name': 'email',
        'data': "my@email.com"
    }

    payload = {}

    result = run_plugin(StringValidatorAction, init, payload)
    assert result.output.value is True

def test_dot():

    init = {"data": "event@id",
            "validation_name": "time"}
    payload = {}
    profile = Profile(id="profile-id", traits=ProfileTraits(public={"test": "new test"}))
    event = Event(id="event-id",
                  type="event-type",
                  profile=profile,
                  session=Session(id="session-id"),
                  source=Entity(id="source-id"),
                  context=Context())
    result = run_plugin(StringValidatorAction, init, payload,
                        profile, None, event)
    assert not result.output.value

    print("OUTPUT:", result.output)
    print("PROFILE:", result.profile)

