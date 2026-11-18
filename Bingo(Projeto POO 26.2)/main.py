import random
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Marcacao:
    jogador: str
    numero: int
    faltam: int

@dataclass
class Rodada:
    numero: int
    marcacoes: list[Marcacao]

class Observer(ABC):
   @abstractmethod
   def update(self, number: int) -> Marcacao | None:
       pass

class FonteNumeros(ABC):
    @abstractmethod
    def sortear_numero(self) -> int | None:
        pass


class Urna(FonteNumeros):
    def __init__(self, max: int = 75):
        self.balls = list(range(1, max + 1))
        random.shuffle(self.balls)

    def sortear_numero(self) -> int | None:
        if not self.balls:
            return None
        return self.balls.pop()


class Sorteio():
    class Sorteio:
    def __init__(self, fonte: FonteNumeros):
        self.observador: list[Observer] = []
        self.fonte = fonte
        self.sorteados: list[int] = []

    def adicionar(self, observer: Observer) -> None:
        if observer not in self.observador:
            self.observador.append(observer)

    def remover(self, observer: Observer) -> None:
        if observer in self.observador:
            self.observador.remove(observer)

    def notificar(self, number: int) -> list[Marcacao]:
        resultados = (obs.update(number) for obs in list(self.observador))
        return [r for r in resultados if r is not None]

    def sortear(self) -> Rodada | None:
        number = self.fonte.sortear_numero()

        if number is None:
            return None

        self.sorteados.append(number)
        marcacoes = self.notificar(number)
        return Rodada(number, marcacoes)


class Jogador(Observer):
    def __init__(self, name: str, qtd_numbers: int = 10, max: int = 75):
        self.name = name
        self.cartela = set(random.sample(range(1, max + 1), qtd_numbers))
        self.marcados: set[int] = set()

    @property
    def venceu(self) -> bool:
        return self.marcados == self.cartela

    def update(self, number: int) -> Marcacao | None:
        if number in self.cartela:
            self.marcados.add(number)
            faltam = len(self.cartela) - len(self.marcados)
            return Marcacao(self.name, number, faltam)

class Apresentador(ABC):

    @abstractmethod
    def mostrar_inicio(self) -> None:
        pass

    @abstractmethod
    def mostrar_cartelas(self, jogadores: list[Jogador]) -> None:
        pass

    @abstractmethod
    def mostrar_rodada(self, rodada: Rodada) -> None:
        pass

    @abstractmethod
    def mostrar_vencedores(self, vencedores: list[Jogador]) -> None:
        pass

    @abstractmethod
    def mostrar_fim(self) -> None:
        pass


class ApresentadorConsole(Apresentador):

    def mostrar_inicio(self) -> None:
        for c in "Bingo: ":
            print(c, end='', flush=True)
            time.sleep(0.2)
        print()
        time.sleep(1)

    def mostrar_cartelas(self, jogadores: list[Jogador]) -> None:
        print("Cartelas dos jogadores:")
        time.sleep(1)

        for j in jogadores:
            print(f"Cartela de {j.name}: {sorted(j.cartela)}")
            time.sleep(1)

    def mostrar_rodada(self, rodada: Rodada) -> None:
        print(f"\\nNumero sorteado: {rodada.numero}")
        time.sleep(2)

        for m in rodada.marcacoes:
            print(f"{m.jogador} marcou {m.numero} faltam {m.faltam}")
            time.sleep(2)

    def mostrar_vencedores(self, vencedores: list[Jogador]) -> None:
        print(
            "\\nBINGO! Vencedor(es):",
            ", ".join(j.name for j in vencedores)
        )

    def mostrar_fim(self) -> None:
        print("Acabaram as bolas!")
        
def jogar() -> None:
    urna = Urna(max=75)
    sorteador = Sorteio(urna)

    jogadores = [
        Jogador("Arlindo Lúcio da Silva", max=75),
        Jogador("Maria da Costa Gonçalves", max=75),
        Jogador("Geraldo Rodrigues de Souza", max=75)
    ]

    for j in jogadores:
        sorteador.adicionar(j)

    apresentador = ApresentadorConsole()

    apresentador.mostrar_inicio()
    apresentador.mostrar_cartelas(jogadores)

    while True:
        rodada = sorteador.sortear()

        if rodada is None:
            apresentador.mostrar_fim()
            break

        apresentador.mostrar_rodada(rodada)

        vencedores = [j for j in jogadores if j.venceu]

        if vencedores:
            apresentador.mostrar_vencedores(vencedores)
            break


if __name__ == "__main__":
    jogar()

