READ_SCOPE = "user-read-playback-state"
MODIFY_PLAYBACK_SCOPE = "user-modify-playback-state"
MODIFY_LIBRARY_SCOPE = "user-library-modify"
READ_LIBRARY_SCOPE = "user-library-read"

SCOPES = [READ_SCOPE, MODIFY_PLAYBACK_SCOPE, MODIFY_LIBRARY_SCOPE, READ_LIBRARY_SCOPE]

def get_scope(scopes):
    """
    Returns the scopes needed to perform a certain operation
    """

    assert type(scopes) not in [dict, set, frozenset], "Argument must be a string, list or tuple"

    if type(scopes) is str:

        # if the parameter matches one of the defined scopes, return it

        if scopes in SCOPES: return scopes

        # string passed in is not one of the defined scopes, parse it

        # if we are not split by commas, throw error

        assert (scopes.find(',') != -1), "The scopes string must be separated by commas (',')"

        possible_scopes = []

        for possible_scope in scopes.split(','):
            if possible_scope in SCOPES: possible_scopes.append(possible_scope)

        assert len(possible_scopes) > 0, "No valid scopes were given"

        return ",".join(possible_scopes)
    else: # we are a container

        possible_scopes = []

        for possible_scope in scopes:
            if possible_scope in SCOPES: possible_scopes.append(possible_scope)

        assert len(possible_scopes) > 0, "No valid scopes were given"

        return ",".join(possible_scopes)