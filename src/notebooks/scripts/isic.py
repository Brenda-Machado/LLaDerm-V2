'''
Converte dados ISIC para o formato SimpleLesionData esperado
pelo restante do pipeline. Geração de laudos clínicos via templates.

isic.py
'''

from pydantic import BaseModel
from scripts.data import SimpleLesionData, SimpleReport


ISIC_2019_LABEL_TO_SKIN_LESION: dict[str, str | None] = {
    'MEL':  'Câncer de pele Melanoma',
    'NV':   'Nevo melanocítico',
    'BCC':  'Câncer de pele Não Melanoma (CEC ou CBC)',
    'AK':   'Ceratoses solares/actínicas',
    'BKL':  'Ceratose seborreica',
    'DF':   'Lesões de pele benignas com indicação de tratamento cirúrgico',
    'VASC': 'Outras',
    'SCC':  'Câncer de pele Não Melanoma (CEC ou CBC)',
    'UNK':  None,  
}

ISIC_2019_LABEL_COLUMNS = tuple(ISIC_2019_LABEL_TO_SKIN_LESION.keys())

SKIN_LESION_TO_RISK: dict[str, str] = {
    'Câncer de pele Melanoma':
        'AMARELA - ENCAMINHAMENTO COM PRIORIDADE PARA O AMBULATÓRIO DE REFERÊNCIA TERCIÁRIO',
    'Lesões de pele que necessitam de avaliação presencial com dermatologista':
        'AMARELA - ENCAMINHAMENTO COM PRIORIDADE PARA O AMBULATÓRIO DE REFERÊNCIA TERCIÁRIO',
    'Câncer de pele Não Melanoma (CEC ou CBC)':
        'VERDE - AVALIAÇÃO CLÍNICO-CIRURGIA COM ESPECIALISTA',
    'Ceratoses solares/actínicas':
        'VERDE - AVALIAÇÃO CLÍNICO-CIRURGIA COM ESPECIALISTA',
    'Nevo melanocítico':
        'AZUL - TRATAMENTO NA UNIDADE BÁSICA DE SAÚDE (UBS)',
    'Ceratose seborreica':
        'AZUL - TRATAMENTO NA UNIDADE BÁSICA DE SAÚDE (UBS)',
    'Fotodano crônico':
        'AZUL - TRATAMENTO NA UNIDADE BÁSICA DE SAÚDE (UBS)',
    'Lesões de pele benignas com indicação de tratamento cirúrgico':
        'AZUL - TRATAMENTO NA UNIDADE BÁSICA DE SAÚDE (UBS)',
    'Outras dermatoses':
        'AZUL - TRATAMENTO NA UNIDADE BÁSICA DE SAÚDE (UBS)',
    'Outras':
        'AZUL - TRATAMENTO NA UNIDADE BÁSICA DE SAÚDE (UBS)',
}

