import textwrap


class StreamlitMixin:
    def __repr__(self):
        """
        For better Streamlit display
        """
        return ""


def wrap(s: str, width=80):
    return "\n".join(
        "\n".join(
            textwrap.wrap(x, width=width),
        )
        for x in s.splitlines(keepends=True)
    )
