import io as _io

import pandas as _pandas
import requests as _requests
import taiga as _taiga

from .. import get_logger

logger = get_logger("Taiga")

_eng_projetos = [
    "ENT001.001 - Projeto de Ondulador Delta para a Linhas Sabiá",
    "ENT001.002 - Projeto para recuperação do Ondulador do UVX (backup Ipê - Sabiá)",
    "ENT001.003 - Projeto de Ondulador Delta de 2.4 metros",
    "ENT001.004 - Projeto de Ondulador Delta de 3.6 metros",
    "ENT001.005 - Projeto de Câmaras de Vácuo para Onduladores Delta 22",
    "ENT001.006 - Projeto de Câmaras de Vácuo para Onduladores Delta 52",
    "ENT001.007 - Projeto de Onduladores Planares",
    "ENT001.008 - Projeto de Ondulador Delta para a Linhas Carnaúba",
    "ENT002.001 - Projeto de amplificadores de potência de RF nacionais",
    "ENT002.002 - Projeto de Torres de RF para operação com da cavidade SC",
    "ENT002.003 - Projeto da Cavidade Harmônica do Sirius",
    "ENT002.004 - Projeto da Cavidade Supercondutora",
    "ENT003.001 - Projeto de ar-condicionado na Sala de Caracterização Magnética",
    "ENT003.002 - Projeto de organização de estoque e armazenagem da ENT",
    "ENT003.003 - Operação e Manutenção de Infraestruturas dos Laboratórios",
    "ENT004.001 - Instalações nos Aceleradores do Sirius",
    "ENT004.002 - Manutenção Preventiva e Corretiva dos Aceleradores do Sirius",
    "ENT005.001 - Projeto do Sistema de Intertravamento dos Aceleradores do Sirius",
    "ENT005.002 - Projeto de Sistema de Correção Rápida para o Sirius (FOFB)",
    "ENT005.003 - Projeto para alinhamento e monitoramento dos aceleradores",
    "ENT005.004 - Projeto do Pré-Font End Máquina",
    "ENT005.005 - Projeto de Sistemas de Monitoramento de Racks para o Sirius",
    "ENT005.006 - Apoio à operação ao Sirius",
    "ENT005.007 - Implementações e testes para operação top-up ",
    "ENT005.008 - Implementações e testes para melhorias da estabilidade do feixe",
    "ENT008.001 - Melhoramentos dos sistemas do LINAC do Sirius",
    "ENT008.002 - Dispositivos pulsados do Sirius ",
    "ENT008.003 - Melhoramentos do Canhão de Elétrons do Sirius",
    "ENT008.004 - Melhoramentos no Booster e Linhas de Transporte",
    "ENT009.001 - Projeto de Planta de Hélio Líquido no Sirius",
    "ENT009.002 - Projeto de sistema de distribuição nítrogênio líquido",
    "ENT011.001 - Projeto de Energização das linhas do faseamento",
    "ENT011.002 - Projeto de Alinhamento de Linhas de Luz XXXXX do Sirius",
    "ENT011.003 - Projeto de Brasagem de componentes para Linhas de Luz do Sirius",
    "ENT011.004 - LCA Laboratório de Ciências Ambientais (Carnaúba S8B5)",
    "ENT011.005 - LCRIO Laboratório de criogenia (Cateretê S8B3)",
    "ENT011.006 - Projeto de Ambiente para CryoLoading  Linha EMA",
    "ENT011.007 - Caracterizações dimensionais e geométricas de detectores e componentes de linhas",
    "ENT011.008 - Sistema de coleta de condensado por vácuo para o Sirius",
    "ENT011.009 - Readequação da fonte para a Linha EMA ",
    "ENT011.010 - Relayout da Sala 908G3 - Sirius",
    "ENT012.001 - Contratação de Empresa de Manutenção Predial do Sirius",
    "ENT012.002 - Projeto de Integração do sistema de incêndio do Sirius do campus",
    "ENT012.003 - Projeto para Renovação de AVCB do Sirius",
    "ENT012.004 - Garantia de obras do Sirius",
    "ENT012.005 - Manutenções Prediais Emergenciais do Sirius",
    "ENT013.001 - Projeto e instalação do sistemas de detecção de incêndio das linhas do Sirius",
    "ENT013.002 - Projeto e instalação de sistemas de exaustão do Sirius",
    "ENT013.003 - Projeto e instalação de sistemas de incêndio especiais (CPD e Carnaúba)",
    "ENT013.004 - Projeto para ampliação do sistema de controle de acessos do Sirius",
    "ENT013.005 - Projeto da Sala do Conselho no Sirius",
    "ENT013.006 - Projeto e Instalação de ar-condicionado na sala de racks do Sirius",
    "ENT013.007 - Projeto de Proteção da Marquise do Sirius",
    "ENT013.008 - Projeto de Revisão do sistema de monitoramento de câmeras do Sirius",
    "ENT013.009 - Projeto do Sistema de Abastecimento de Água (C6) do Sirius",
    "ENT013.010 - Instalações dos sistemas de TI para Salas Video Conferências do Sirius",
    "ENT014.001 - Projeto de recuperação dos Scrapers do Sirius",
    "ENT014.002 - Medição das curvas de excitação dos magnetos do Sirius",
    "ENT014.003 - Melhorias e Caracterização das Fontes do Sirius",
    "ENT014.004 - Projeto e construção de protótipo de conversor AC/DC tiristorizado",
    "ENT014.005 - Projeto da Nova Gaveta de Comando para as Fontes FAC",
    "ENT014.006 - Projeto e construção de protótipo de um novo estágio de saída FAC",
    "ENT014.007 - Projeto e construção de protótipo de fonte de alta corrente e baixa tensão",
    "ENT015.001 - Projeto de Descomissionamento do UVX",
    "ENT016.001 - Projeto de Dipolo Supercondutor (SCBC) para o Sirius - CERN",
    "ENT017.001 - Cursos e Treinamentos de Recursos Humanos",
    "ENT017.002 - Estudos e Desenvolvimentos Internos de Equipes",
    "ENT017.003 - Gestão de Equipes e Recursos Humanos",
    "ENT018.001 - Limpeza e Recuperação de bombas iônicas dos microscópios",
    "ENT018.002 - Desenvolvimento de soluções de automação, controle ou IoT para instalações laboratoriais ",
    "ENT020.001 - Projeto EXA",
    "ENT020.002 - Ciência aberta",
    "ENT020.003 - Atividades Administrativas Internas",
]


