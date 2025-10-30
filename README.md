# Sistema PDV - Ponto de Venda

Sistema completo de Ponto de Venda para mercadinhos e pequenos comércios.

## 🚀 Características

- ✅ Interface administrativa completa
- ✅ Interface simplificada para operadores de caixa
- ✅ Gestão completa de produtos e estoque
- ✅ Múltiplas formas de pagamento
- ✅ Integração com Pinpad (simulada, preparada para real)
- ✅ Geração de QR Code PIX
- ✅ Relatórios gerenciais
- ✅ Sistema de backup automático
- ✅ Controle de usuários e permissões

## 📋 Pré-requisitos

- Python 3.8 ou superior
- MySQL 8.0 ou superior
- Windows (compatível com adaptações para Linux/Mac)

## 🔧 Instalação

### 1. Clone ou baixe o projeto

```bash
cd c:/PDV
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o sistema

Copie o arquivo de configuração de exemplo e edite com suas credenciais:

```bash
copy config.ini.example config.ini
```

Edite `config.ini` com suas configurações:

```ini
[database]
host = localhost
port = 3306
user = root
password = SUA_SENHA_MYSQL_AQUI
database = pdv_sistema
pool_size = 5

[mercadopago]
# Credenciais do Mercado Pago (opcional)
access_token = SEU_ACCESS_TOKEN
public_key = SEU_PUBLIC_KEY

[pix]
# Configurações PIX Estático (opcional)
chave_pix = seu@email.com
nome_recebedor = Nome da Empresa

[sistema]
nome_empresa = Nome do Seu Comércio
cnpj = 00.000.000/0001-00
```

⚠️ **IMPORTANTE:** 
- O arquivo `config.ini` contém informações sensíveis e **NÃO** deve ser versionado
- Use `config.ini.example` como modelo
- Nunca compartilhe suas credenciais

### 5. Configure o MySQL

Certifique-se de que o MySQL está rodando e configure a senha no `config.ini`

### 6. Crie o banco de dados

Execute o script SQL:

```bash
mysql -u root -p < database/schema.sql
```

Ou pelo MySQL Workbench/phpMyAdmin, execute o arquivo `database/schema.sql`

### 7. Execute o sistema

```bash
python main.py
```

## 👤 Acesso Padrão

**Administrador:**
- Usuário: `admin`
- Senha: `admin123`

**Operador de Caixa:**
- Usuário: `operador`
- Senha: `operador123`

⚠️ **IMPORTANTE:** Altere as senhas padrão após o primeiro acesso!

## 📚 Documentação

- [Plano de Desenvolvimento](PLANO_DESENVOLVIMENTO.md) - Arquitetura e especificações completas
- [Manual do Usuário](docs/MANUAL_USUARIO.md) - Guia de uso do sistema (será criado)
- [Manual Técnico](docs/MANUAL_TECNICO.md) - Detalhes técnicos (será criado)

## 🏗️ Estrutura do Projeto

```
PDV/
├── venv/                  # Ambiente virtual
├── src/                   # Código fonte
│   ├── config/           # Configurações
│   ├── models/           # Modelos de dados
│   ├── dao/              # Acesso ao banco
│   ├── services/         # Lógica de negócio
│   ├── ui/               # Interfaces
│   └── utils/            # Utilitários
├── database/             # Scripts SQL
├── resources/            # Recursos (imagens, sons)
├── logs/                 # Logs do sistema
├── backups/              # Backups automáticos
└── main.py               # Ponto de entrada
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.x** - Linguagem principal
- **Tkinter** - Interface gráfica
- **MySQL** - Banco de dados
- **bcrypt** - Segurança de senhas
- **qrcode** - Geração de QR Code PIX
- **ReportLab** - Geração de relatórios PDF

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação completa ou entre em contato.

## 📄 Licença

Projeto desenvolvido para uso interno.

---

**Versão:** 1.0
**Data:** Outubro 2025
