# PLANO COMPLETO DE DESENVOLVIMENTO - SISTEMA PDV

## 📋 VISÃO GERAL DO PROJETO

Sistema PDV (Ponto de Venda) completo para mercadinho com:
- Interface administrativa completa
- Interface simplificada para operador de caixa
- Integração com Pinpad para pagamentos
- Geração de QR Code PIX
- Gestão completa de produtos, estoque, vendas e relatórios

---

## 🏗️ ARQUITETURA DO SISTEMA

### Tecnologias Utilizadas
- **Backend**: Python 3.x
- **Banco de Dados**: MySQL (localhost, root, sem senha)
- **Interface**: Tkinter (nativa Python)
- **QR Code**: qrcode + Pillow
- **Pagamentos**: Integração simulada com Pinpad
- **Relatórios**: ReportLab para PDF

### Estrutura de Diretórios
```
PDV/
├── venv/                       # Ambiente virtual Python
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── database.py         # Configuração do banco
│   ├── models/
│   │   ├── __init__.py
│   │   ├── produto.py
│   │   ├── categoria.py
│   │   ├── usuario.py
│   │   ├── venda.py
│   │   ├── item_venda.py
│   │   └── pagamento.py
│   ├── dao/
│   │   ├── __init__.py
│   │   ├── produto_dao.py
│   │   ├── categoria_dao.py
│   │   ├── usuario_dao.py
│   │   ├── venda_dao.py
│   │   └── pagamento_dao.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── venda_service.py
│   │   ├── pinpad_service.py
│   │   └── pix_service.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── login_window.py
│   │   ├── admin/
│   │   │   ├── __init__.py
│   │   │   ├── main_admin.py
│   │   │   ├── produtos_window.py
│   │   │   ├── categorias_window.py
│   │   │   ├── usuarios_window.py
│   │   │   ├── relatorios_window.py
│   │   │   └── estoque_window.py
│   │   └── caixa/
│   │       ├── __init__.py
│   │       ├── main_caixa.py
│   │       ├── venda_window.py
│   │       ├── pagamento_window.py
│   │       └── pix_window.py
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       ├── formatters.py
│       └── logger.py
├── database/
│   └── schema.sql               # Script de criação do banco
├── resources/
│   ├── images/                  # Ícones e imagens
│   └── sounds/                  # Sons de notificação
├── logs/                        # Logs do sistema
├── backups/                     # Backups automáticos
├── requirements.txt             # Dependências Python
├── README.md                    # Documentação
└── main.py                      # Ponto de entrada

```

---

## 🗄️ MODELO DO BANCO DE DADOS

### Tabelas Principais

#### 1. **categorias**
- id (INT, PK, AUTO_INCREMENT)
- nome (VARCHAR(100))
- descricao (TEXT)
- ativo (BOOLEAN)
- data_cadastro (DATETIME)

#### 2. **produtos**
- id (INT, PK, AUTO_INCREMENT)
- codigo_barras (VARCHAR(50), UNIQUE)
- nome (VARCHAR(200))
- descricao (TEXT)
- categoria_id (INT, FK)
- preco_custo (DECIMAL(10,2))
- preco_venda (DECIMAL(10,2))
- estoque_atual (INT)
- estoque_minimo (INT)
- unidade_medida (VARCHAR(20))
- ativo (BOOLEAN)
- data_cadastro (DATETIME)
- data_atualizacao (DATETIME)

#### 3. **usuarios**
- id (INT, PK, AUTO_INCREMENT)
- username (VARCHAR(50), UNIQUE)
- senha_hash (VARCHAR(255))
- nome_completo (VARCHAR(200))
- tipo (ENUM: 'admin', 'operador')
- ativo (BOOLEAN)
- data_cadastro (DATETIME)
- ultimo_acesso (DATETIME)

#### 4. **vendas**
- id (INT, PK, AUTO_INCREMENT)
- numero_venda (VARCHAR(20), UNIQUE)
- usuario_id (INT, FK)
- data_hora (DATETIME)
- subtotal (DECIMAL(10,2))
- desconto (DECIMAL(10,2))
- total (DECIMAL(10,2))
- status (ENUM: 'aberta', 'finalizada', 'cancelada')
- observacoes (TEXT)

#### 5. **itens_venda**
- id (INT, PK, AUTO_INCREMENT)
- venda_id (INT, FK)
- produto_id (INT, FK)
- quantidade (DECIMAL(10,3))
- preco_unitario (DECIMAL(10,2))
- desconto (DECIMAL(10,2))
- subtotal (DECIMAL(10,2))

#### 6. **pagamentos**
- id (INT, PK, AUTO_INCREMENT)
- venda_id (INT, FK)
- forma_pagamento (ENUM: 'dinheiro', 'debito', 'credito', 'pix')
- valor (DECIMAL(10,2))
- numero_parcelas (INT)
- status (ENUM: 'pendente', 'aprovado', 'recusado')
- nsu (VARCHAR(50))
- codigo_autorizacao (VARCHAR(50))
- dados_pix (TEXT)
- data_hora (DATETIME)