def _get_dataframe(url: str):
    return _pandas.read_csv(
        _io.StringIO(_requests.get(url, verify=False).content.decode("utf8"))
    )


_taiga_default_url = "https://10.0.38.59:9011/"

_gas_slug = "grupo-automacao-e-software"
_gas_equipes = ["SM", "TI", "Interlock", "Automação", "Automação dos Delta", "GAS"]
_gas_macro_atividades = [
    "Ansible",
    "Aplicações web no geral",
    "Avaliações de desempenho",
    "Cabeamento de rede",
    "Carrinhos de medição de radiação",
    "Component DB",
    "Computadores da sala de controle",
    "Computadores de trabalho",
    "Conexão da rede do sistema de controle",
    "Conteinerização de aplicações",
    "Contratação de pessoal",
    "DCCTs",
    "Descomissionamento do UVX",
    "Diagnósticos Sirius",
    "Dicionário de PVs",
    "EPICS Archiver",
    "Equipamentos de rede",
    "Espaços físicos para o grupo",
    "Estoque no Sirius",
    "FreeCAD",
    "Gestão das atividades do grupo com o Scrum",
    "HAProxy",
    "Hardware dos sistemas LLRF do booster e anel",
    "IOC das cavidades supercondutoras",
    "IOC das estações de bombeamento de vácuo",
    "IOC das fendas de energia",
    "IOC das gavetas de calibração",
    "IOC das screens do Linac",
    "IOC do sistema LLRF do Linac",
    "IOC do sistema de interlock",
    "IOC dos DCCTs do anel",
    "IOC dos circuladores de RF",
    "IOC dos osciloscópios Keysight",
    "IOC dos power sensors da RF",
    "IOC dos retificadores Regatron",
    "IOCs das torres de amplificadores de RF",
    "IOCs de CLPs Yokogawa",
    "IOCs do sistema de sincronismo",
    "IOCs dos ICTs",
    "IOCs dos detectores de radiação",
    "IOCs dos pulsados",
    "IOCs dos sistemas LLRF do booster e anel",
    "IOCs dos skids",
    "IOCs para o BMS",
    "Integração dos skids ao sistema de controle",
    "Interlock - Linac",
    "Interlock - MPS e PPS",
    "Interlock - MPS",
    "Interlock - PPS",
    "Interlock - RF",
    "Jupyter Lab",
    "Mesa de montagem automatizada dos sub-cassetes dos Delta",
    "Moduladores do Linac",
    "Monitores fluorescentes do Linac",
    "Motores da RF do Linac",
    "Motores do Linac",
    "Motorizados e Acq de Imagens",
    "Motorizados e Acq de imagens",
    "Motorizados",
    "Multímetros",
    "Módulo Python pyDRS",
    "Olog",
    "Onduladores Delta",
    "Onduladores Kyma",
    "Osciloscópios",
    "Outros",
    "Participação em conferências",
    "Portainer",
    "Processos seletivos",
    "Projeto EXA",
    "Projetos com entidades externas",
    "Recuperação da máquina",
    "Redundância da rede do sistema de controle",
    "Repositórios Git",
    "Sala de controle",
    "Servidores da RF",
    "Servidores",
    "Serviço DNS",
    "Serviço NTP",
    "Sistema de arquivamento para o FOFB",
    "Sistema de deposição de NEG",
    "Sistema de notificação de alarmes de PVs",
    "Sistema de sincronismo para as linhas Carcará",
    "Sistema de sincronismo para as linhas de luz",
    "Streak camera",
    "Suporte a outros grupos",
    "Taiga",
    "Telas de supervisório",
    "Torres de amplificadores de RF",
    "Treinamentos",
    "Visualizador web do EPICS Archiver",
    "Zabbix",
]


