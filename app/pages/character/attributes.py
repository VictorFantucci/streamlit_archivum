# ------------------------------------------------------------------------------------------------ #
# IMPORTS

import os
import math
import streamlit as st
import warnings
from streamlit_option_menu import option_menu
warnings.simplefilter(action='ignore', category=UserWarning)

# RELATIVE IMPORTS
from app.src.data_loader import read_excel_data

# ------------------------------------------------------------------------------------------------ #
# FUNÇÕES ATRIBUTOS PRIMÁRIOS

def strength() -> None:
    """Atributos Primários: Força (ST)"""

    st.markdown(r"""
        ### Força (ST)

        A **Força (ST)** mede o poder físico e a massa muscular do personagem.
        Ela é crucial para guerreiros em um mundo primitivo, pois permite:

        - Causar e absorver mais dano em combate corpo-a-corpo
        - Levantar e arremessar objetos
        - Mover-se rapidamente com carga

        ---

        A **ST** também influencia diretamente:

        - **Pontos de Vida (Junto com HT)**
        - **Carga Básica (CB)**
        - **Dano básico**
        - **Toxicidade (Junto com IQ e HT)**

        > Portanto, aumentar o ST também aumenta esses atributos.
    """)

def dexterity() -> None:
    """Atributos Primários: Destreza (DX)"""

    st.markdown(r"""
        ### Destreza (DX)

        A **Destreza (DX)** mede a combinação de **agilidade e coordenação motora** do personagem.

        Ela influencia diretamente:

        - **Perícias atléticas** (corrida, saltos, escalada)
        - **Perícias de combate** (ataques precisos, esquiva)
        - **Operação de veículos** (condução, pilotagem)
        - **Trabalho manual delicado** (ajustes finos, consertos, trabalhos de precisão)

        ---

        A **DX** também influencia diretamente:

        - **Velocidade Básica** (tempo de reação)
        - **Deslocamento** (quão rápido você corre)
        - **Esquiva** (quão fácil é se esquivar de golpes)

        > Portanto, aumentar a DX também aumenta esses atributos.
    """)

def intelligence() -> None:
    """Atributos Primários: Inteligência (IQ)"""

    st.markdown(r"""
        ### Inteligência (IQ)

        A **Inteligência (IQ)** mede o **poder mental** do personagem, incluindo:

        - Raciocínio
        - Criatividade
        - Intuição
        - Memória
        - Percepção
        - Razão
        - Lucidez
        - Força de vontade

        Ela influencia diretamente todas as **perícias “mentais”**, como:

        - Ciências
        - Interações sociais
        - Magia
        - Inventos e invenções

        > Qualquer **feiticeiro, cientista ou inventor** precisa de um IQ alto para ser eficaz.

        ---

        A **IQ** também influencia diretamente:

        - **Mana (junto com IQ)
        - - **Toxicidade (Junto com ST e HT)**
        - **Vontade**
        - **Percepção**

        > Portanto, aumentar a IQ também aumenta esses atributos.
    """)

def vitality() -> None:
    """Atributos Primários: Vitalidade"""

    st.markdown(r"""
        ### Vitalidade (HT)

        A **Vitalidade (HT)** mede a **saúde e energia** do personagem.
        Ela representa:

        - Vigor físico
        - Resistência a venenos, doenças, radiações e outros efeitos adversos

        ---

        ### Importância da HT

        - Uma **HT alta** é benéfica para todos os personagens
        - É **crucial para guerreiros** de baixa tecnologia, que dependem da resistência física

        ---

        A **HT** também influencia diretamente:

        - **Pontos de Vida (Junto com ST)**
        - **Mana (junto com IQ)
        - **Toxicidade (junto com ST e IQ)
        - **Velocidade Básica** (junto com DX)
        - **Deslocamento** (junto com Velocidade Básica)

        > 💡 Personagens com HT baixa sofrerão mais rapidamente com fadiga, venenos ou doenças.
    """)

# ------------------------------------------------------------------------------------------------ #
# FUNÇÕES ATRIBUTOS SECUNDÁRIOS

