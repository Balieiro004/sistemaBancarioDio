from abc import ABC, abstractmethod
from datetime import date, datetime


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass
    

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historio.adiconar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historio.adiconar_transacao(self)

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historio()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico


    def sacar(self, valor):
        saldo = self.saldo

        if valor > saldo:
            print(f"Saldo insuficiente")

        elif valor <= saldo and saldo > 0:
            saldo -= valor
            extrato += f"Saque R$ {valor:.2f} horário {datetime.now()}\n"
            numero_saques += 1
            print(f"Saque de {valor} realizado, Seu novo saldo é: {saldo}")
            print(datetime.now())
            return True

        else:
            print("Saldo indiponivel")

        return False
    
    def depositar(self, valor):
                
        if (valor > 0):
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f} horario {datetime.now()}\n"
        else:
              print(f"Por favor insira um saldo maior que 0")
              return False

        print(f"Seu saldo é: {saldo}")
        return True
       
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        
        if valor > saldo:
            print(f"Saldo insuficiente")

        elif valor > self.limite:
            print(f"O valor excede o limite.")

        elif numero_saques >= self.limite_saques:
            print("Número de saques excedido")

        else:
            return super().sacar(valor)

        return False
    
    def __str__(self):
        return f"""Agencia: {self.agencia}
                    C/C: {self.numero}
                    Titular: {self.cliente.nome}
                """

class Historio:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

