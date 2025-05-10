from typing import List, Dict, Any, Callable, Optional
from graficos.controllerEvent import ControllerEvent
from graficos.IUserView import IUserView
from graficos.ILogger import ILogger

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import traceback
import os

# =============================================================================
# Eventos Utilizados pelo Model
# =============================================================================

class FicheiroInvalidoEvt(ControllerEvent):
    """
    Evento emitido quando ocorre algum erro relacionado com o ficheiro.
    Os handlers subscritos recebem uma mensagem (string) a explicar o erro.
    """
    def add_handler(self, handler: Callable[[str], None]) -> None:
        super().add_handler(handler)
    def invoke(self, mensagem: str) -> None:
        super().invoke(mensagem)

class EstadoProcessamentoEvt(ControllerEvent):
    """
    Evento para notificar alterações no estado do processamento.
    Ex.: "Início da importação", "Processamento concluído", "Gravação concluída", etc.
    """
    def add_handler(self, handler: Callable[[str], None]) -> None:
        super().add_handler(handler)
    def invoke(self, estado: str) -> None:
        super().invoke(estado)

class ImportacaoConcluidaEvt(ControllerEvent):
    """
    Evento para notificar que a importação foi concluída com sucesso.
    (Sem argumentos)
    """
    def add_handler(self, handler: Callable[[], None]) -> None:
        super().add_handler(handler)
    def invoke(self) -> None:
        super().invoke()

class GraficoGravadoEvt(ControllerEvent):
    """
    Evento para notificar que a gravação do gráfico foi concluída com sucesso.
    (Sem argumentos)
    """
    def add_handler(self, handler: Callable[[], None]) -> None:
        super().add_handler(handler)
    def invoke(self) -> None:
        super().invoke()

class GraficoDisponivelEvt(ControllerEvent):
    """
    Evento para notificar que existem gráficos disponíveis após a importação.
    Os handlers recebem a lista de gráficos.
    """
    def add_handler(self, handler: Callable[[List[str]], None]) -> None:
        super().add_handler(handler)
    def invoke(self, lista_graficos: List[str]) -> None:
        super().invoke(lista_graficos)

class GraficoGeradoEvt(ControllerEvent):
    """
    Evento emitido quando o gráfico está gerado e pronto para ser mostrado.
    Os handlers recebem uma lista de strings com os gráficos disponíveis.
    """
    def add_handler(self, handler: Callable[[List[str]], None]) -> None:
        super().add_handler(handler)
    def invoke(self) -> None:
        super().invoke()

# --- Novos eventos para diferenciar os tipos de falha ---
class FalhaImportacaoEvt(ControllerEvent):
    """
    Evento para notificar que ocorreu uma falha de importação (dados/ficheiro).
    Os handlers recebem uma mensagem específica de falha de importação.
    """
    def add_handler(self, handler: Callable[[str], None]) -> None:
        super().add_handler(handler)
    def invoke(self, mensagem: str) -> None:
        super().invoke(mensagem)

class FalhaGravacaoEvt(ControllerEvent):
    """
    Evento para notificar que ocorreu uma falha na gravação do gráfico.
    Os handlers recebem uma mensagem específica de falha na gravação.
    """
    def add_handler(self, handler: Callable[[str], None]) -> None:
        super().add_handler(handler)
    def invoke(self, mensagem: str) -> None:
        super().invoke(mensagem)

class FalhaGeracaoEvt(ControllerEvent):
    """
    Evento para notificar que ocorreu uma falha durante a geração do gráfico.
    Os handlers recebem uma mensagem específica de falha de geração.
    """
    def add_handler(self, handler: Callable[[str], None]) -> None:
        super().add_handler(handler)
    def invoke(self, mensagem: str) -> None:
        super().invoke(mensagem)

# --- Para simular o Throw do C# ---
class ErroInternoEvt(ControllerEvent):
    """
    Evento para notificar erros internos com stack trace.
    A View pode decidir se quer mostrar esta mensagem ou apenas guardar.
    """
    def add_handler(self, handler: Callable[[str], None]) -> None:
        super().add_handler(handler)
    def invoke(self, stacktrace: str) -> None:
        super().invoke(stacktrace)

