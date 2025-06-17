from . import (
    avatar,
    button,
    card,
    input,
    label,
    select,
    textarea,
    radio_group,
    coder_prompt,
    example,
)


shadcn_docs = [
    avatar.component_data,
    button.component_data,
    card.component_data,
    input.component_data,
    label.component_data,
    radio_group.component_data,
    select.component_data,
    textarea.component_data,
]


system_prompt = coder_prompt.get_main_coding_prompt(
    shadcn_docs=shadcn_docs, examples=example.shadcn_examples
)