def hp() -> None:
    """Atributos secundários: PV."""
    st.markdown(r"""
        ### Pontos de Vida (PV)

        Os **Pontos de Vida (PV)** representam a resistência física total do personagem.

        Eles são calculados pela fórmula:

        $$
        \text{PV} = \frac{HT \times 4 + ST \times 2}{2}
        $$

        Sendo:

        - $HT$ = Vitalidade
        - $ST$ = Força
    """)
    with st.expander("Exemplo"):
        st.markdown(r"""
            Se um personagem possui:

            $$
            HT = 11
            $$

            $$
            ST = 10
            $$

            Então:

            $$
            \text{PV} = \frac{(11 \times 4) + (10 \times 2)}{2}
            $$

            $$
            \text{PV} = \frac{44 + 20}{2}
            $$

            $$
            \text{PV} = \frac{64}{2} = 32
            $$
        """)

def mana() -> None:
    """Atributos Secundários: Mana"""

    st.markdown(r"""
        ### Mana (MP)

        A **Mana (MP)** representa a energia mágica disponível do personagem para conjurar magias e sustentar efeitos mágicos.

        Ela é calculada pela fórmula:

        $$
        \text{Mana} = \frac{IQ \times 4 + HT \times 2}{2}
        $$

        Sendo:

        - $IQ$ = Inteligência
        - $HT$ = Vitalidade
    """)

    with st.expander("Exemplo"):
        st.markdown(r"""
            Se um personagem possui:

            $$
            IQ = 12
            $$

            $$
            HT = 10
            $$

            Então:

            $$
            \text{Mana} = \frac{(12 \times 4) + (10 \times 2)}{2}
            $$

            $$
            \text{Mana} = \frac{48 + 20}{2}
            $$

            $$
            \text{Mana} = \frac{68}{2} = 34
            $$
        """)

def toxicity() -> None:
    """Atributos Secundários: Toxicidade"""

    st.markdown(r"""
        ### Toxicidade

        A **Toxicidade** representa o limite fisiológico do personagem para consumir substâncias alquímicas sem sofrer efeitos adversos.

        Ela é calculada pela fórmula:

        $$
        \text{Toxicidade} = \frac{HT \times 4 + IQ \times 3 + ST \times 3}{3}
        $$

        Sendo:

        - $HT$ = Vitalidade
        - $IQ$ = Inteligência
        - $ST$ = Força

    """)

    with st.expander("Exemplo"):
        st.markdown(r"""
            Se um personagem possui:

            $$
            HT = 12
            $$

            $$
            IQ = 11
            $$

            $$
            ST = 10
            $$

            Então:

            $$
            \text{Toxicidade} = \frac{(12 \times 4) + (11 \times 3) + (10 \times 3)}{3}
            $$

            $$
            \text{Toxicidade} = \frac{48 + 33 + 30}{3}
            $$

            $$
            \text{Toxicidade} = \frac{90}{3} = 37
            $$
        """)

def damage(df_dict: dict) -> None:
    """Atributos secundários: Dano."""

    st.subheader("Dano Base", divider="grey")

    st.markdown(r"""
    Sua ST determina quanto dano você provoca em um combate desarmado ou com uma arma branca. Dois tipos de danos derivam da ST:

    - Dano por Golpe de Ponta (**GDP**) é o dano básico causado por um soco, chute ou mordida, ou com uma arma de ponta como uma lança ou um florete.
    - Dano por golpe em Balanço (**BAL**) é o dano básico causado por um machado, um porrete, uma espada, ou qualquer coisa que funcione como uma alavanca para multiplicar a ST.

    Para saber seu dano básico, consulte a Tabela de Dano abaixo. Ele está expresso no formato "dados + bônus"

    ⚠️ Armas e ataques específicos podem modificar os valores.
                """)

    df_base_damage = df_dict["base_damage"]

    with st.expander("Tabela de Dano"):

        df = (
            df_base_damage
            .fillna('')
            .convert_dtypes()
            .sort_values(by="attacker_strength")
            .reset_index(drop=True)
        )

        # ---------------------------------------------------
        # 📦 Criar colunas formatadas (3 colunas finais)
        # ---------------------------------------------------

        def format_damage(dados, mod):
            mod = int(mod)
            if mod == 0:
                return f"{dados}"
            return f"{dados} {mod:+d}"

        df_formatado = df.copy()

        df_formatado["GDP"] = df_formatado.apply(
            lambda row: format_damage(
                row["GDP_base_damage"],
                row["GDP_base_damage_modifier"]
            ),
            axis=1
        )

        df_formatado["BAL"] = df_formatado.apply(
            lambda row: format_damage(
                row["BAL_base_damage"],
                row["BAL_base_damage_modifier"]
            ),
            axis=1
        )

        df_final = df_formatado[[
            "attacker_strength",
            "GDP",
            "BAL"
        ]].rename(columns={
            "attacker_strength": "ST"
        })

        # ---------------------------------------------------
        # 📄 Paginação
        # ---------------------------------------------------

        itens_por_pagina = 10
        total_paginas = math.ceil(len(df_final) / itens_por_pagina)

        pagina = st.number_input(
            "Página",
            min_value=1,
            max_value=total_paginas,
            value=1,
            step=1
        )

        inicio = (pagina - 1) * itens_por_pagina
        fim = inicio + itens_por_pagina

        df_pagina = df_final.iloc[inicio:fim]

        # ---------------------------------------------------
        # 📊 Exibição
        # ---------------------------------------------------

        st.dataframe(
            df_pagina,
            use_container_width=True,
            hide_index=True
        )

        st.caption(f"Página {pagina} de {total_paginas}")

