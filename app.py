import streamlit as st
import pandas as pd
import hashlib

# SALT (Troque por uma DString longa / aleatória; em deploy use st.secrets)
SALT = "adbhsbdhbfjdsnffbhsdsbvdvsvdvasldhvsldhbsabdhabshdbfndfkdkfna"

def hash_password(password: str) -> str:
    """retorna o hash SHA256 da senha + salt."""
    return hashlib.sha256(f"{password}{SALT}".encode("utf-8")).hexdigest()

CREDENCIAIS = {
    "cliente.teste": hash_password("Eletroduto#2025"),
    # adicione outros usuarios assim:
    # "cliente1": "hash_gerado_aqui",
}

#Inicializa flags na sessão
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

#Se já está logado, oferecer logout na sidebar
if st.session_state.get("logged_in"):
    with st.sidebar:
        st.write(f"👤 Conectado como: **{st.session_state.username}**")
        if st.button("Sair / Logout"):
            #Limpa sessão
            for k in ["logged_in", "username"]:
                if k in st.session_state:
                    del st.session_state[k]
            #Tenta forçar o refresh 
            try:
                st.rerun()
            except Exception:
                try:
                    st.rerun()
                except Exception:
                    pass

# --- Se não está logado, mostrar formulário de login e impedir execução do resto ---
if not st.session_state.get("logged_in", False):
    st.markdown(
        """
        <div style="max-width:420px;margin:20px auto;padding:18px;border-radius:8px;
                    box-shadow:0 2px 4px rgba(0,0,0,0.08);background:#ffffff;">
            <h3 style="text-align:center;color:#1E90FF;margin:0;padding-bottom:8px;">🔒 Login - Dimensionamento</h3>
            <p style="text-align:center;color:gray;margin-top:0;margin-bottom:8px;font-size:13px;">
                Insira suas credenciais para acessar a ferramenta.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form", clear_on_submit=False):
        user_input = st.text_input("Usuário", key="login_user")
        pw_input = st.text_input("Senha", type="password", key="login_pass")
        remember = st.checkbox("Manter conectado (apenas local)", value=False)
        submitted = st.form_submit_button("Entrar")

        if submitted:
            if user_input in CREDENCIAIS and CREDENCIAIS[user_input] == hash_password(pw_input):
                st.session_state.logged_in = True
                st.session_state.username = user_input
                st.success(f"Bem-vindo, {user_input}!")
                # tenta forçar atualização para que o resto do script seja executado
                try:
                    st.experimental_rerun()
                except Exception:
                    try:
                        st.rerun()
                    except Exception:
                        pass
            else:
                st.error("Usuário ou senha inválidos. Verifique e tente novamente.")

    # para evitar que o resto do app rode antes do login:
    st.stop()


#===========================

# TABELA DE ELETRODUTOS

#===========================

eletrodutos = [
    {"polegada": '3/4"', "diametro_mm": 19.05, "area_total": 285.02,
     "area_ocupavel53":151.06, "area_ocupavel31": 88.36, "area_ocupavel40": 114.0},
    {"polegada": '1"', "diametro_mm": 25.4, "area_total": 506.71,
      "area_ocupavel53":268.55, "area_ocupavel31": 157.08, "area_ocupavel40": 202.68},
    {"polegada": '1 1/4"', "diametro_mm": 31.75, "area_total": 791.73,
      "area_ocupavel53":419.62, "area_ocupavel31": 245.44, "area_ocupavel40": 316.69},
    {"polegada": '1 1/2"', "diametro_mm": 38.1, "area_total": 1140.09,
      "area_ocupavel53":604.25, "area_ocupavel31": 353.43, "area_ocupavel40": 456.04},
    {"polegada": '2"', "diametro_mm": 50.8, "area_total": 2026.83,
      "area_ocupavel53":1074.22, "area_ocupavel31": 628.32, "area_ocupavel40": 810.73},
    {"polegada": '2 1/2"', "diametro_mm": 65.00, "area_total": 3318.31,
      "area_ocupavel53":1758.70, "area_ocupavel31": 1028.68, "area_ocupavel40": 1327.32},
    {"polegada": '3"', "diametro_mm": 76.2 , "area_total": 4560.37,
      "area_ocupavel53":2416.99, "area_ocupavel31": 1413.71, "area_ocupavel40": 1824.15},
    {"polegada": '4"', "diametro_mm": 101.6, "area_total": 8107.32,
      "area_ocupavel53": 4296.88, "area_ocupavel31": 2513.27, "area_ocupavel40": 3242.93}

]

#===========================

# TABELA DE CONDUTORES

#===========================



condutores = {
    "PVC 750V 70°C CLASSE 2": [
        {"bitola": 1.5, "diametro_mm": 2.9, "area_mm2": 6.61},
        {"bitola": 2.5, "diametro_mm": 3.6, "area_mm2": 10.18},
        {"bitola": 4,   "diametro_mm": 4.1, "area_mm2": 13.20},
        {"bitola": 6,   "diametro_mm": 4.7, "area_mm2": 17.35},
        {"bitola": 10,  "diametro_mm": 6.1, "area_mm2": 29.22},
        {"bitola": 16,  "diametro_mm": 7.1, "area_mm2": 39.59},
        {"bitola": 25,  "diametro_mm": 8.7, "area_mm2": 59.45},
        {"bitola": 35,  "diametro_mm": 9.9, "area_mm2": 76.98},
        {"bitola": 50,  "diametro_mm": 11.6, "area_mm2": 105.68},
        {"bitola": 70,  "diametro_mm": 13.3, "area_mm2": 138.93},
        {"bitola": 95,  "diametro_mm": 15.5, "area_mm2": 188.69},
        {"bitola": 120, "diametro_mm": 17.0, "area_mm2": 226.98},
        {"bitola": 150, "diametro_mm": 19.5, "area_mm2": 298.65},
        {"bitola": 185, "diametro_mm": 21.0, "area_mm2": 346.36},
        {"bitola": 240, "diametro_mm": 24.7, "area_mm2": 479.16},
        {"bitola": 300, "diametro_mm": 27.4, "area_mm2": 589.65}
    ],
    "PVC 750V 70°C CLASSE 5": [
        {"bitola": 1.5, "diametro_mm": 2.9, "area_mm2": 6.61},
        {"bitola": 2.5, "diametro_mm": 3.5, "area_mm2": 9.62},
        {"bitola": 4,   "diametro_mm": 4.0, "area_mm2": 12.57},
        {"bitola": 6,   "diametro_mm": 4.6, "area_mm2": 16.62},
        {"bitola": 10,  "diametro_mm": 6.0, "area_mm2": 28.27},
        {"bitola": 16,  "diametro_mm": 7.0, "area_mm2": 38.48},
        {"bitola": 25,  "diametro_mm": 9.0, "area_mm2": 63.62},
        {"bitola": 35,  "diametro_mm": 10.0, "area_mm2": 78.54},
        {"bitola": 50,  "diametro_mm": 12.3, "area_mm2": 118.82},
        {"bitola": 70,  "diametro_mm": 13.6, "area_mm2": 145.27},
        {"bitola": 95,  "diametro_mm": 15.4, "area_mm2": 186.27},
        {"bitola": 120, "diametro_mm": 17.2, "area_mm2": 232.35},
        {"bitola": 150, "diametro_mm": 19.2, "area_mm2": 289.53},
        {"bitola": 185, "diametro_mm": 21.9, "area_mm2": 376.68},
        {"bitola": 240, "diametro_mm": 24.4, "area_mm2": 467.59},
        {"bitola": 300, "diametro_mm": 27.8, "area_mm2": 606.99},
        {"bitola": 400, "diametro_mm": 32.2, "area_mm2": 814.33},
        {"bitola": 500, "diametro_mm": 35.8, "area_mm2": 1006.60}
    ],

    "PVC 0,6 a 1kV 70°C CLASSE 2": [
        {"bitola": 2.5, "diametro_mm": 0.00, "area_mm2": 0.00},
        {"bitola": 4,   "diametro_mm": 0.00, "area_mm2": 0.00},
        {"bitola": 6,   "diametro_mm": 7.1, "area_mm2": 39.59},
        {"bitola": 10,  "diametro_mm": 8.1, "area_mm2": 51.53},
        {"bitola": 16,  "diametro_mm": 9.1, "area_mm2": 65.04},
        {"bitola": 25,  "diametro_mm": 10.9, "area_mm2": 93.31},
        {"bitola": 35,  "diametro_mm": 12.0, "area_mm2": 113.10},
        {"bitola": 50,  "diametro_mm": 14.0, "area_mm2": 153.94},
        {"bitola": 70,  "diametro_mm": 15.7, "area_mm2": 193.59},
        {"bitola": 95,  "diametro_mm": 17.9, "area_mm2": 251.65},
        {"bitola": 120, "diametro_mm": 19.8, "area_mm2": 307.91},
        {"bitola": 150, "diametro_mm": 22.2, "area_mm2": 387.08},
        {"bitola": 185, "diametro_mm": 24.4, "area_mm2": 467.59},
        {"bitola": 240, "diametro_mm": 27.2, "area_mm2": 581.07},
        {"bitola": 300, "diametro_mm": 30.4, "area_mm2": 725.83}
    ],

    "PVC 0,6 a 1kV 70°C CLASSE 5": [
        {"bitola": 1.5, "diametro_mm": 5.00, "area_mm2": 19.63},
        {"bitola": 2.5, "diametro_mm": 5.40, "area_mm2": 22.90},
        {"bitola": 4,   "diametro_mm": 6.50, "area_mm2": 33.18},
        {"bitola": 6,   "diametro_mm": 7.1, "area_mm2": 39.59},
        {"bitola": 10,  "diametro_mm": 8.0, "area_mm2": 50.27},
        {"bitola": 16,  "diametro_mm": 9.1, "area_mm2": 65.04},
        {"bitola": 25,  "diametro_mm": 11.2, "area_mm2": 98.52},
        {"bitola": 35,  "diametro_mm": 12.2, "area_mm2": 116.90},
        {"bitola": 50,  "diametro_mm": 14.7, "area_mm2": 169.72},
        {"bitola": 70,  "diametro_mm": 16.0, "area_mm2": 201.06},
        {"bitola": 95,  "diametro_mm": 18.0, "area_mm2": 254.47},
        {"bitola": 120, "diametro_mm": 20.0, "area_mm2": 314.16},
        {"bitola": 150, "diametro_mm": 22.0, "area_mm2": 380.13},
        {"bitola": 185, "diametro_mm": 24.7, "area_mm2": 479.16},
        {"bitola": 240, "diametro_mm": 27.6, "area_mm2": 598.28},
        {"bitola": 300, "diametro_mm": 31.4, "area_mm2": 774.37},
         {"bitola": 400, "diametro_mm": 35.6, "area_mm2": 995.38},
        {"bitola": 500, "diametro_mm": 39.6, "area_mm2": 1231.63}
    ],

    "PVC 0,6 a 1kV 90°C CLASSE 5": [
        {"bitola": 2.5, "diametro_mm": 0.00, "area_mm2": 0.00},
        {"bitola": 4,   "diametro_mm": 0.00, "area_mm2": 0.00},
        {"bitola": 6,   "diametro_mm": 0.00, "area_mm2": 0.00},
        {"bitola": 10,  "diametro_mm": 7.5, "area_mm2": 44.18},
        {"bitola": 16,  "diametro_mm": 8.6, "area_mm2": 58.09},
        {"bitola": 25,  "diametro_mm": 10.5, "area_mm2": 86.59},
        {"bitola": 35,  "diametro_mm": 11.5, "area_mm2": 103.87},
        {"bitola": 50,  "diametro_mm": 13.8, "area_mm2": 149.57},
        {"bitola": 70,  "diametro_mm": 15.4, "area_mm2": 186.27},
        {"bitola": 95,  "diametro_mm": 17.0, "area_mm2": 226.98},
        {"bitola": 120, "diametro_mm": 19.0, "area_mm2": 283.53},
        {"bitola": 150, "diametro_mm": 21.2, "area_mm2": 352.99},
        {"bitola": 185, "diametro_mm": 23.4, "area_mm2": 430.05},
        {"bitola": 240, "diametro_mm": 26.4, "area_mm2": 547.39},
        {"bitola": 300, "diametro_mm": 29.8, "area_mm2": 697.46},
        {"bitola": 400, "diametro_mm": 33.5, "area_mm2": 881.41},
        {"bitola": 500, "diametro_mm": 38.0, "area_mm2": 1134.11}
    ],    

    "XLPE 0,6 a 1kV 90°C CLASSE 2": [
        {"bitola": 2.5, "diametro_mm": 0.00, "area_mm2": 0.00},
        {"bitola": 4,   "diametro_mm": 0.00, "area_mm2": 0.00},
        {"bitola": 6,   "diametro_mm": 0.00, "area_mm2": 0.00},
        {"bitola": 10,  "diametro_mm": 7.1, "area_mm2": 39.59},
        {"bitola": 16,  "diametro_mm": 8.1, "area_mm2": 51.53},
        {"bitola": 25,  "diametro_mm": 9.1, "area_mm2": 65.04},
        {"bitola": 35,  "diametro_mm": 10.2, "area_mm2": 81.71},
        {"bitola": 50,  "diametro_mm": 12.3, "area_mm2": 118.82},
        {"bitola": 70,  "diametro_mm": 14.0, "area_mm2": 153.94},
        {"bitola": 95,  "diametro_mm": 15.6, "area_mm2": 191.13},
        {"bitola": 120, "diametro_mm": 17.9, "area_mm2": 251.65},
        {"bitola": 150, "diametro_mm": 19.2, "area_mm2": 289.53},
        {"bitola": 185, "diametro_mm": 21.3, "area_mm2": 356.33},
        {"bitola": 240, "diametro_mm": 23.6, "area_mm2": 437.44},
        {"bitola": 300, "diametro_mm": 26.7, "area_mm2": 559.90}
    ], 


    "REDE, TELEFONIA E ANTENA": [
        {"bitola": 'CAT 5E', "diametro_mm": 5.5, "area_mm2": 23.76},
        {"bitola": 'RG 6',   "diametro_mm": 7.1, "area_mm2": 39.93},
        {"bitola": 'CCI-50-2',   "diametro_mm": 5.0, "area_mm2": 19.63}
    ],

}

# ============================

# FUNÇÕES UTILITÁRIAS

# ============================
def area_condutor_por_tipo(tipo, bitola):
    tabela = condutores.get(tipo, [])
    for c in tabela:
        if str(c["bitola"]) == str(bitola):
            return c.get("area_mm2", 0.0)
    return None



def encontrar_eletroduto(area_total, n_condutores):
    if n_condutores == 1:
        chave = "area_ocupavel53"
    elif n_condutores == 2:
        chave = "area_ocupavel31"
    else:
        chave = "area_ocupavel40"

    for e in sorted(eletrodutos, key=lambda x: x[chave]):
        if area_total <= e[chave]:
            return e, chave
    return None, chave

#=========================

# INTERFACE STREAMLIT

#=========================

aba1, aba2 = st.tabs(["⚡ Calculadora ", "📘 Sobre/ Ajuda"])

with aba1:

    st.set_page_config(page_title="Dimensionamento de Eletrodutos", page_icon="⚡", layout="centered")
    st.markdown(
        """
        <h1 style="text-align:center;color:#1E90FF;">⚡ Dimensionamento de Eletrodutos</h1>
        <p style="text-align: center; color: gray;">Ferramenta para cálculo da ocupação de condutores em eletrodutos</p>
    <hr>
    """,
    unsafe_allow_html=True
    )
    #st.write("Adicione os condutores da instalação e clique em **Calcular eletroduto**.")

    # inicializações do session_state
    if "condutores_lista" not in st.session_state:
        st.session_state.condutores_lista = []

    #aba1, aba2 = st.tabs(["📥Inserir Dados", "📊Resultados"])

    # --- WIDGETS (com 'key' para poder resetar) ---
    # tipo_condutor
    st.selectbox("Tipo de condutor", options=list(condutores.keys()), key="tipo_condutor")

    # atualiza opções de bitola com base no tipo selecionado
    bitolas_disponiveis = [c["bitola"] for c in condutores[st.session_state.tipo_condutor]]

    # garante default válido para 'bitola' no session_state (só cria antes do widget, não modifica depois)
    if "bitola" not in st.session_state or str(st.session_state.bitola) not in [str(x) for x in bitolas_disponiveis]:
        st.session_state.bitola = bitolas_disponiveis[0]

    st.selectbox("Seção transversal mm² (bitola)", options=bitolas_disponiveis, key="bitola")

    # quantidade controlada
    if "quantidade" not in st.session_state:
        st.session_state.quantidade = 1
    st.number_input("Quantidade", min_value=1, key="quantidade")

    # --- AÇÃO: adicionar condutor ---
    if st.button("➕ Adicionar condutor"):
        # armazena tupla (tipo, bitola, quantidade)
        st.session_state.condutores_lista.append((st.session_state.tipo_condutor, st.session_state.bitola, st.session_state.quantidade))
        st.success(f"Adicionado: {st.session_state.quantidade} x {st.session_state.bitola} ({st.session_state.tipo_condutor})")

    # --- Mostrar lista adicionada (desempacotar 3 valores) ---
    if st.session_state.condutores_lista:
        st.markdown("### 📋 Condutores adicionados")
        #for tipo, b, q in st.session_state.condutores_lista:
            #st.write(f" - {q} x {b} mm² ({tipo})")

    # Exibir tabela com botão de remover
    for idx, (tipo, bitola, quantidade) in enumerate(st.session_state.condutores_lista):
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        with col1:
            st.write(tipo)
        with col2:
            st.write(f"{bitola} mm²")
        with col3:
            st.write(f"{quantidade} un.")
        with col4:
            if st.button("❌", key=f"remove_{idx}"):
                st.session_state.condutores_lista.pop(idx)
                st.rerun()

    # --- Calcular eletroduto somando todos os itens da lista ---
    if st.button("⚙️ Calcular eletroduto"):
        if not st.session_state.condutores_lista:
            st.warning("Adicione ao menos um condutor antes de calcular.")
        else:
            area_total = 0.0
            total_condutores = 0
            missing = []

            # percorre todos os itens adicionados
            for tipo, b, q in st.session_state.condutores_lista:
                area_item = area_condutor_por_tipo(tipo, b)
                if area_item is None:
                    missing.append((tipo, b))
                else:
                    area_total += area_item * q
                    total_condutores += q

            if missing:
                st.error(f"Não encontrei os seguintes condutores na tabela: {missing}. Verifique a seleção.")
            else:
                st.success(f"Área total ocupada: {area_total:.2f} mm²")
                eletro, chave = encontrar_eletroduto(area_total, total_condutores)
                if eletro:
                    percentual = chave.replace("area_ocupavel", "")
                    st.success(f"Eletroduto Permitido: {eletro['polegada']}") 
                    st.success(f"Área Ocupável ({percentual}%) -> {eletro[chave]:.2f} mm²") 
                    utilizacao = (area_total / eletro[chave]) * 100
                    st.info(f"Utilização da capacidade: {utilizacao:.1f}%")
                    st.info("📘 Cálculo conforme critérios de ocupação da NBR 5410:2004")
                    
                    # — Utilização: {utilizacao:.1f}%")
                else:
                    st.error("⚠️ Nenhum eletroduto disponível comporta essa área total. Considere múltiplos dutos ou verifique suas entradas.")

    # --- Reset: remover chaves dos widgets e limpar a lista ---
    st.markdown("---")
    if st.button("🔄 Novo Cálculo"):
        for k in ["tipo_condutor", "bitola", "quantidade", "condutores_lista"]:
            if k in st.session_state:
                del st.session_state[k]
                #st.session_state.condutores_lista = []
        # REMOVER as chaves que estão ligadas aos widgets para que, ao rerun, os widgets iniciem com os defaults
        st.rerun()
        

    #===========================

    # RODAPÉ

    # =========================    


    st.markdown("<hr><p style='text-align: center; color: gray;'>Desenvolvido por Deivison Dias ⚡<p/>", unsafe_allow_html=True)

#============================

# PÁGINA SOBRE/ AJUDA

#============================

with aba2:
    st.markdown("""
                ## 📘 Sobre esta ferramenta
    
    Esta aplicação foi desenvolvida para auxiliar no **dimensionamento de eletrodutos**,
    considerando as taxas máximas de ocupação de **53%, 31%, 40%** da área interna do eletroduto, conforme
    estabelecido na **NBR 5410:2004**.
    
    ---
    ### ✅ Pontos aplicados da NBR 5410
    
    - **Taxa de Ocupação dos eletrodutos**  
      *Item 6.2.11.1.6 – NBR 5410:2004*
        - 53% -> 1 condutor
        - 31% -> 2 condutores
        - 40% -> 3 ou mais condutores
                
    - **Limites de trechos contínuos de tubulação sem interposição de caixas ou equipamentos:**
        - 15 m em áreas internas
        - 30 m em áreas externas
        - Redução de 3 m para cada curva de 90°
                
    
    - **Classes e temperaturas dos cabos**  
      Condutores isolados em **PVC (70 °C)** e **XLPE (90 °C)** são considerados,
      conforme tabelas da NBR 5410.  
    
    ---
    ### ⚠️ Aviso de responsabilidade
    
    Esta ferramenta é um **apoio técnico**.  
    O resultado deve ser sempre analisado por um **profissional habilitado**, considerando
    as condições específicas da instalação.
    
    ---
    🔗 Para mais informações, consulte a norma completa: **ABNT NBR 5410:2004**.
    """)

    st.info("📘 Cálculo conforme critérios de ocupação pela NBR 5410:2004")