_CLINICAL_TEXTS: dict[str, tuple[list[str], str]] = {
    'Câncer de pele Melanoma': (
        [
            'Lesão melanocítica com características dermoscópicas de alto risco.',
            'Assimetria acentuada, bordas irregulares e variação cromática presentes.',
            'Estruturas regressivas e véu azul-esbranquiçado observados.',
        ],
        'Lesão altamente suspeita de melanoma. Encaminhamento urgente para avaliação '
        'presencial com dermatologista para biópsia e estadiamento.'
    ),
    'Nevo melanocítico': (
        [
            'Lesão melanocítica com padrão reticular simétrico.',
            'Bordas bem definidas e coloração homogênea.',
            'Ausência de estruturas atípicas ao exame dermoscópico.',
        ],
        'Nevo melanocítico benigno sem características de malignidade. '
        'Acompanhamento periódico recomendado com autoexame regular.'
    ),
    'Câncer de pele Não Melanoma (CEC ou CBC)': (
        [
            'Lesão com estruturas vasculares atípicas e áreas brancas brilhantes.',
            'Padrão dermoscópico compatível com carcinoma de pele não melanoma.',
            'Bordas elevadas ou ulceração superficial presentes.',
        ],
        'Lesão compatível com carcinoma de pele não melanoma (CEC ou CBC). '
        'Encaminhamento para avaliação presencial com dermatologista para '
        'confirmação diagnóstica e definição de conduta cirúrgica.'
    ),
    'Ceratoses solares/actínicas': (
        [
            'Lesão eritematosa com escamas aderidas sobre fundo avermelhado.',
            'Superfície áspera e padrão pseudorredicular ao dermatoscópio.',
            'Bordas mal definidas em contexto de fotodano crônico.',
        ],
        'Ceratose actínica com indicação de tratamento. Encaminhamento para '
        'avaliação e tratamento em unidade de referência dermatológica.'
    ),
    'Ceratose seborreica': (
        [
            'Lesão com aspecto cerebroide, pseudocistos de milium e criptas comedo-like.',
            'Superfície verrucosa com coloração castanha heterogênea.',
            'Ausência de estruturas vasculares atípicas.',
        ],
        'Ceratose seborreica sem características de malignidade. '
        'Tratamento conforme indicação clínica e queixa estética do paciente.'
    ),
    'Fotodano crônico': (
        [
            'Lesão pigmentada de aspecto lentiginoso em área de exposição solar crônica.',
            'Padrão reticular com granulação fina ao dermatoscópio.',
            'Bordas regulares e coloração uniforme.',
        ],
        'Lesão compatível com fotodano crônico (lentigo solar). '
        'Orientação para fotoproteção rigorosa e acompanhamento clínico periódico.'
    ),
    'Lesões de pele benignas com indicação de tratamento cirúrgico': (
        [
            'Lesão de aspecto benigno com padrão dermoscópico característico.',
            'Ausência de estruturas atípicas sugestivas de malignidade.',
            'Indicação de remoção por critérios estéticos ou funcionais.',
        ],
        'Lesão benigna com indicação de avaliação para tratamento cirúrgico eletivo. '
        'Encaminhamento para consulta com especialista.'
    ),
    'Lesões de pele que necessitam de avaliação presencial com dermatologista': (
        [
            'Lesão melanocítica atípica com padrão dermoscópico indeterminado.',
            'Características insuficientes para classificação definitiva por teledermatologia.',
            'Necessidade de avaliação presencial para investigação adicional.',
        ],
        'Lesão com características atípicas que requerem avaliação presencial '
        'com dermatologista para investigação diagnóstica complementar, '
        'incluindo possível biópsia.'
    ),
    'Outras dermatoses': (
        [
            'Lesão com padrão dermoscópico sugestivo de dermatose inflamatória ou benigna.',
            'Ausência de estruturas melanocíticas atípicas.',
            'Características compatíveis com lesão de origem não neoplásica.',
        ],
        'Lesão compatível com dermatose benigna. '
        'Acompanhamento clínico e tratamento conforme apresentação clínica.'
    ),
    'Outras': (
        [
            'Lesão com características dermoscópicas inespecíficas.',
            'Padrão estrutural não enquadrado nas categorias diagnósticas principais.',
            'Ausência de sinais imediatos de malignidade.',
        ],
        'Lesão de caracterização inespecífica ao exame dermoscópico. '
        'Acompanhamento clínico e reavaliação conforme evolução.'
    ),
}


def get_clinical_texts(skin_lesion: str) -> tuple[list[str], str]:
    return _CLINICAL_TEXTS.get(
        skin_lesion,
        (
            ['Lesão de pele identificada ao exame dermoscópico.'],
            'Acompanhamento clínico recomendado conforme evolução da lesão.'
        )
    )

def resolve_isic_2019_label(row: dict) -> str | None:
    # Retorna o código da label ativa (e.g. 'MEL') ou None em caso de ambiguidade ou label ausente.

    active = [
        col for col in ISIC_2019_LABEL_COLUMNS
        if float(row.get(col, 0)) == 1.0
    ]
    return active[0] if len(active) == 1 else None


def isic_2019_to_simple_lesion_data(image_name: str,
                                     label_code: str,
                                     exam_id: int) -> SimpleLesionData | None:

    skin_lesion = ISIC_2019_LABEL_TO_SKIN_LESION.get(label_code)

    if skin_lesion is None:
        return None

    risk = SKIN_LESION_TO_RISK[skin_lesion]
    skin_lesion_conclusion, conclusion = get_clinical_texts(skin_lesion)

    return SimpleLesionData(
        exam_id=exam_id,
        image=f'{image_name}.jpg',
        report=SimpleReport(
            skin_lesion=skin_lesion,
            risk=risk,
            conclusion=conclusion,
            skin_lesion_conclusion=skin_lesion_conclusion
        )
    )