def base_carry_load() -> None:
    """Atributos secundários: Carga Básica"""

    st.subheader("Carga Básica", divider="grey")

    st.markdown(r"""
        A **Carga Básica (CB)** é o peso máximo que um personagem é capaz de erguer sobre a cabeça com **uma mão em um segundo**.

        Ela é calculada por:

        $$
        CB = \frac{ST \times ST}{10}
        $$

        O resultado é dado em **quilogramas (kg)**.

        Se a CB for maior que 5 kg, arredonde para o número inteiro mais próximo.

        **Exemplo:**

        $$
        ST = 9
        $$

        $$
        CB = \frac{9 \times 9}{10} = \frac{81}{10} = 8{,}1 \text{ kg}
        $$

        Arredondando:

        $$
        CB = 8 \text{ kg}
        $$

        Um humano médio possui:

        $$
        ST = 10
        $$

        $$
        CB = \frac{10 \times 10}{10} = 10 \text{ kg}
        $$

    """)

    st.markdown(r"""
        - Dobrando o tempo, é possível erguer:

        $$
        2 \times CB
        $$

        (ainda com uma mão)

        - Quadruplicando o tempo e usando duas mãos, pode-se erguer:

        $$
        8 \times CB
        $$
    """)

    st.markdown(r"""
        A quantidade de equipamento que você pode carregar — armaduras, mochilas, armas, etc. — é derivada da **CB**.

        Para mais detalhes e para consultar a tabela completa, veja a seção **Carga e Movimento**.
    """)

def base_speed() -> None:
    """Atributos Secundários: Velocidade Básica"""

    st.markdown(r"""
        ### Velocidade Básica

        A **Velocidade Básica (VB)** mede os reflexos e a rapidez corpórea geral do personagem.
        Ela influencia:

        - Velocidade de corrida (veja **Deslocamento** abaixo)
        - Chance de **esquivar ataques**
        - Ordem de ação em combate (uma velocidade maior permite agir primeiro)
    """)

    with st.expander("Cálculo da Velocidade Básica"):
        st.markdown(r"""
            A fórmula para calcular sua **Velocidade Básica** é:

            $$
            \text{Velocidade Básica} = \frac{DX + HT}{4}
            $$

            - $DX$ = Destreza
            - $HT$ = Vitalidade

            > ⚠️ Não arredonde! Por exemplo, 5,25 é melhor que 5.
        """)

