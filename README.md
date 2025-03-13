# MurMurHash3
Python para filtrar UUID dentro da AllowList pelo MurMurHash3

Implementação python para:
1. Ler um arquivo CSV de UUIDs, 
2. Aplicar o MurMurHash3_x86_32 igual o site padrão usado
3. Gerar a porcentagem de 0 a 100% baseado na saída do item anterior (divisão pelo MAX_UINT32)
4. Filtragem da lista de UUIDs, aplicando a allow-list (threshold)
5. Exportar os UUIDs "dentro da allow-list" (<= do que o threshold)

## Getting Started

Clone the repository, compile and run it.

### Clone

```
git clone https://github.com/EduardoCulau/MurMurHash3.git
```

### Módulos Necessários
1. numpy
2. sys
3. csv
4. mmh3
5. pandas -> opcional, mas recomendado

### Arquivos de Entrada
Um CSV com UUIDs na primeira e *única coluna*
