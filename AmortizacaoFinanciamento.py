import pandas as pd
import math

class AmortizacaoFinanciamento:
    def __init__(self, total_financiado, taxa_juros, parcelas, ao_ano=True):
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

    def calcular_amortizacao(self):
        """
        Calcula o plano de amortização, considerando as amortizações extras.
        """
        amortizacao_constante = self.total_financiado / self.parcelas
        saldo_devedor = self.total_financiado
        historico = []
        parcela_num = 0

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

            # Atualiza o saldo devedor
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

            # Se o saldo devedor for menor que a amortização constante, ajusta o valor da última parcela
            if saldo_devedor <= 0:
                historico[-1]['Amortização do Mês'] += saldo_devedor  # Ajusta o saldo para 0
                break
        
        # Cria o DataFrame a partir da lista
        df = pd.DataFrame(historico)
        return df


if __name__ == "__main__":
    # Exemplo de uso da classe
    financiamento = AmortizacaoFinanciamento(total_financiado=240000, taxa_juros=10.49, parcelas=420)

    # Adicionando amortizações extras em meses específicos
    for i in range(420):
        if i % 12 == 0:
            financiamento.adicionar_amortizacao(mes=i, valor=15000)  # Amortização extra no mês 5
        if i % 24 == 0:
            financiamento.adicionar_amortizacao(mes=i, valor=50000)   # Amortização extra no mês 8
        # financiamento.adicionar_amortizacao(mes=i, valor=1200)

    # Calculando e mostrando o DataFrame
    df = financiamento.calcular_amortizacao()
    print(df)
    print(f"total pago: {df['Valor da Parcela'].sum()}")
    print(f"Total de juros acumulado: {df['Juros do Mês'].sum()}")