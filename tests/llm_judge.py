# tests/llm_judge.py
import json, anthropic

_client = anthropic.Anthropic()                 # le ANTHROPIC_API_KEY do ambiente
JUDGE_MODEL = "claude-haiku-4-5-20251001"       # rapido e barato p/ CI; troque p/ sonnet em casos dificeis

def semantic_assert(claim: str, context: str) -> tuple[bool, str]:
    """Pergunta ao Claude se a AFIRMACAO e verdadeira dado o CONTEXTO."""
    prompt = (
        "Voce e um avaliador rigoroso de testes de software. "
        "Decida se a AFIRMACAO e verdadeira considerando o CONTEXTO. "
        "Seja conservador: na duvida, reprove.\n\n"
        f"CONTEXTO:\n{context}\n\n"
        f"AFIRMACAO:\n{claim}\n\n"
        'Responda SOMENTE com JSON, sem markdown: {"pass": true|false, "reason": "..."}'
    )
    msg = _client.messages.create(
        model=JUDGE_MODEL, max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    text = msg.content[0].text.strip()
    text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    data = json.loads(text)
    return data["pass"], data["reason"]