#### 7. **movimentacoes_estoque**
- id (INT, PK, AUTO_INCREMENT)
- produto_id (INT, FK)
- tipo (ENUM: 'entrada', 'saida', 'ajuste')
- quantidade (DECIMAL(10,3))
- motivo (VARCHAR(200))
- usuario_id (INT, FK)
- data_hora (DATETIME)

#### 8. **caixa**
- id (INT, PK, AUTO_INCREMENT)
- usuario_id (INT, FK)
- data_abertura (DATETIME)
- data_fechamento (DATETIME)
- valor_abertura (DECIMAL(10,2))
- valor_fechamento (DECIMAL(10,2))
- status (ENUM: 'aberto', 'fechado')

---

## 🎯 FUNCIONALIDADES DETALHADAS

### MÓDULO ADMINISTRATIVO

#### 1. Dashboard
- Resumo de vendas do dia
- Produtos com estoque baixo
- Vendas por período (gráficos)
- Top produtos mais vendidos
- Total em caixa

#### 2. Gestão de Produtos
- **Cadastro**: código de barras, nome, descrição, categoria, preços, estoque
- **Edição**: todos os campos editáveis
- **Exclusão**: lógica (marcar como inativo)
- **Busca**: por código, nome, categoria
- **Importação**: CSV/Excel de produtos
- **Etiquetas**: geração de etiquetas com código de barras

#### 3. Gestão de Categorias
- Criar, editar, excluir categorias
- Vincular produtos às categorias
- Visualizar produtos por categoria

#### 4. Gestão de Estoque
- Entrada de produtos
- Ajuste de estoque
- Histórico de movimentações
- Alertas de estoque mínimo
- Inventário completo

#### 5. Gestão de Usuários
- Cadastro de operadores e administradores
- Definição de permissões
- Ativar/desativar usuários
- Histórico de acessos

#### 6. Relatórios
- Vendas por período
- Vendas por produto
- Vendas por operador
- Formas de pagamento
- Movimentação de estoque
- Lucratividade
- Exportação para PDF/Excel

#### 7. Configurações
- Dados da empresa
- Configuração de impressora
- Configuração de pinpad
- Backup automático
- Parâmetros do sistema

### MÓDULO OPERADOR DE CAIXA

#### 1. Abertura de Caixa
- Login do operador
- Informar valor inicial em caixa
- Registro de abertura no banco

#### 2. Frente de Caixa (Interface Principal)
- **Entrada de Produtos**:
  - Leitor de código de barras (integrado)
  - Busca rápida por nome/código
  - Adição manual de quantidade
- **Lista de Itens**:
  - Exibição clara dos produtos
  - Quantidade, preço unitário, subtotal
  - Opção de remover item
  - Editar quantidade
- **Totalizador**:
  - Subtotal visível
  - Aplicação de descontos
  - Total destacado em fonte grande

#### 3. Finalização de Venda
- **Formas de Pagamento**:
  - Dinheiro (calcular troco)
  - Débito (integração pinpad)
  - Crédito (integração pinpad, parcelas)
  - PIX (gerar QR Code)
- **Múltiplas Formas**: permitir pagamento misto
- **Confirmação**: após aprovação do pagamento
- **Impressão**: cupom fiscal/não fiscal

#### 4. Operações Rápidas
- Cancelar venda em andamento
- Consultar preço de produto
- Sangria de caixa
- Reforço de caixa

#### 5. Fechamento de Caixa
- Contabilizar formas de pagamento
- Comparar com valor esperado
- Gerar relatório de fechamento
- Imprimir resumo

---

## 🔌 INTEGRAÇÕES

### 1. Pinpad
**Simulação de Integração** (estrutura preparada para integração real):
- Protocolo de comunicação serial/USB
- Comandos: inicialização, venda débito, venda crédito, cancelamento
- Captura de NSU, código de autorização
- Tratamento de erros (recusa, timeout)
- Interface mock para testes

**Estrutura para Integração Real**:
```python
class PinpadService:
    def conectar(self)
    def venda_debito(self, valor)
    def venda_credito(self, valor, parcelas)
    def cancelar_transacao(self, nsu)
    def desconectar(self)
```

### 2. QR Code PIX
- Geração de QR Code PIX estático (CPF/CNPJ do estabelecimento)
- Geração de payload PIX (EMV)
- Exibição do QR Code na tela
- Timer de expiração (configurável)
- Confirmação manual do pagamento pelo operador
- Estrutura preparada para integração com API bancária

**Dados do QR Code**:
- Chave PIX do estabelecimento
- Valor da transação
- Identificador único da transação
- Nome do beneficiário

---

## 🔒 SEGURANÇA

### 1. Autenticação
- Login com usuário e senha
- Hash de senhas (bcrypt)
- Sessão de usuário
- Timeout de inatividade

### 2. Autorização
- Controle de acesso por tipo de usuário
- Admin: acesso total
- Operador: apenas módulo de caixa

### 3. Auditoria
- Log de todas as operações críticas
- Registro de usuário, data/hora, ação
- Logs de vendas, pagamentos, alterações de estoque