class TaigaClient:
    def __init__(
        self,
        host: str = _taiga_default_url,
        tls_verify: bool = False,
    ):
        self.api: _taiga.TaigaAPI = _taiga.TaigaAPI(host=host, tls_verify=tls_verify)

    def initialize_project(self, slug: str = _gas_slug):
        project = self.api.projects.get_by_slug(slug)
        self._add_user_story_attributes(project)

    def _add_user_story_attributes(self, project: _taiga.models.Project):
        project.add_user_story_attribute(
            "Projeto",
            description="Projetos válidos da ENG",
            type="dropdown",
            extra=_eng_projetos,
        )
        project.add_user_story_attribute(
            "Macro-atividade",
            description="Macro-atividade da user history",
            type="dropdown",
            extra=_gas_macro_atividades,
        )
        project.add_user_story_attribute(
            "Prioridade Mapeada",
            description="Valor da prioridade (int) utilizada na planilha",
            type="number",
        )
        project.add_user_story_attribute(
            "Variação de pontuação",
            description="Variação de pontuação da atividade durante o sprint",
            type="number",
        )
        project.add_user_story_attribute(
            "Nova?",
            description="Atividade nova no sprint, imprevista",
            type="checkbox",
        )
        project.add_user_story_attribute(
            "Dependências / Condições para a atividade",
            description="Dependências / Condições para a atividade, repersentação textual que será integrada na planilha geral da ENG",
            type="text",
        )
        project.add_user_story_attribute(
            "Nome da Equipe",
            description="Equipe Interna do grupo",
            type="dropdown",
            extra=_gas_equipes,
        )
        project.add_user_story_attribute(
            "Grupo",
            description="Grupos envolvidos",
            type="text",
        )

    def auth(
        self,
        username: str,
        password: str,
    ):
        self.api.auth(username, password)

    def to_excel_table(self, df: _pandas.DataFrame, filename: str = "table.xlsx"):
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = _pandas.ExcelWriter(filename, engine="xlsxwriter")

        # Write the dataframe data to XlsxWriter. Turn off the default header and
        # index and skip one row to allow us to insert a user defined header.
        df.to_excel(
            writer, sheet_name="user_stories", startrow=1, header=False, index=False
        )

        # Get the xlsxwriter workbook and worksheet objects.
        worksheet = writer.sheets["user_stories"]

        # Get the dimensions of the dataframe.
        (max_row, max_col) = df.shape

        # Create a list of column headers, to use in add_table().
        column_settings = [{"header": column} for column in df.columns]

        # Add the Excel table structure. Pandas will add the data.
        worksheet.add_table(0, 0, max_row, max_col - 1, {"columns": column_settings})

        # Make the columns wider for clarity.
        worksheet.set_column(0, max_col - 1, 12)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

    def get_stories_df(self, slug: str = _gas_slug):
        project = self.api.projects.get_by_slug(slug)
        userstories_csv_uuid = project.userstories_csv_uuid
        if not userstories_csv_uuid:
            msg = f"Project '{slug}' does not have a user story report enabled. Please enable it using the Taiga front-end before continuing."
            raise Exception(msg)

        userstories_csv_url = (
            f"{self.api.host}/api/v1/userstories/csv?uuid={userstories_csv_uuid}"
        )

        logger.info(f"Using User Story Report '{userstories_csv_url}'")
        stories_df = _get_dataframe(userstories_csv_url)

        filtered_df = stories_df.rename(
            columns={
                "assigned_users_full_name": "Membros Atribuidos",
                "description": "Descrição",
                "id": "Taiga Story ID",
                "sprint": "Sprint",
                "status": "Status",
                "subject": "Atividades",
                "tags": "Taiga Tags",
                "tasks": "Taiga Tasks ID",
                "total-points": "Número de Pontos",
            }
        )

        columns = [
            "Projeto",
            "Prioridade Mapeada",
            "Macro-atividade",
            "Atividades",
            "Status",
            "Número de Pontos",
            "Grupo",
            "Nome da Equipe",
            "Descrição",
            "Dependências / Condições para a atividade",
            "Variação de pontuação",
            "Nova?",
            "Membros Atribuidos",
            "Sprint",
            "Taiga Story ID",
            "Taiga Tasks ID",
            "Taiga Tags",
        ]
        output_df = filtered_df[columns]
        output_df["Sprint"].fillna("Backlog", inplace=True)
        output_df["Prioridade Mapeada"].fillna(500, inplace=True)
        output_df["Grupo"].fillna("GAS", inplace=True)
        output_df["Nome da Equipe"].fillna("GAS", inplace=True)

        output_df["Nova?"].fillna("Não", inplace=True)
        mask = output_df["Nova?"] == True  # noqa: E712
        output_df.loc[mask, "Nova?"] = "Sim"
        mask = output_df["Nova?"] == False  # noqa: E712
        output_df.loc[mask, "Nova?"] = "Não"

        output_df.fillna("", inplace=True)
        return output_df