# =============================================================================
# Classe Model
# =============================================================================

class Model:
    def __init__(self, view: IUserView, logger: ILogger) -> None:
        self.view = view
        self.logger = logger
        self.dados: List[Dict[str, Any]] = []   # Armazena os dados importados
        self.graficos: List[str] = []             # Lista de gráficos gerados
        self.__figura: Optional[plt.Figure] = None  # Figura gerada para posterior gravação

        # Existe Handlers para tratamentos específicos e restantes são tratados como genericos
        # Eventos de sucesso e estado
        self.__estado_processamento_evt: EstadoProcessamentoEvt = EstadoProcessamentoEvt()
        self.__estado_processamento_evt.add_handler(view.mostra_mensagem_info)
        self.__importacao_concluida_evt: ImportacaoConcluidaEvt = ImportacaoConcluidaEvt()
        self.__grafico_gravado_evt: GraficoGravadoEvt = GraficoGravadoEvt()
        self.__grafico_disponivel_evt: GraficoDisponivelEvt = GraficoDisponivelEvt()
        self.__grafico_disponivel_evt.add_handler(view.atualiza_lista_graficos)
        self.__grafico_gerado_evt: GraficoGeradoEvt = GraficoGeradoEvt()
        self.__grafico_gerado_evt.add_handler(view.mostrar_grafico)
        
        # Eventos para falhas diferenciadas
        #TODO: Dividir o evento genérico de ficheiro inválido, em diversos eventos
        self.__falha_importacao_evt: FalhaImportacaoEvt = FalhaImportacaoEvt()
        self.__falha_importacao_evt.add_handler(view.mostra_erro_importacao)
        self.__falha_gravacao_evt: FalhaGravacaoEvt = FalhaGravacaoEvt()
        self.__falha_geracao_evt : FalhaGeracaoEvt = FalhaGeracaoEvt()

        # Evento genérico de ficheiro inválido:
        self.__ficheiro_invalido_evt: FicheiroInvalidoEvt = FicheiroInvalidoEvt()
        self.__ficheiro_invalido_evt.add_handler(view.mostra_erro_ficheiro)

        # Evento para erros internos (simulando o Throw do C#)
        self.__erro_interno_evt : ErroInternoEvt = ErroInternoEvt()

    # =========================================================================
    # Propriedades para acesso aos eventos
    # =========================================================================

    @property
    def estado_processamento_evt(self) -> EstadoProcessamentoEvt:
        return self.__estado_processamento_evt

    @property
    def importacao_concluida_evt(self) -> ImportacaoConcluidaEvt:
        return self.__importacao_concluida_evt

    @property
    def grafico_gravado_evt(self) -> GraficoGravadoEvt:
        return self.__grafico_gravado_evt

    @property
    def grafico_disponivel_evt(self) -> GraficoDisponivelEvt:
        return self.__grafico_disponivel_evt

    @property
    def falha_importacao_evt(self) -> FalhaImportacaoEvt:
        return self.__falha_importacao_evt

    @property
    def falha_gravacao_evt(self) -> FalhaGravacaoEvt:
        return self.__falha_gravacao_evt

    @property
    def ficheiro_invalido_evt(self) -> FicheiroInvalidoEvt:
        return self.__ficheiro_invalido_evt
    
    @property
    def falha_geracao_evt(self) -> FalhaGeracaoEvt: 
        return self.__falha_geracao_evt
    
    @property
    def erro_interno_evt(self) -> ErroInternoEvt: 
        return self.__erro_interno_evt
    
    @property
    def grafico_gerado_evt(self) -> GraficoGeradoEvt:
        return self.__grafico_gerado_evt


    # =========================================================================
    # Métodos de Notificação (Invokes encapsulados)
    # =========================================================================

    def mensagem_estado_processamento(self, estado: str) -> None:
        """
        Notifica os interessados de uma alteração no estado do processamento.
        (Ex.: "Início da importação", "Processamento concluído", etc.)
        """
        self.__estado_processamento_evt.invoke(estado)

    def mensagem_importacao_concluida(self) -> None:
        """
        Notifica que a importação foi concluída com sucesso.
        """
        self.__importacao_concluida_evt.invoke()

    def mensagem_grafico_gravado(self) -> None:
        """
        Notifica que a gravação do gráfico foi concluída com sucesso.
        """
        self.__grafico_gravado_evt.invoke()

    def notifica_graficos_disponiveis(self) -> None:
        """
        Notifica que existem gráficos disponíveis (por exemplo, "Barras", "Linhas", "Pizza").
        """
        self.__grafico_disponivel_evt.invoke(self.graficos)

    # --- Novos métodos de notificação de falhas diferenciadas ---
    def mensagem_falha_importacao(self, mensagem: str = "Falha de importação do ficheiro.") -> None:
        """
        Notifica que ocorreu uma falha específica na importação.
        """
        self.__falha_importacao_evt.invoke(mensagem)

    def mensagem_falha_gravacao(self, mensagem: str = "Falha na gravação do gráfico.") -> None:
        """
        Notifica que ocorreu uma falha específica na gravação.
        """
        self.__falha_gravacao_evt.invoke(mensagem)

    def mensagem_falha_geracao (self, mensagem: str = "Falha na geração do gráfico.") -> None:
        """
        Notifica que ocorreu uma falha específica na geração do gráfico.
        """
        self.__falha_geracao_evt.invoke(mensagem)

    # =========================================================================
    # Métodos de dados (Importação, Geração, Gravação)
    # =========================================================================

    def importar_ficheiro(self, caminho: str) -> None:
        """
        Importa e processa o ficheiro de dados.        
        :param caminho: Caminho do ficheiro a importar.
        """
        #TODO: Adicionar validação para o tamanho máximo de ficheiro
        MAX_TAMANHO_MB = 10  # Tamanho máximo em MB

        self.mensagem_estado_processamento("Início da importação")
        self.logger.log_info("importar_ficheiro() - Início da importação")
        try:
            if not caminho.endswith(".csv"):
                self.__ficheiro_invalido_evt.invoke("Ficheiro selecionado não é CSV.")
                self.logger.log_erro("importar_ficheiro() - Ficheiro não é CSV")
                return

            # Validação do tamanho do ficheiro (em bytes)
            tamanho_bytes = os.path.getsize(caminho)
            tamanho_mb = tamanho_bytes / (1024 * 1024)
            # Verifica se o tamanho do ficheiro excede o máximo permitido
            if tamanho_mb > MAX_TAMANHO_MB:
                self.__ficheiro_invalido_evt.invoke(f"O ficheiro excede o tamanho máximo de {MAX_TAMANHO_MB} MB.")
                self.logger.log_erro(f"importar_ficheiro() - Ficheiro excede {MAX_TAMANHO_MB} MB")
                return

            self.dados = pd.read_csv(caminho).to_dict(orient="records")
            self.logger.log_info(f"importar_ficheiro() - {len(self.dados)} registos carregados do CSV")

            df = pd.DataFrame(self.dados)

            # Verifica se o DataFrame contém as colunas necessárias
            # Neste momento está fixo porém podemos por a view a enviar esses valores.            
            if "Categoria" not in df.columns or "Valor" not in df.columns:
                self.mensagem_falha_importacao("Ficheiro CSV mal formatado.")
                self.logger.log_erro("importar_ficheiro() - Ficheiro CSV mal formatado (faltam colunas obrigatórias)")
                return                        
            
            if not self.dados:
                self.mensagem_falha_importacao("Ficheiro CSV está vazio.")
                self.logger.log_erro("importar_ficheiro() - Ficheiro CSV está vazio")
                return

            # Atualiza os gráficos disponíveis (exemplo fixo para já)
            self.graficos = ["Barras", "Linhas"]
            self.notifica_graficos_disponiveis()
            self.mensagem_importacao_concluida()
            self.mensagem_estado_processamento("Importação concluída")

        except pd.errors.EmptyDataError:
        # CSV completamente vazio: ficheiro vazio!
            self.mensagem_falha_importacao("Ficheiro CSV está vazio.")
            self.logger.log_erro("importar_ficheiro() - Ficheiro CSV está vazio")

        except Exception as e:
            stacktrace = traceback.format_exc()
            # 1. Evento técnico (equivalente ao throw ex no C#)
            self.__erro_interno_evt.invoke(stacktrace)
            # 2. Evento funcional amigável (mensagem para a View)
            self.mensagem_falha_importacao(f"Erro ao importar: {str(e)}")
            self.logger.log_erro(f"importar_ficheiro() - Erro inesperado: {str(e)}")

    def gerar_grafico(self, tipo: str, x: str, y: str, x_label: Optional[str] = "", y_label: Optional[str] = "", titulo: Optional[str] = "") -> None:
        """
        Gera um gráfico a partir dos dados importados.
        Armazena internamente a figura para posterior gravação.
        """
        self.mensagem_estado_processamento("A gerar gráfico")
        self.logger.log_info(f"gerar_grafico() - A gerar gráfico do tipo '{tipo}'")
        try:
            if not self.dados:
                self.mensagem_falha_geracao("Não há dados para gerar gráfico.")
                self.logger.log_erro("gerar_grafico() - Não há dados para gerar gráfico")
                return

            df = pd.DataFrame(self.dados)

            plt.figure(figsize=(6, 4))
            if tipo.lower() == "barras":
                sns.barplot(x="Categoria", y="Valor", data=df)
            elif tipo.lower() == "linhas":
                sns.lineplot(x="Categoria", y="Valor", data=df)
            else:
                self.mensagem_falha_geracao(f"Tipo de gráfico não suportado: {tipo}")
                self.logger.log_erro(f"gerar_grafico() - Tipo de gráfico não suportado: {tipo}")
                return

            # Adiciona labels e título
            plt.xlabel(x_label or x)
            plt.ylabel(y_label or y)
            plt.title(titulo or "Gráfico")
            plt.tight_layout()
            self.__figura = plt.gcf()

            self.mensagem_estado_processamento("Gráfico gerado com sucesso")
            self.logger.log_info("gerar_grafico() - Gráfico gerado com sucesso")
            self.__grafico_gerado_evt.invoke()
            self.mensagem_estado_processamento("Gráfico pronto para visualização")  

        except Exception as e:
            stacktrace = traceback.format_exc()

            # 1. Evento técnico (equivalente ao throw ex no C#)
            self.__erro_interno_evt.invoke(stacktrace)
            # 2. Evento funcional amigável (mensagem para a View)
            self.mensagem_falha_geracao(f"Erro ao gerar gráfico: {str(e)}")
            self.logger.log_erro(f"gerar_grafico() - Erro inesperado: {str(e)}")
        finally:
            # Garante que fecha qualquer figura temporária se houve erro
            if self.__figura is None:
                plt.close()


    def get_colunas_disponiveis(self) -> list[str]:
        """
        Retorna uma lista com os nomes das colunas disponíveis nos dados importados.    
        Se não houver dados, retorna uma lista vazia.
        """
        if not self.dados:
            return []
        return list(pd.DataFrame(self.dados).columns)
    

    def gravar_grafico(self, caminho: str) -> None:
        """
        Grava a figura do gráfico previamente gerada.
        """
        self.mensagem_estado_processamento("Início da gravação do gráfico")
        self.logger.log_info(f"gravar_grafico() - A gravar gráfico em: {caminho}")

        try:
            if self.__figura is None:
                self.mensagem_falha_gravacao("Nenhum gráfico foi gerado.")
                self.logger.log_erro("gravar_grafico() - Nenhum gráfico foi gerado")
                return

            self.__figura.savefig(caminho)
            self.mensagem_grafico_gravado()
            self.mensagem_estado_processamento("Gravação concluída")
            self.logger.log_info("gravar_grafico() - Gravação concluída com sucesso")
        except Exception as e:
            stacktrace = traceback.format_exc()

            # 1. Evento técnico (equivalente ao throw ex no C#)
            self.__erro_interno_evt.invoke(stacktrace)
            # 2. Evento funcional amigável (mensagem para a View)
            self.mensagem_falha_gravacao(f"Erro ao gravar gráfico: {str(e)}")
            self.logger.log_erro(f"gravar_grafico() - Erro inesperado: {str(e)}")
        finally:
            # Garante limpeza de recursos mesmo em caso de erro
            plt.close(self.__figura)
            self.__figura = None