### 4. Backup
- Backup automático diário do banco
- Armazenamento em diretório específico
- Manter últimos 30 dias

---

## 🎨 DESIGN DA INTERFACE

### Princípios de UX
- **Administrador**: interface completa com menus, abas, tabelas detalhadas
- **Operador**: interface minimalista, botões grandes, foco na venda
- **Cores**: esquema profissional (azul/branco para admin, verde/branco para caixa)
- **Fonte**: grande e legível para o operador
- **Atalhos**: teclas de atalho para operações frequentes

### Interface do Operador
- Tela única focada na venda
- Botões grandes para formas de pagamento
- Leitor de código de barras sempre ativo
- Feedback visual para cada ação
- Sons de confirmação (bip ao adicionar produto)

### Interface do Administrador
- Menu lateral com módulos
- Área de trabalho central
- Tabelas com ordenação e filtros
- Formulários organizados
- Gráficos e dashboards

---

## 📦 DEPENDÊNCIAS PYTHON

```txt
mysql-connector-python==8.2.0    # Conexão MySQL
bcrypt==4.1.2                    # Hash de senhas
pillow==10.1.0                   # Manipulação de imagens
qrcode[pil]==7.4.2               # Geração de QR Code
reportlab==4.0.7                 # Geração de PDF
pandas==2.1.4                    # Manipulação de dados
matplotlib==3.8.2                # Gráficos
openpyxl==3.1.2                  # Excel
pyserial==3.5                    # Comunicação serial (pinpad)
python-dateutil==2.8.2           # Manipulação de datas
```

---

## 🚀 ETAPAS DE DESENVOLVIMENTO

### Fase 1: Configuração do Ambiente (1h)
- [x] Criar virtual environment Python
- [x] Instalar dependências
- [x] Configurar MySQL
- [x] Criar estrutura de diretórios

### Fase 2: Banco de Dados (1h)
- [ ] Criar script SQL com todas as tabelas
- [ ] Executar script e validar estrutura
- [ ] Criar dados iniciais (usuário admin padrão)

### Fase 3: Camada de Dados (2h)
- [ ] Implementar models (classes Python)
- [ ] Implementar DAOs (acesso ao banco)
- [ ] Criar connection pool
- [ ] Testes unitários dos DAOs

### Fase 4: Serviços (2h)
- [ ] Serviço de autenticação
- [ ] Serviço de vendas
- [ ] Serviço de pinpad (mock)
- [ ] Serviço de PIX (geração QR Code)

### Fase 5: Interface Administrativa (4h)
- [ ] Tela de login
- [ ] Dashboard principal
- [ ] CRUD de produtos
- [ ] CRUD de categorias
- [ ] CRUD de usuários
- [ ] Gestão de estoque
- [ ] Relatórios

### Fase 6: Interface de Caixa (3h)
- [ ] Tela de abertura de caixa
- [ ] Frente de caixa principal
- [ ] Integração com leitor de código de barras
- [ ] Tela de pagamento
- [ ] Tela de PIX com QR Code
- [ ] Tela de fechamento de caixa

### Fase 7: Integrações (2h)
- [ ] Simulação de pinpad
- [ ] Geração de QR Code PIX
- [ ] Geração de cupom de venda
- [ ] Sistema de backup

### Fase 8: Testes e Ajustes (2h)
- [ ] Testes de fluxo completo
- [ ] Ajustes de interface
- [ ] Validações e tratamento de erros
- [ ] Documentação final

**TEMPO TOTAL ESTIMADO: 17 horas**

---

## 📝 OBSERVAÇÕES IMPORTANTES

### Integração com Pinpad Real
A integração está estruturada para facilitar a conexão com pinpads reais. Os principais fabricantes são:
- **Gertec**: PPC920, Mobi Pin 10
- **Ingenico**: iWL250, Link2500
- **PAX**: D195, S920

Para integração real, será necessário:
1. SDK do fabricante do pinpad
2. Certificados e credenciais da adquirente (Stone, Cielo, Rede, etc.)
3. Implementação dos protocolos específicos

### QR Code PIX
O sistema gerará QR Codes estáticos. Para PIX dinâmico com confirmação automática:
1. Necessário integração com API do banco
2. Webhook para receber confirmação de pagamento
3. Certificados de segurança

### Código de Barras
O sistema aceita código de barras por teclado (leitor USB emula teclado). Se necessário integração específica, implementar biblioteca apropriada.

### Impressão de Cupons
Implementação básica para impressoras térmicas não fiscais. Para impressora fiscal (ECF/SAT), necessário:
1. Driver específico do fabricante
2. Biblioteca de integração fiscal
3. Adequação à legislação tributária

---

## 🎓 PRÓXIMOS PASSOS APÓS APROVAÇÃO

1. Confirmar especificações e requisitos
2. Validar estrutura do banco de dados
3. Iniciar desenvolvimento seguindo as fases planejadas
4. Entregas incrementais para validação

---

**PLANO CRIADO EM:** 27/10/2025
**VERSÃO:** 1.0
**STATUS:** Aguardando aprovação para iniciar desenvolvimento
