from maltypes import MalList, MalVector


def pr_str(data) -> str:
    return str(data)
    match data:
        case list():
            return "(" + " ".join(pr_str(i) for i in data) + ")"
        case str():
            return data
        case _:
            return str(data)
