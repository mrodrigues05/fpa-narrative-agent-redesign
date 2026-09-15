# Checklist — redesenho de agente de narrativa financeira

## Cálculo
- Nunca deixe o LLM fazer contas críticas (somas, taxas, comparação %, qual é o maior driver). Matemática determinística, sempre — o LLM só interpreta o resultado já calculado.
- Nunca esconda o cálculo intermediário. Todo número citado na narrativa precisa responder "de onde veio isso" em segundos — valor → fórmula → dado de entrada → período → fonte.
- Nunca publique uma narrativa cuja soma dos impactos por unidade não reconcilie com a variação total. Bloqueie a narrativa (`VALIDATION FAILED`), não arredonde silenciosamente.

## Memória / histórico
- Histórico gera hipótese, nunca prova. Uma claim precisa ser testada de novo a cada período — não repetida porque "foi assim mês passado".
- Nunca transforme um "padrão observado" em regra permanente sem prazo de validade (`valid_until` / `requires_current_period_validation`).
- Claims são estruturadas — `{claim, período de origem, evidência de origem, status}` — não frases soltas que só se acumulam num arquivo de texto.

## Narrativa
- O LLM não escolhe sozinho o driver principal — ele recebe essa decisão já calculada (`primary_driver`) e só narra em cima dela.
- Separe fato, interpretação, hipótese e recomendação. Recomendação nunca aparece disfarçada de fato.
- Quando a evidência for insuficiente ou ambígua, a resposta certa é dizer isso — declarar limitação não é falha do agente, é o comportamento correto.
- Nunca invente o dado que falta. Sinalize "dado ausente" e diga qual dado resolveria — não estime no lugar dele.

## Validação
- Todo redesenho precisa de um checker automático depois da narrativa, antes de ela poder ser aceita: reconciliação, driver principal suportado por evidência, "historical anchoring" (repetir um padrão já contradito pelo período atual).
- O teste mais importante é o **adversarial**: um caso onde o histórico tenta induzir o erro (o padrão do período anterior não vale mais). Se o agente redesenhado ainda repetir o diagnóstico antigo nesse caso, o redesenho falhou — não é um detalhe, é o critério de sucesso.
- Todo checker precisa de casos conhecidos com gabarito (`assert status == "PASS"` / `"FAIL"`), não só "um analista aprovou".

## Escopo do protótipo
- Não vire dashboard de BI genérico, chatbot financeiro, ou infraestrutura de produção (multiagente, vector DB, MLOps). O objetivo é demonstrar raciocínio verificável, não sofisticação técnica.
- Prioridade, nessa ordem: **correção > verificabilidade > transparência > experiência visual > sofisticação técnica.**
- Se um script Python simples resolve, é isso que se entrega primeiro — complexidade só entra quando resolve uma limitação já demonstrada.
- Não esconda falhas: se a nova versão errar em algum caso, a saída deve mostrar isso (`FAILED`, `expected` vs. `agent`, motivo) — o objetivo não é provar uma IA perfeita, é provar que o sistema detecta e sinaliza o próprio erro.

## Critérios de avaliação típicos desse tipo de case
- Qualidade da leitura do dado
- Qualidade do diagnóstico e do raciocínio que levou até ele
- Verificabilidade do que se propõe (dá pra reconstruir "por que essa conclusão?")
- Pragmatismo — solução enxuta contra over-engineering
- Honestidade sobre os próprios limites
- Clareza, no documento e na defesa oral
