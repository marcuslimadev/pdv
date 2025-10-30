# Sistema de Aparência Personalizável

## Visão Geral

O sistema PDV agora possui um módulo completo de personalização visual que permite ao administrador configurar:

- **Cores** (primária, secundária, destaque, perigo, info, aviso, texto, fundo)
- **Fontes** (família e tamanhos)
- **Logotipo** (imagem customizada)
- **Bordas** (arredondamento)

Todas as configurações são armazenadas no banco de dados e aplicadas dinamicamente em todo o sistema.

## Como Usar

### 1. Acessar Configurações de Aparência

1. Faça login como **Administrador**
2. No menu lateral, clique em **🎨 Aparência**
3. A janela de configurações será aberta

### 2. Configurar Cores

Na aba **"Cores"**, você pode personalizar:

#### Cores Principais
- **Cor Primária**: Cor principal do sistema (botões, destaques)
- **Cor Secundária**: Cor de sucesso (confirmações, positivo)
- **Cor de Destaque**: Cor de avisos e destaques

#### Cores de Ação
- **Cor de Perigo**: Ações perigosas (cancelar, excluir)
- **Cor de Informação**: Informações neutras
- **Cor de Aviso**: Alertas e avisos

#### Cores de Texto
- **Texto Principal**: Cor do texto principal
- **Texto Secundário**: Cor do texto secundário/legendas

#### Cor de Fundo
- **Fundo Principal**: Cor de fundo do sistema

**Como escolher uma cor:**
1. Clique no quadrado colorido ao lado do nome da cor
2. Selecione a cor desejada no seletor
3. A prévia será atualizada automaticamente

### 3. Configurar Fontes

Na aba **"Fontes e Tamanhos"**, você pode:

#### Família da Fonte
- Digite o nome da fonte que deseja usar (ex: "Segoe UI", "Arial", "Calibri")
- A fonte deve estar instalada no sistema

#### Tamanhos de Fonte
- **Pequeno**: Textos muito pequenos, notas de rodapé
- **Normal**: Texto padrão do sistema
- **Médio**: Títulos de seção, botões
- **Grande**: Títulos importantes
- **Extra Grande**: Destaques
- **XX Grande**: Campos de entrada grandes
- **Enorme**: Valores principais (totais)

#### Raio da Borda
- Define o arredondamento dos cantos
- `0` = quadrado
- `4` = levemente arredondado (padrão)
- `12` = muito arredondado

### 4. Configurar Logotipo

Na aba **"Logotipo"**, você pode:

1. Marcar **"Mostrar logotipo no sistema"** para ativar
2. Clicar em **"Procurar..."** para selecionar uma imagem
3. Definir **Largura** e **Altura** em pixels

**Formatos aceitos:** PNG, JPG, JPEG, GIF

**Recomendações:**
- Use imagens em alta resolução
- Formato PNG com fundo transparente fica melhor
- Tamanho sugerido: 150x50 pixels

### 5. Salvar Configurações

Após fazer as mudanças:

1. Clique em **"💾 Salvar Configurações"**
2. Uma mensagem de sucesso será exibida
3. **IMPORTANTE**: Reinicie o sistema para aplicar as mudanças

### 6. Restaurar Padrão

Se quiser voltar às configurações originais:

1. Clique em **"🔄 Restaurar Padrão"**
2. Confirme a ação
3. Reinicie o sistema

## Esquema de Cores Padrão

O sistema vem configurado com um tema moderno em roxo:

| Elemento | Cor | Código Hex |
|----------|-----|------------|
| Primária | Roxo vibrante | `#6C5CE7` |
| Secundária | Verde moderno | `#00B894` |
| Destaque | Amarelo suave | `#FDCB6E` |
| Perigo | Vermelho suave | `#D63031` |
| Info | Azul claro | `#74B9FF` |
| Aviso | Amarelo claro | `#FFEAA7` |
| Texto Principal | Cinza escuro | `#2D3436` |
| Texto Secundário | Cinza médio | `#636E72` |
| Fundo | Cinza muito claro | `#F5F6FA` |

## Tamanhos de Fonte Padrão

| Tipo | Tamanho (pixels) |
|------|------------------|
| Pequeno | 8 |
| Normal | 10 |
| Médio | 11 |
| Grande | 13 |
| Extra Grande | 16 |
| XX Grande | 24 |
| Enorme | 32 |

## Exemplos de Personalizações

### Tema Azul Corporativo
- Primária: `#0052CC` (Azul corporativo)
- Secundária: `#00875A` (Verde aprovação)
- Destaque: `#FFAB00` (Laranja)
- Fonte: Arial

### Tema Verde Natural
- Primária: `#36B37E` (Verde natural)
- Secundária: `#00B8D9` (Azul água)
- Destaque: `#FFAB00` (Amarelo)
- Fonte: Calibri

### Tema Vermelho Energia
- Primária: `#FF5630` (Vermelho energia)
- Secundária: `#6554C0` (Roxo)
- Destaque: `#FFAB00` (Amarelo)
- Fonte: Tahoma

## Arquitetura Técnica

### Migração do Banco de Dados
- Arquivo: `database/migrations/003_add_aparencia_config.sql`
- Adiciona colunas de aparência na tabela `configuracoes`

### Serviço de Aparência
- Arquivo: `src/services/aparencia_service.py`
- Classe: `AparenciaService`
- Métodos:
  - `get_configuracoes()`: Obtém configurações
  - `salvar_configuracoes()`: Salva no banco
  - `restaurar_padrao()`: Restaura valores padrão

### Estilos Dinâmicos
- Arquivo: `src/ui/styles.py`
- Classe: `ModernStyles`
- Método: `carregar_configuracoes()`: Carrega do banco e aplica

### Interface Admin
- Arquivo: `src/ui/admin/aparencia_window.py`
- Classe: `AparenciaWindow`
- Interface completa com abas e seletores de cor

## Dicas Avançadas

### Cores Acessíveis
Para garantir boa legibilidade:
- Use cores com bom contraste
- Teste com texto claro e escuro
- Considere daltonismo ao escolher cores

### Fontes Legíveis
- Prefira fontes sans-serif para interfaces
- Segoe UI, Arial, Calibri são ótimas opções
- Evite fontes muito decorativas

### Logotipo
- Use PNG para melhor qualidade
- Fundo transparente é ideal
- Mantenha proporção adequada

## Solução de Problemas

### As mudanças não aparecem
- **Solução**: Certifique-se de reiniciar o sistema completamente

### Logotipo não aparece
- **Verifique**: Se o arquivo existe no caminho especificado
- **Verifique**: Se o formato é suportado (PNG, JPG, JPEG, GIF)
- **Verifique**: Se marcou "Mostrar logotipo no sistema"

### Fonte não mudou
- **Solução**: Certifique-se que a fonte está instalada no Windows
- **Alternativa**: Use fontes padrão do Windows

### Cores ficaram estranhas
- **Solução**: Use o botão "Restaurar Padrão" e comece novamente
- **Dica**: Teste mudanças uma de cada vez

## Backup

As configurações de aparência são armazenadas no banco de dados na tabela `configuracoes`.

Para fazer backup:
```sql
SELECT * FROM configuracoes WHERE chave = 'aparencia';
```

Para restaurar:
- Use a interface administrativa
- OU execute o script `aplicar_migracao_aparencia.py`

## Suporte

Em caso de problemas:
1. Verifique os logs em `logs/pdv.log`
2. Tente restaurar configurações padrão
3. Reaplique a migração se necessário

---

**Desenvolvido com ❤️ para personalização total do seu PDV!**
