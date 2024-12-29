import pandas as pd
import math

class AmortizacaoFinanciamento:
    def __init__(self, total_financiado, taxa_juros, parcelas, ao_ano=True, congelar_parcela_inicial=False):
        """
        Inicializa a classe com o valor total financiado, a taxa de juros mensal (taxa_juros),
        e o número de parcelas (parcelas).
        """
        self.total_financiado = total_financiado
        self.taxa_juros = taxa_juros / 100
        if ao_ano:
            self.taxa_juros = (taxa_juros / 100) / 12  # Converte a taxa de juros para formato decimal
        self.parcelas = parcelas
        self.saldo_devedor = total_financiado
        self.amortizacoes_extras = {}  # Armazena amortizações extras
        self.congelar_parcela_inicial = congelar_parcela_inicial

    def adicionar_amortizacao(self, mes, valor):
        """
        Adiciona uma amortização extra em um mês específico.
        """
        if valor > self.saldo_devedor:
            valor = self.saldo_devedor
        if mes in self.amortizacoes_extras:
            self.amortizacoes_extras[mes] += valor
        else:
            self.amortizacoes_extras[mes] = valor

    def calcular_amortizacao(self, teste=False):
        """
        Calcula o plano de amortização, considerando as amortizações extras.
        """
        amortizacao_constante = self.total_financiado / self.parcelas
        saldo_devedor = self.total_financiado
        historico = []
        parcela_num = 0
        parcela_inicial = 0
        dif_parcela_inicial = 0

        while saldo_devedor > 0 and parcela_num < self.parcelas:
            parcela_num += 1

            # Verifica se há amortização extra no mês
            amortizacao_extra = self.amortizacoes_extras.get(parcela_num, 0)

            # Amortização do mês (constante) + amortização extra
            amortizacao = amortizacao_constante + amortizacao_extra

            # Calcula os juros do mês com base no saldo devedor
            juros = saldo_devedor * self.taxa_juros

            # Valor da parcela (amortização + juros)
            valor_parcela = amortizacao + juros
            if parcela_num == 1:
                parcela_inicial = valor_parcela
            else:
                dif_parcela_inicial = parcela_inicial - valor_parcela

            # Atualiza o saldo devedor
            if self.congelar_parcela_inicial:
                amortizacao_extra += dif_parcela_inicial
                amortizacao = amortizacao_constante + amortizacao_extra
                valor_parcela = amortizacao + juros
            saldo_devedor -= amortizacao

            # Armazena os dados do mês
            historico.append({
                'Mês': parcela_num,
                'Juros do Mês': round(juros, 2),
                'Amortização do Mês': round(amortizacao, 2),
                'Amortização Extra': round(amortizacao_extra, 2),
                'Valor da Parcela': round(valor_parcela, 2),
                'Saldo Devedor': round(max(saldo_devedor, 0), 2)
            })

            if teste:
                if parcela_num > 10:
                    break
            # Se o saldo devedor for menor que a amortização constante, ajusta o valor da última parcela
            if saldo_devedor <= 0:
                historico[-1]['Amortização do Mês'] += saldo_devedor  # Ajusta o saldo para 0
                break
        
        # Cria o DataFrame a partir da lista
        df = pd.DataFrame(historico)
        return df


if __name__ == "__main__":
    # Exemplo de uso da classe
    valor_imovel = 439999
    valor_venda_imovel = 410000
    taxa_entrada = 0.3
    fgts = 62156
    # entrada = valor_imovel * taxa_entrada
    total_financiado = valor_imovel * (1 - taxa_entrada)
    entrada_venda = valor_venda_imovel - total_financiado
    # entrada_financiada = (valor_imovel - entrada) - (valor_venda_imovel - entrada_venda)
    # esquema = entrada_venda - entrada_financiada
    financiamento = AmortizacaoFinanciamento(total_financiado=total_financiado, taxa_juros=9.79, parcelas=420, congelar_parcela_inicial=False)

    taxas_cartorio = valor_imovel * 0.0555

    # Adicionando amortizações extras em meses específicos
    for i in range(420):
        # if i == 1:
        #     financiamento.adicionar_amortizacao(mes=i, valor=50000)
        if i % 12 == 0:
            financiamento.adicionar_amortizacao(mes=i, valor=10000)  # Amortização extra no mês 12
        if i % 24 == 0:
            financiamento.adicionar_amortizacao(mes=i, valor=50000)   # Amortização extra bienal FGTS
        # Amortizacao mensal a partir do 5 mes
        if i > 12:
            financiamento.adicionar_amortizacao(mes=i, valor=1000)

    # Calculando e mostrando o DataFrame
    df = financiamento.calcular_amortizacao()
    print(df)
    print(f"Total do imóvel: R${valor_imovel}")
    print(f"Valor da entrada: R${entrada_venda}")
    print(f"Valor das taxas de cartório (5.50%): R${taxas_cartorio}")
    print(f"Total FGTS: {fgts}")
    print(f"Total upfront: R${(entrada_venda + taxas_cartorio) - fgts}")
    print(f"Valor financiado: R${total_financiado}")
    print(f"Total pago do financiamento: {df['Valor da Parcela'].sum()}")
    print(f"Total de juros acumulado: {df['Juros do Mês'].sum()}")
    print(f"Total pago: R${entrada_venda + df['Valor da Parcela'].sum() + taxas_cartorio}")
    print(f"Tempo total do financiamento: {len(df)} meses, ({len(df) / 12} anos).")
    df.to_csv("simulacao_financiamento.csv")