def movement() -> None:
    """Atributos Secundários: Deslocamento"""

    st.markdown(r"""
        ### Deslocamento

        O **Deslocamento** representa a velocidade do personagem em metros por segundo (m/s).
        Ele indica quão rápido você pode correr — ou se arrastar, rolar, etc. — sem carga.
        > É possível temporariamente correr mais rápido com um **sprint** em linha reta.

        ---

        ### Cálculo do Deslocamento

        O **Deslocamento básico** é igual à **Velocidade Básica arredondada para baixo**:

        $$
        \text{Deslocamento} = \lfloor \text{Velocidade Básica} \rfloor
        $$

        - Por exemplo, se sua Velocidade Básica for 5,75:

        $$
        \text{Deslocamento} = \lfloor 5,75 \rfloor = 5 \text{ m/s}
        $$

        - Um humano médio tem:

        $$
        \text{Deslocamento} = 5 \text{ m/s}
        $$

        > Isso significa que ele pode correr 5 metros por segundo sem carga.

        ---

        ### Movimento em combate

        O **Movimento em combate** é o **Deslocamento modificado pelo nível de carga** do personagem.
    """)

def dodge() -> None:
    """Atributos Secundários: Esquiva"""

    st.markdown(r"""

        ### Esquiva

        Sua defesa **Esquiva** é calculada como:

        $$
        \text{Esquiva} = \lfloor \text{Velocidade Básica} + 3 \rfloor
        $$

        - Por exemplo, se sua Velocidade Básica for 5,25:

        $$
        \text{Esquiva} = \lfloor 5,25 + 3 \rfloor = 8
        $$

        > ⚠️ A carga do personagem pode reduzir a Esquiva (veja **Carga e Movimento**).

        Para esquivar de um ataque, o personagem deve rolar **3d6** e obter um resultado **igual ou menor que sua Esquiva**.
    """)

def carry_load_and_movement() -> None:
    """Atributos secundários: Carga e Movimento"""

    st.markdown(r"""
        ### Carga e Movimento

        A **Carga** representa o peso total que você está carregando em relação à sua **Força (ST)**.
        Ela afeta tanto o **Movimento** quanto a **Esquiva** do personagem.

        Os efeitos são divididos em **cinco níveis de carga**, numerados de 0 a 4:

        | Nível de Carga | Peso Máximo | Movimento | Esquiva |
        |----------------|------------|-----------|---------|
        | 0 – Carga Nula | até $CB$ | $\text{Movimento} = \text{Deslocamento}$ | $\text{Esquiva} \times 1$ |
        | 1 – Carga Leve | até $2 \times CB$ | $\text{Movimento} = \lfloor \text{Deslocamento} \times 0,8 \rfloor$ | $\text{Esquiva} - 1$ |
        | 2 – Carga Média | até $3 \times CB$ | $\text{Movimento} = \lfloor \text{Deslocamento} \times 0,6 \rfloor$ | $\text{Esquiva} - 2$ |
        | 3 – Carga Pesada | até $6 \times CB$ | $\text{Movimento} = \lfloor \text{Deslocamento} \times 0,4 \rfloor$ | $\text{Esquiva} - 3$ |
        | 4 – Carga Muito Pesada | até $10 \times CB$ | $\text{Movimento} = \lfloor \text{Deslocamento} \times 0,2 \rfloor$ | $\text{Esquiva} - 4$ |

        > **Regras adicionais:**
        >
        > - Sempre arredonde **para baixo**.
        > - A carga nunca pode reduzir o **Movimento** ou a **Esquiva** abaixo de 1.
        > - Estes números são usados pelo Mestre para penalidades em testes, por exemplo: **Escalada, Furtividade e Natação**.

    """)

    with st.expander("Fórmulas Resumidas"):
        st.markdown(r"""
            Para um personagem com **Deslocamento (D)** e **Esquiva (E)**:

            - **Carga Leve (1):**
            $$
            \text{Movimento} = \lfloor D \times 0,8 \rfloor, \quad \text{Esquiva} = E - 1
            $$

            - **Carga Média (2):**
            $$
            \text{Movimento} = \lfloor D \times 0,6 \rfloor, \quad \text{Esquiva} = E - 2
            $$

            - **Carga Pesada (3):**
            $$
            \text{Movimento} = \lfloor D \times 0,4 \rfloor, \quad \text{Esquiva} = E - 3
            $$

            - **Carga Muito Pesada (4):**
            $$
            \text{Movimento} = \lfloor D \times 0,2 \rfloor, \quad \text{Esquiva} = E - 4
            $$
        """)

