import pandas as pd

class JurosCompostos:
    def __init__(self, principal, taxa_juros, meses, aporte_mensal=0, ao_ano=True):
        """
        Inicializa a classe com o valor inicial (principal), taxa de juros mensal (taxa_juros),
        número de meses (meses) e o valor do aporte mensal.
        """
        self.principal = principal
        self.ao_ano = ao_ano
        self.taxa_juros = taxa_juros / 100
        if ao_ano:
            self.taxa_juros = (taxa_juros / 100) / 12  # Converte a taxa de juros para formato decimal
        self.meses = meses
        self.aporte_mensal = aporte_mensal
        self.incrementos = {}  # Armazena incrementos específicos para meses

    def adicionar_incremento(self, mes, valor):
        """
        Adiciona um incremento em um mês específico.
        """
        if mes in self.incrementos:
            self.incrementos[mes] += valor
        else:
            self.incrementos[mes] = valor

    def calcular(self):
        """
        Calcula os valores de juros compostos e retorna um DataFrame com os detalhes mensais.
        """
        # Lista para armazenar os dados mensais
        historico = []
        saldo = self.principal
        
        for mes in range(1, self.meses + 1):
            juros = saldo * self.taxa_juros
            aporte = self.aporte_mensal
            
            # Verifica se há um incremento para o mês
            if mes in self.incrementos:
                aporte += self.incrementos[mes]
            
            saldo += juros + aporte
            
            # Armazena os dados do mês
            historico.append({
                'Mês': mes,
                'Juros do Mês': round(juros, 2),
                'Aporte do Mês': round(aporte, 2),
                'Total Juros': round(sum([h['Juros do Mês'] for h in historico]), 2),
                'Total Aporte': round(sum([h['Aporte do Mês'] for h in historico]), 2),
                'Saldo Total': round(saldo, 2)
            })
        
        # Cria o DataFrame a partir da lista
        df = pd.DataFrame(historico)
        return df


if __name__ == "__main__":
    # Exemplo de uso da classe
    periodo = 72
    juros_compostos = JurosCompostos(principal=50000, taxa_juros=15, ao_ano=True, meses=periodo, aporte_mensal=500)

    # Adicionando incrementos específicos
    for i in range(1, periodo):
        if i % 12 == 0:
            juros_compostos.adicionar_incremento(mes=i, valor=15000)  # Incremento no mês 6
    # Calculando e mostrando o DataFrame
    df = juros_compostos.calcular()
    print(df)