def will() -> None:
    """Atributos Secundários: Vontade"""

    st.markdown(r"""
        ### Vontade

        A **Vontade** mede a capacidade do personagem de resistir a:

        - Pressão psicológica: lavagem cerebral, medo, hipnotismo, interrogatório, sedução, tortura, etc.
        - Ataques sobrenaturais: magia, psiquismo, etc.

        A base de sua Vontade é igual ao seu **IQ**:

        $$
        \text{Vontade base} = IQ
        $$

        Você pode **aumentar ou reduzir** sua Vontade por meio das seguintes vantagem e desvantagem:

        - Força de Vontade.
        - Vontade Fraca.

        Consulte a página de Vantagens e Desvantagens.

        > ⚠️ Sem permissão do Mestre, a Vontade nunca pode exceder 20 ou ser menor que 4.
    """)

    with st.expander("Sobre Desvantagens Mentais"):
        st.markdown(r"""
            Algumas desvantagens mentais permitem que o personagem afetado faça testes de **IQ** ou **Vontade** (pág. 93) para tentar evitar os efeitos adversos de seu problema.

            - Qualquer resultado **maior ou igual a 14** significará uma **falha**.
            - Caso contrário, personagens com inteligência ou força de vontade muito alta seriam quase completamente imunes aos seus maus hábitos, o que não refletiria a realidade.
        """)

def perception() -> None:
    """Atributos Secundários: Percepção (Sentidos)"""

    st.markdown(r"""
        ### Percepção

        A **Percepção (Per)** representa a atenção geral do personagem.
        O Mestre realiza **Testes de Sentidos** contra sua Percepção para determinar se o personagem nota detalhes ou acontecimentos no ambiente (veja **Testes de Sentidos**).

        A base de sua Percepção é igual ao seu **IQ**:

        $$
        \text{Percepção base} = IQ
        $$

        Você pode **aumentar ou reduzir** sua Percepção através de vantagens e desvantagens:

        - Vantagens:
            - Visão Aguçada.
            - Ouvido Aguçado.
            - Paladar/Olfato Apurados.
        - Desvantagens Físicas.

        > ⚠️ Sem permissão do Mestre, a Percepção nunca pode exceder 20 ou ser menor que 4.
    """)

# ------------------------------------------------------------------------------------------------ #
# FUNÇÕES DE VISUALIZAÇÃO DO STREAMLIT

def secondary_attributes(df_dict: dict) -> None:
    """ Atributos secundários."""

    options = ["Pontos de Vida", "Mana", "Toxicidade", "Dano Base", "Velocidade Básica",
               "Deslocamento", "Esquiva", "Carga Básica", "Carga e Movimento",
               "Vontade", "Percepção"]

    selection =  st.selectbox(
            label="Selecione o atributo:",
            options=options,
            index=0,
        )

    if selection == options[0]:
        hp()
    elif selection == options[1]:
        mana()
    elif selection == options[2]:
        toxicity()
    elif selection == options[3]:
        damage(df_dict)
    elif selection == options[4]:
        base_speed()
    elif selection == options[5]:
        movement()
    elif selection == options[6]:
        dodge()
    elif selection == options[7]:
        base_carry_load()
    elif selection == options[8]:
        carry_load_and_movement()
    elif selection == options[9]:
        will()
    elif selection == options[10]:
        perception()

def primary_attributes() -> None:
    """Atributos Primários"""

    options = ["Força", "Destreza", "inteligência", "Vitalidade"]


    selection = option_menu(
            menu_title=None,
            options=options,
            default_index=0,
            orientation="horizontal"
        )

    if selection == options[0]:
        strength()
    elif selection == options[1]:
        dexterity()
    elif selection == options[2]:
        intelligence()
    elif selection == options[3]:
        vitality()

# ------------------------------------------------------------------------------------------------ #
# FUNÇÃO MAIN

def main():
    df_dict = read_excel_data("attributes.xlsx")

    options = ["Atributos Primários", "Atributos Secundários"]

    with st.sidebar:
        st.markdown("### Navegação")
        selection = option_menu(
            menu_title=None,
            options=options,
            icons=["1-square-fill", "2-square-fill"],
            default_index=0,
        )

    # Roteamento das páginas
    if selection == options[0]:
        primary_attributes()
    elif selection == options[1]:
        secondary_attributes(df_dict)

# ------------------------------------------------------------------------------------------------ #
main()